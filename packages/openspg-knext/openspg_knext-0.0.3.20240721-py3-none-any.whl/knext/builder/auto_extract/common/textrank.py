# -*- coding: utf-8 -*-

import jieba
import networkx as nx
import numpy as np


def preprocess_text(text):

    words = jieba.lcut(text)
    # stopwords = set()
    # with open("stopwords.txt", "r", encoding="utf-8") as f:
    #     for line in f:
    #         stopwords.add(line.strip())
    # words = [word for word in words if word not in stopwords]
    return words


def build_graph(sentences):
    graph = nx.Graph()
    graph.add_nodes_from(range(len(sentences)))
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            similarity = calculate_similarity(sentences[i], sentences[j])
            if similarity > 0:
                graph.add_edge(i, j, weight=similarity)
    return graph


def calculate_similarity(sentence1, sentence2):
    words1 = set(sentence1)
    words2 = set(sentence2)
    common_words = words1.intersection(words2)
    return len(common_words) / (np.log(len(words1)) + np.log(len(words2)))


def textrank(sentences, num_sentences=3):
    processed_sentences = [preprocess_text(sentence) for sentence in sentences]
    graph = build_graph(processed_sentences)
    scores = nx.pagerank(graph)
    ranked_sentences = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top_sentence_indices = [idx for idx, score in ranked_sentences[:num_sentences]]
    top_sentences = [sentences[idx] for idx in sorted(top_sentence_indices)]
    return "".join(top_sentences)
