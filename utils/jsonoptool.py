# coding=utf-8

import json
import xlrd
import xlwt
from db import dbcenter as pydb
from db import mysqldbcenter as mydb

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def import_mobile_list():
    try:
        with open("/Users/yangjie/Desktop/mobile1205.txt", "r") as load_f:
            load_dict = json.load(load_f)
            mobile_list = load_dict['body']

        for item in mobile_list:
            qsql='''
                select count(1) from user_phone_list where mobile=%s
            '''
            num=pydb.getOne(qsql,(item['phone'],))
            if num>0:
                continue
            
            if item['phone'].startswith('12593') or item['phone'].startswith('17951'):
                item['phone']=item['phone'][5:]
            if item['phone'].startswith('+86'):
                item['phone']=item['phone'][3:] 
            if len(item['phone'])>11 or item['phone'].startswith('0'):
                # print item['phone']
                continue
            
            print item['phone']
            sql='''
                insert into user_phone_list(mobile,name) values(%s,%s)
            '''
            mydb.insertRow(sql,(item['phone'],item['name']))
    except Exception as e:
        print e
    finally:
        pass
    print "finish----------"

def import_contact_detail():
    with open("/Users/yangjie/Desktop/丛树亮-232325198004061850-18345198389.txt", "r") as load_f:
        load_dict = json.load(load_f)
        print load_dict['body']['extensiveInner']['serviceResultDetails'][
            'MoXieCarrierReport'][0]['inputParams']

        contact_details = load_dict['body']['extensiveInner'][
            'serviceResultDetails']['MoXieCarrierReport'][0]['outputResult'][
                'call_contact_detail']
        sql = '''
            insert into user_phone_call_6m(dial_cnt_6m,call_cnt_6m,peer_num) values(%s,%s,%s)
        '''
        index = 1
        for contact in contact_details:
            try:
                pnum = contact['peer_num']
                pnum = str(pnum)
                if pnum.find('1') == -1:
                    continue
                if pnum is not None and pnum.index(
                        '1') == 0 and len(pnum) > 10:
                    pydb.insertRow(
                        sql, (contact['dial_cnt_6m'], contact['call_cnt_6m'],
                              contact['peer_num']))
                    # print str(index)+","+str(contact['call_cnt_6m'])+","+str(contact['peer_num'])+","+str(contact['dial_cnt_6m'])
                    index = index + 1
            except Exception, e:
                print e, contact['peer_num'].find('1')


def print_mobile_test():

    try:
        readbook = xlrd.open_workbook(r'/Users/yangjie/Desktop/通话详单解析-1205.xlsx')
        sheet = readbook.sheet_by_index(0)
        nrows = sheet.nrows
        ncols = sheet.ncols

        print nrows, ncols
        print sheet.cell_value(1, 1)
        print sheet.row(1)[1]

        # print json.dumps("中文打印测试",encoding = 'gbk', ensure_ascii=True)

        with open("/Users/yangjie/Desktop/mobile1205.txt", "r") as load_f:
            load_dict = json.load(load_f)
            mobile_list = load_dict['body']
    
        wb = xlwt.Workbook()
        sheet_w = wb.add_sheet('sheet2')

        for i in range(len(mobile_list)):
            if i==0:
                print i,mobile_list[i]['phone'],mobile_list[i]['name']
            if mobile_list[i]['phone']=='18621580460':
                    print mobile_list[i]['name']

        for i in range(nrows):
            sheet_w.write(i,0,sheet.cell_value(i,0))
            sheet_w.write(i,1,sheet.cell_value(i,1))
            sheet_w.write(i,2,sheet.cell_value(i,2))
            sheet_w.write(i,4,sheet.cell_value(i,4))
            sheet_w.write(i,5,sheet.cell_value(i,5))
            sheet_w.write(i,7,sheet.cell_value(i,7))
            sheet_w.write(i,8,sheet.cell_value(i,8))

            if i == 0:
                sheet_w.write(i,3,sheet.cell_value(i,3))
                sheet_w.write(i,6,sheet.cell_value(i,6))
                continue            

            for mi in range(len(mobile_list)):
                # print mobile_list[mi]['phone'],int(sheet.cell_value(i,5))
                if mobile_list[mi]['phone']==str(int(sheet.cell_value(i,5))):
                    if i==44:
                        print i,mobile_list[mi]['phone']
                    sheet_w.write(i,3,mobile_list[mi]['name'])
                if mobile_list[mi]['phone']==str(int(sheet.cell_value(i,8))):
                    sheet_w.write(i,6,mobile_list[mi]['name'])
                    continue
                    


        wb.save('/Users/yangjie/Desktop/firstW.xls')

    except Exception, e:
        print e
    finally:
        pass

    print "finish-----------------"


if __name__ == '__main__':
    import_mobile_list()
