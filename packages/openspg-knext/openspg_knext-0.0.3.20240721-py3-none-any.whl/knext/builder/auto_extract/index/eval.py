# -*- coding: utf-8 -*-
import json
import os
import pickle
import numpy as np
from tenacity import retry, stop_after_attempt, wait_exponential
from knext.builder.auto_extract.index.openie_extractor import IndexExtractor
from knext.builder.auto_extract.index.build_graph import build_graph
from knext.builder.auto_extract.index.rag import HippoRAG
from knext.builder.auto_extract.model.chunk import Chunk, ChunkTypeEnum
from knext.builder.auto_extract.index.utils import EmbeddingService
from knext.builder.auto_extract.index.utils import (
    NodeType,
    EdgeType,
)
from knext.builder.auto_extract.splitter import DocSplitter
from knext.builder.auto_extract.common.llm_client import LLMClient

semantic_chunk_examples = [
    {
        "input": "杭州市灵活就业人员缴存使用住房公积金管理办法（试行）\n为扩大住房公积金制度受益面，支持灵活就业人员解决住房问题，根据国务院《住房公积金管理条例》、《浙江省住房公积金条例》以及住房和城乡建设部、浙江省住房和城乡建设厅关于灵活就业人员参加住房公积金制度的有关规定和要求，结合杭州市实际，制订本办法。\n一、本办法适用于本市行政区域内灵活就业人员住房公积金的自愿缴存、使用和管理。\n二、本办法所称灵活就业人员是指在本市行政区域内，年满16周岁且男性未满60周岁、女性未满55周岁，具有完全民事行为能力，以非全日制、个体经营、新就业形态等灵活方式就业的人员。\n三、灵活就业人员申请缴存住房公积金，应向杭州住房公积金管理中心（以下称公积金中心）申请办理缴存登记手续，设立个人账户。\n ",
        "output": [
            {"小节摘要": "管理办法的制定背景和依据", "小节起始点": "为扩大住房公积金制度受益面"},
            {"小节摘要": "管理办法的适用范围", "小节起始点": "一、本办法适用于本市行政区域内"},
            {"小节摘要": "灵活就业人员的定义", "小节起始点": "二、本办法所称灵活就业人员是指"},
            {"小节摘要": "灵活就业人员缴存登记手续", "小节起始点": "三、灵活就业人员申请缴存住房公积金"},
        ],
    },
    {
        "input": " 金华市灵活就业人员住房公积金\n缴存使用暂行办法\n第一章  总 则\n第一条 本办法所称灵活就业人员是指金华市行政区域内以个体经营、非全日制、新业态等方式灵活就业的完全民事行为能力人。\n第二条 灵活就业人员缴存的住房公积金归其个人所有，任何单位和个人不得挪作他用。\n第二章  申请条件\n第三条 灵活就业人员申请缴存须符合以下条件：\n（一）在金华市行政区域内有较稳定的经济收入来源；\n（二）年满18周岁，且男性不超过60周岁，女性不超过50周岁,具有完全民事行为能力。\n第三章  附 则\n第四条 本办法由金华市住房公积金管理中心负责解释。\n",
        "output": [
            {"小节摘要": "暂行办法的总则", "小节起始点": "金华市灵活就业人员住房公积金"},
            {"小节摘要": "总则", "小节起始点": "第一章  总 则"},
            {"小节摘要": "申请条件", "小节起始点": "第二章  申请条件"},
            {"小节摘要": "附则和解释权", "小节起始点": "第三章  附 则"},
        ],
    },
]


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
def split(doc_splitter, content):
    chunks = doc_splitter.semantic_chunk(
        content, threshold=1024, example=semantic_chunk_examples
    )
    return chunks


def create_data(file_path: str):

    qas = []
    documents = []
    llm_client = LLMClient.from_config_name(
        "deepseek",
        use_pre=False,
    )

    doc_splitter = DocSplitter(llm_client=llm_client)

    with open(file_path, "r") as reader:
        docs = json.loads(reader.read())
        for doc in docs:
            question = doc["question"]
            answer = []
            for document in doc["context"]:
                title, passages = document
                answer.append(title)
                content = "\n".join(passages)
                if len(content) > 10000:
                    sentences = doc_splitter.split_sentence(content)
                    contents = doc_splitter.slide_window(sentences, 10000, 512, "\n")
                else:
                    contents = [content]
                all_chunks = []
                for content in contents:
                    try:
                        chunks = doc_splitter.semantic_chunk(
                            content, threshold=1024, example=semantic_chunk_examples
                        )
                        all_chunks.extend(chunks)
                    except Exception as e:
                        print(f"semantic chunk fails, fallback to slide window chunk.")
                        sentences = doc_splitter.split_sentence(content)
                        for chunk_id, chunk in enumerate(
                            doc_splitter.slide_window(sentences, 1024, 100, "\n")
                        ):
                            name = f"{title}#{chunk_id}"
                            key = Chunk.generate_hash_id(name)
                            all_chunks.append(
                                Chunk(
                                    type=ChunkTypeEnum.Text,
                                    chunk_header="",
                                    chunk_name=name,
                                    chunk_id=key,
                                    content=chunk,
                                )
                            )

                    for chunk in all_chunks:
                        documents.append(
                            {
                                "title": f"{title}#{chunk.name}",
                                "text": chunk.content,
                            }
                        )
            qas.append((question, answer))
    dedup = set()
    idx = 0
    output = []
    for document in documents:
        title = document["title"]
        if title in dedup:
            continue
        dedup.add(title)
        output.append({"title": title, "text": document["text"], "idx": idx})
        idx += 1
    return qas, output


def compute_recall(golden_labels, pred_labels, pred_scores, top_k):
    golden_labels = set(golden_labels[:top_k])
    pred = {}
    tp = []
    fn = []
    for pred_label, pred_score in zip(pred_labels[:top_k], pred_scores[:top_k]):
        pred[pred_label] = pred_score
        if pred_label in golden_labels:
            tp.append([pred_label, pred_score])

    for golden_label in golden_labels:
        if golden_label not in pred:
            fn.append([golden_label, 0])
    return {
        "tp": tp,
        "fn": fn,
        "recall": len(tp) / (len(tp) + len(fn)),
    }


if __name__ == "__main__":
    workdir = os.path.expanduser("~/Src/libs/data/rag_eval/")
    data = []
    input_file = "eval_policy.json"
    basename = os.path.splitext(input_file)[0]
    corpus_file = os.path.join(workdir, f"{basename}_corpus.json")
    if not os.path.exists(corpus_file):
        print(f"Load eval data...")
        qas, corpus = create_data(os.path.join(workdir, input_file))
        with open(corpus_file, "w") as writer:
            writer.write(
                json.dumps(
                    {"qas": qas, "corpus": corpus},
                    ensure_ascii=False,
                    indent=4,
                )
            )

    else:
        with open(corpus_file, "r") as reader:
            content = json.loads(reader.read())

        qas = content["qas"]
        corpus = content["corpus"]

    openie_output_file = os.path.join(workdir, f"{basename}_openie.json")
    if not os.path.exists(openie_output_file):
        print(f"Run open information extraction...")
        for line in corpus:
            data.append(
                Chunk(
                    type=ChunkTypeEnum.Text,
                    chunk_header="",
                    chunk_name=line["title"],
                    chunk_id=line["idx"],
                    content=line["text"],
                )
            )

        job_conf = {
            "model_conf": [
                {
                    "model_name": "deepseek",
                    "lora_name": None,
                    "use_pre": False,
                },
            ],
            "name": "政策相关文件",
        }

        extractor = IndexExtractor(0, job_conf=job_conf)

        output = extractor.invoke(data)
        with open(os.path.join(workdir, openie_output_file), "w") as writer:
            writer.write(json.dumps(output, ensure_ascii=False, indent=4))

    index_file = os.path.join(workdir, f"{basename}_graph.pkl")
    embedding_service = EmbeddingService(use_pre=True, num_parallel=1)
    if not os.path.exists(index_file):
        print(f"Build graph index...")

        graph_data = build_graph(
            openie_output_file=openie_output_file,
            embedding_service=embedding_service,
            workdir=workdir,
            nns=100,
            synonym_thresh=0.8,
        )
        print(graph_data.keys())
        pickle.dump(
            graph_data,
            open(
                os.path.join(workdir, f"{basename}_graph.pkl"),
                "wb",
            ),
        )

    edge_weights = {
        EdgeType.CHUNK_CONCURRENT_CHUNK.name: 1,
        EdgeType.ENTITY_CONCURRENT_ENTITY.name: 0.3,
        EdgeType.ENTITY_CONCURRENTINDOC_ENTITY.name: 0.7,
        EdgeType.ENTITY_SYNONYM_ENTITY.name: 1,
    }

    rag = HippoRAG(
        index_data_path=index_file,
        embedding_service=embedding_service,
        task_name="政策文件",
        extraction_model_name="deepseek",
        node_specificity=True,
        dpr_only=False,
        graph_alg="ppr",
        damping=0.5,
        similarity_threshold=0.8,
        recognition_threshold=0.9,
        edge_weights=edge_weights,
        weighted_graph=False,
    )

    info = []
    for query in qas:
        chunk_id, chunk_score, rank_info = rag.rank_docs(query[0], 10)
        info.append([chunk_id, chunk_score, rank_info])
        print("*" * 80)
        print(f"question: {query}")
        print(f"chunk_id: {chunk_id}")
        print(f"chunk_score: {chunk_score}")
        print(f"rank_info: {rank_info}")

    top_ks = [1, 2, 5, 10]
    scores = []
    recalls = {}
    for top_k in top_ks:
        score = {}
        for idx, query in enumerate(qas):
            rank_info = info[idx][-1]
            golden_labels = query[1]
            pred_labels = rank_info["ppr_documents"]
            pred_scores = rank_info["ppr_document_scores"]
            score[query[0]] = compute_recall(
                golden_labels, pred_labels, pred_scores, top_k=top_k
            )
        scores.append(score)
        recall = np.mean([x["recall"] for x in score.values()])
        recalls[top_k] = recall
