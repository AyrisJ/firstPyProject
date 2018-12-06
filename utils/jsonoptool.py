# coding=utf-8

import json
import xlrd
import xlwt
from db import dbcenter as pydb
from db import mysqldbcenter as mydb

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# 导入逾期用户通讯录信息到数据库
def import_mobile_list():
    try:
        with open("/Users/yangjie/Desktop/mobile1205.txt", "r") as load_f:
            load_dict = json.load(load_f)
            mobile_list = load_dict['body']

        for item in mobile_list:
            qsql = '''
                select count(1) from user_phone_list where mobile=%s
            '''
            num = pydb.getOne(qsql, (item['phone'], ))
            if num > 0:
                continue

            if item['phone'].startswith('12593') or item['phone'].startswith(
                    '17951'):
                item['phone'] = item['phone'][5:]
            if item['phone'].startswith('+86'):
                item['phone'] = item['phone'][3:]
            if len(item['phone']) > 11 or item['phone'].startswith('0'):
                # print item['phone']
                continue

            print item['phone']
            sql = '''
                insert into user_phone_list(mobile,name) values(%s,%s)
            '''
            mydb.insertRow(sql, (item['phone'], item['name']))
    except Exception as e:
        print e
    finally:
        pass
    print "finish----------"

# 批量导入多个用户的通话记录数据到数据库
def import_all_contact_info():
    with open("/Users/yangjie/Desktop/overdue_2.txt", "r") as load_f:
        load_datas = json.load(load_f)
    for load_data in load_datas['data']:
        import_contact_detail(load_data)
    
    print 111

def import_contact_detail(load_data):
    # with open("/Users/yangjie/Desktop/temphoneU.txt", "r") as load_f:
    #     load_dict = json.load(load_f)
    load_dict=load_data
    name=load_dict['body']['base']['idName']
    idnum=load_dict['body']['base']['idNo']+ "'"
    mobile=load_dict['body']['base']['mobile']
    print name,idnum,mobile

    contact_details = load_dict['body']['extensiveInner'][
        'serviceResultDetails']['MoXieCarrierReport'][0]['outputResult'][
            'call_contact_detail']
    sql2 = '''
        insert into user_phone_call_6m(dial_cnt_6m,call_cnt_6m,peer_num) values(%s,%s,%s)
    '''

    sql='''
        insert into user_phone_call_analy(name,idnum,mobile,dial_cnt_6m,call_cnt_6m,peer_num)
        values(%s,%s,%s,%s,%s,%s)
    '''

    index = 1
    for contact in contact_details:
        try:
            pnum = contact['peer_num']
            pnum = str(pnum)
            if pnum.find('1') == -1:
                continue
            if pnum is not None and pnum.index('1') == 0 and len(pnum) > 10:
                mydb.insertRow(
                    sql, (name,idnum,mobile,contact['dial_cnt_6m'], contact['call_cnt_6m'],
                            contact['peer_num']))
                index = index + 1
        except Exception, e:
            print e, contact['peer_num'].find('1')

# 导出表中的记录到excel表格中
def export_contact_analysis():
    wb = xlwt.Workbook()
    sheet_w = wb.add_sheet('sheet1')
    
    gsql='''
        select name,mobile,idnum,count(1) from user_phone_call_analy group by name
    '''
    gresult=mydb.getAll(gsql,())
    index=0
    for item in gresult:
        print item
        startpos=(index)*30
        endpos=(index+1)*30
        
        dialsql='''
            select name,mobile,idnum,dial_cnt_6m,peer_num from user_phone_call_analy where mobile=%s order by dial_cnt_6m desc limit 30 
        '''
        dialrecords=pydb.getAll(dialsql,(item['mobile']))
       
        callsql='''
            select name,mobile,idnum,call_cnt_6m,peer_num from user_phone_call_analy where mobile=%s order by call_cnt_6m desc limit 30
        '''
        callrecords=pydb.getAll(callsql,(item['mobile']))
        
        for i in range(30):
            if startpos%30==0:
                # sheet_w.write(startpos, 0, item['name'])
                sheet_w.write(startpos, 1, item['mobile'])
                sheet_w.write(startpos, 2, item['idnum'])
            sheet_w.write(startpos, 4, dialrecords[i]['dial_cnt_6m'])
            sheet_w.write(startpos, 5, dialrecords[i]['peer_num'])
            sheet_w.write(startpos, 7, callrecords[i]['call_cnt_6m'])
            sheet_w.write(startpos, 8, callrecords[i]['peer_num'])
            startpos=startpos+1

        if index==0:
            pass
        index=index+1
        
    wb.save('/Users/yangjie/Desktop/overdue_1206.xls')
    print 'i am the end line--------------'


# 读取一个Excel表格内容写入到另一个Excel表格
def print_mobile_test():

    try:
        readbook = xlrd.open_workbook(
            r'/Users/yangjie/Desktop/通话详单解析-1205.xlsx')
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
            if i == 0:
                print i, mobile_list[i]['phone'], mobile_list[i]['name']
            if mobile_list[i]['phone'] == '18621580460':
                print mobile_list[i]['name']

        for i in range(nrows):
            sheet_w.write(i, 0, sheet.cell_value(i, 0))
            sheet_w.write(i, 1, sheet.cell_value(i, 1))
            sheet_w.write(i, 2, sheet.cell_value(i, 2))
            sheet_w.write(i, 4, sheet.cell_value(i, 4))
            sheet_w.write(i, 5, sheet.cell_value(i, 5))
            sheet_w.write(i, 7, sheet.cell_value(i, 7))
            sheet_w.write(i, 8, sheet.cell_value(i, 8))

            if i == 0:
                sheet_w.write(i, 3, sheet.cell_value(i, 3))
                sheet_w.write(i, 6, sheet.cell_value(i, 6))
                continue

            for mi in range(len(mobile_list)):
                # print mobile_list[mi]['phone'],int(sheet.cell_value(i,5))
                if mobile_list[mi]['phone'] == str(
                        int(sheet.cell_value(i, 5))):
                    if i == 44:
                        print i, mobile_list[mi]['phone']
                    sheet_w.write(i, 3, mobile_list[mi]['name'])
                if mobile_list[mi]['phone'] == str(
                        int(sheet.cell_value(i, 8))):
                    sheet_w.write(i, 6, mobile_list[mi]['name'])
                    continue

        wb.save('/Users/yangjie/Desktop/firstW.xls')

    except Exception, e:
        print e
    finally:
        pass

    print "finish-----------------"


if __name__ == '__main__':
    export_contact_analysis()
