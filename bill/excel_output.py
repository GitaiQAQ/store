# -*- encoding: utf-8 -*-
import xlrd
import xlwt 
import itertools

import pdb
import sys

h1 = xlwt.easyxf(
    'font:name Arial, bold on,height 300; borders: bottom thin, top thin, right thin, left thin; align: vert centre, horz center')

text = xlwt.easyxf(
    'font:name Arial, bold off,height 220; borders: bottom thin, top thin, right thin, left thin;  align: vert centre, horz left')


text_centre = xlwt.easyxf(
    'font:name Arial, bold off,height 220; borders: bottom thin, top thin, right thin, left thin; align: vert centre, horz centre')

text_right = xlwt.easyxf(
    'font:name Arial, bold off,height 220; borders: bottom thin, top thin, right thin, left thin; align: vert centre, horz right')

def write_track_record( **kwargs):
    #导出订单
    f = xlwt.Workbook(encoding = 'utf-8')
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)
    col_width_t = 256*30
    col_width_b = 256*20
    col_width_s = 256*6
    col_width_m = 256*12
    
    # 入库记录
    try:
        for i in itertools.count():
            sheet1.col(i).width = col_width_m
    except ValueError:
        pass
    sheet1.col(1).width = col_width_t
    sheet1.col(2).width = col_width_b
    sheet1.col(4).width = col_width_t  
    header =  '订单记录'  
    sheet1.write_merge(0,1,0,9, header, h1) 
    sheet1.row(0).height_mismatch = True
    sheet1.row(0).height = 21*20 
    row4  = [u'序号', u'产品型号', u'金额', u'数量', u'订单号', 
             u'收货人',  u'电话']
              
    for i in range(0, len(row4)):
        sheet1.write(2, i, row4[i], text_centre)  
    sheet1.write(2, 9, '', text_centre)  
    i = 3
    j = 1
    total = 0
  
    if kwargs['in_track_result_list'] : 
        for item in kwargs['in_track_result_list']:
            sheet1.write(i, 0, j, text_centre)
            sheet1.write(i, 1, item.batch.no, text_centre)
            datestr = ''
            if item.batch.in_date:
                datestr = item.batch.in_date.strftime('%Y-%m-%d')
            sheet1.write(i, 2, datestr, text_centre)
            sheet1.write(i, 3, item.product.no, text_centre)
            
            sheet1.write(i, 4, item.product.name, text_centre)
            sheet1.write(i, 5, item.product.unit, text_centre)
            sheet1.write(i, 6, '', text_centre)
            sheet1.write(i, 7, item.available_num, text_centre)
            
            sheet1.write(i, 8, '', text_centre)  
            sheet1.write(i, 9, '', text_centre)
            i += 1
            j += 1   
     
    return f.save(kwargs['filename']) #保存文件


if __name__ == '__main__': 
      d = { 
            'aircraft_corp'  : u'外航公司名称',
            'code'          : u'code',
            'date'          : u'1988-12-14',
            'inventories'   : u'list',
            'filename'      : 'demo1.xls',
            'housename'        : u'保税仓库'
        }
      #filename = 'demo1.xls'
      fin_recive_list_xls( **d)
      print 'end'

