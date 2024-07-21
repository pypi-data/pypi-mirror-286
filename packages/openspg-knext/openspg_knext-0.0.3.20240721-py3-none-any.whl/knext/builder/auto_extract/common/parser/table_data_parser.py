# -*- coding: utf-8 -*-

import re
from itertools import product
from bs4 import BeautifulSoup


class TableDataParser:
    @staticmethod
    def from_html(html_table: str):
        """
        html转为table
        最终格式为:[{
            "caption": "美国各州州名及首府（按州名首字母排序）", # option<str>
            "headers": ["序号", "州名", "英文", "简称", "首府", "英文_2"], #option<list>
            "header_position": "row", # option<str>
            "header_len": 1, # option<int>
            "data": [["序号", "州名", "英文", "简称", "首府", "英文_2"],
            [ "1", "亚拉巴马州", "Alabama", "AL", "蒙哥马利", "Montgomery" ],
            [ "2", "阿拉斯加州", "Alaska", "AK", "朱诺", "Juneau" ]]
        }]
        """
        html_content = TableDataParser.split_attr(html_table)
        soup = BeautifulSoup(html_content, "html.parser")
        output = []
        tables = soup.find_all("table")
        if len(tables) > 0:
            for table in tables:
                output.append(TableDataParser.parse_table(table))
        return output[0] if len(output) == 1 else output

    @staticmethod
    def parse_table(table_tag):
        output = {}
        rowspans = []  # track pending rowspans
        # table_metadata = {}
        caption = table_tag.find("caption")
        if caption:
            output["caption"] = re.sub(r"\s+", "", caption.get_text())
        rows = table_tag.find_all("tr")
        # first scan, see how many columns we need
        colcount = 0
        for r, row in enumerate(rows):
            cells = row.find_all(["td", "th"], recursive=False)
            colcount = max(
                colcount,
                sum(int(c.get("colspan", 1)) or 1 for c in cells[:-1])
                + len(cells[-1:])
                + len(rowspans),
            )
            # update rowspan bookkeeping; 0 is a span to the bottom.
            rowspans += [int(c.get("rowspan", 1)) or len(rows) - r for c in cells]
            rowspans = [s - 1 for s in rowspans if s > 1]

        if len(rows) > 2:
            first_row_cells = rows[0].find_all(["th"], recursive=False)
            # Check if the first row spans all columns and should be treated as caption
            if (
                len(first_row_cells) == 1
                and int(first_row_cells[0].get("colspan", 1)) == colcount
            ):
                # 只有当"caption"不存在或为空时，才进行赋值
                if not output.get("caption"):
                    output["caption"] = re.sub(
                        r"\s+", " ", first_row_cells[0].get_text()
                    )
                rows = rows[1:]
        table = {}
        rowspans = {}  # track pending rowspans, column number mapping to count
        for row, row_elem in enumerate(rows):
            span_offset = 0  # how many columns are skipped due to row and colspans
            all_cells_in_row: list = row_elem.find_all(["td", "th"], recursive=False)
            row_span_to_one = len(all_cells_in_row) > 0 and all(
                int(cell.get("rowspan", 1))
                == int(all_cells_in_row[0].get("rowspan", 1))
                for cell in all_cells_in_row
            )
            for col, cell in enumerate(all_cells_in_row):
                # adjust for preceding row and colspans
                col += span_offset
                while rowspans.get(col, 0):
                    span_offset += 1
                    col += 1
                # fill table data
                if (
                    row_span_to_one
                ):  # 有一种情况，为了排版一行中所有的row都有大于1的row span，但是其实都是一行数据，这样处理可以避免输出n次一样的数据，见https://baike.baidu.com/item/%E6%B2%B3%E5%8C%97%E7%9C%81?fromModule=lemma_search-box#2
                    rowspan = rowspans[col] = 1
                else:
                    rowspan = rowspans[col] = (
                        int(cell.get("rowspan", 1)) or len(rows) - row
                    )
                colspan = int(cell.get("colspan", 1)) or colcount - col
                # next column is offset by the colspan
                span_offset += colspan - 1

                value, is_header, links = TableDataParser.parse_cell(cell)
                for drow, dcol in product(range(rowspan), range(colspan)):
                    table[(row + drow, col + dcol)] = (value, links, is_header)
                    rowspans[col + dcol] = rowspan
            rowspans = {c: s - 1 for c, s in rowspans.items() if s > 1}
        # 找header
        first_row_idx = 0  # 默认第一个cell的位置是0，0
        first_col_idx = 0
        header_in_first_row = False
        header_in_first_col = False
        row_idx = -1
        check_row_limit = 3
        checked_row_count = 0
        for (row, col) in table:
            if row > row_idx:
                row_idx = row
                checked_row_count += 1
            if row == first_row_idx and col > first_col_idx and table[(row, col)][-1]:
                header_in_first_row = True
            if col == first_col_idx and row > first_row_idx and table[(row, col)][-1]:
                header_in_first_col = True
            if checked_row_count >= check_row_limit:
                break

        headers = []
        if (
            header_in_first_row and header_in_first_col
        ):  # 首行和首列都被解析成header了，解析错误，不写header，之后用大模型判断
            pass
        elif header_in_first_row:
            for (row, col) in table:
                if row == first_row_idx:
                    headers.append(re.sub(r"\s+", "", table[(row, col)][0]))
                if row > 0:
                    break
        elif header_in_first_col:
            for (row, col) in table:
                if col == first_col_idx:
                    headers.append(re.sub(r"\s+", "", table[(row, col)][0]))
        else:
            pass

        output["headers"] = headers
        if len(headers) > 0:
            output["header_len"] = 1
            if header_in_first_col:
                output["header_position"] = "column"
            if header_in_first_row:
                output["header_position"] = "row"
        else:
            output["header_position"] = "unknown"
            output["header_len"] = 0
        matrix = []
        header_rows = set()
        header_cols = set()
        for row in range(len(rows)):
            tmp = []
            for col in range(colcount):
                value = table.get((row, col), None)
                tmp.append(value)
                if value and value[-1]:  # value[-1]是判断是不是header
                    header_rows.add(row)
                    header_cols.add(col)
            if len(tmp) > 0 and not all(
                item == tmp[0] for item in tmp
            ):  # 空行不加入, 一行里所有列的值都一样，不加入
                matrix.append(tmp)
        raw_table = [[x[0] for x in y] for y in matrix]
        output["data"] = raw_table
        return output

    @staticmethod
    def parse_cell(cell):
        value = cell.get_text().strip()
        cell_content = cell.find_all("span")
        if cell_content is None:
            return value, False, None
        content_class = []
        for item in cell_content:
            class_name = item.get("class", ["text"])
            content_class += class_name
        content_class = " ".join(content_class)
        is_header = cell.name == "th" or cell.name == "th" in content_class
        links = [x.get("href", "") for x in cell.select("a[class^=innerLink]")]
        if is_header:
            value = re.sub(r"\s+", "", value)
        return value, is_header, links

    @staticmethod
    def dict_flatten(input_dict, size):
        output_list = []
        for idx in range(size):
            tmp = {}
            for k, v in input_dict.items():
                if idx < len(v):  # 检查索引是否有效
                    tmp[k] = v[idx]
                else:
                    tmp[k] = v[0]  # 如果超出了当前键的值列表长度，使用第一个值
            output_list.append(tmp)
        return output_list

    @staticmethod
    def split_attr(content):
        attrs = ["class", "rowspan", "colspan", "width", "align", "target", "data-uuid"]
        for attr in attrs:
            content = content.replace(f"{attr}=", f" {attr}=")
        return content
