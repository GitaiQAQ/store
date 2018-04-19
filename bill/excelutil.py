# coding=utf8
import xlrd
import pdb
DEFAULT_SHEET_INDEX = 0
DEFAULT_ROW_INDEX = 3


def analyse(path):
    result = []
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(DEFAULT_SHEET_INDEX)
    
    for i in range(DEFAULT_ROW_INDEX, sheet.nrows):
        o = {
            'billno': sheet.cell(i, 6).value,
            'company': sheet.cell(i, 10).value, 
            'code': sheet.cell(i, 11).value, 
        }
        result.append(o)
     
    return result


if __name__ == '__main__':
    path = 'cangku.xls'
    analyse(path)
