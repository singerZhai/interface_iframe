# -*- coding: utf-8 -*-
import openpyxl
import string
from openpyxl.styles import Alignment


class Xls(object):

    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.active
        xls_rows = string.ascii_uppercase
        self.row_line_dict = {}
        for index, rows in enumerate(xls_rows):
            self.row_line_dict[str(index + 1)] = rows

    def xls_write(self, line, row, xls_str):
        res_line = self.row_line_dict[str(row)]
        self.sheet[str(res_line) + str(line)] = xls_str
        alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        self.sheet[str(res_line) + str(line)].alignment = alignment

    def set_width_height(self, col_list, lines, col_width=66, line_height=100):
        """
        :param col_list: ['A', 'B', 'C',...]
        :param col_width: 宽度值
        :param lines: 共调整多少行 must be int !!!!!!
        :param line_height: 高度值
        :return: None
        """
        for col in col_list:
            self.sheet.column_dimensions[col].width = col_width
        for line in range(1, lines + 1):
            self.sheet.row_dimensions[line].height = line_height

    def save(self, filename):
        self.wb.save(filename)


if __name__ == '__main__':
    xls = Xls()
    xls.xls_write(1, 1, 'admin')
    xls.xls_write(1, 2, '123')
    xls.xls_write(1, 3, '456')
    xls.set_width_height(['A', 'B', 'C', 'D'], 6)
    xls.save('./2.xlsx')
