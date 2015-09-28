#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlwt  
from util import my_sort

def set_style(name,height,bold=False):
    style = xlwt.XFStyle() 
    
    font = xlwt.Font() 
    font.name = name # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height
    
    # borders= xlwt.Borders()
    # borders.left= 6
    # borders.right= 6
    # borders.top= 6
    # borders.bottom= 6
    
    style.font = font
    # style.borders = borders
    
    return style
 
 

def write_excel(l_d_par):
    f = xlwt.Workbook() 
 
 
    sheet1 = f.add_sheet(l_d_par[0]["mode"],cell_overwrite_ok=True)  
    
    #write the first line
    col_name_list=list(l_d_par[0].keys())
    col_name_list=my_sort(col_name_list)
    print(col_name_list)
    for i in range(0,len(col_name_list)):
        sheet1.write(0,i,col_name_list[i],set_style('Times New Roman',220,True))
    
    #write the rest lines
    for i in range(0,len(l_d_par)):
        for j in range(0,len(col_name_list)):
            #if col_name_list[j] != 'pic':
                sheet1.write(i+1,j,l_d_par[i][col_name_list[j]],set_style('Times New Roman',220,True))
            #lse:
              #  sheet1.insert_bitmap('a.bmp',i+1,j)

    try:
        f.save('result.xls')
    except Exception  as e1:
        print('except:', e1)

 
if __name__ == '__main__':
    write_excel([{'a':1,'b':2},{'a':3,'b':4}])
  