# -*- coding: utf-8 -*-

import xlrd
import urllib2
import time
from download import crawlpdf

import sys
reload(sys)
sys.setdefaultencoding('utf8')


def read_excel():
    ef = xlrd.open_workbook("/Users/yangjie/Desktop/temp.xlsx")
    print ef.sheet_names()
    sheet = ef.sheet_by_index(0)
    print sheet.name, sheet.nrows, sheet.ncols

    nrows = sheet.nrows

    for i in range(nrows):
        # print sheet.row_values(i)

        if i < 0:
            continue

        real_name = sheet.row_values(i)[1]
        bo_id = sheet.row_values(i)[2]
        

        
        if int(bo_id) < 2400000:
            bo_id = str(bo_id)
            print i, real_name, bo_id
            crawlpdf.get_pdf_by_boid(real_name, bo_id)


if __name__ == '__main__':
    read_excel()
