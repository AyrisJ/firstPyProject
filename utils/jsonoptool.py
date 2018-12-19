# coding=utf-8

import json
import sys
import time

import xlrd
import xlwt

from db import mysqldbcenter as mydb

reload(sys)
sys.setdefaultencoding("utf-8")

# 导入逾期用户通讯录信息到数据库
def import_mobile_list(filepath):
    print "import_mobile_list begin-------------"
    try:
        with open(filepath, "r") as load_f:
            load_dict = json.load(load_f)
            mobile_list = load_dict['data']

        for item in mobile_list:
            qsql = '''
                select count(1) from user_phone_list where mobile=%s
            '''
            num = mydb.getOne(qsql, (item['phone'], ))
            if num > 0:
                continue

            if item['phone'].startswith('12593') or item['phone'].startswith(
                    '17951'):
                item['phone'] = item['phone'][5:]
            if item['phone'].startswith('+86'):
                item['phone'] = item['phone'][3:]
            if len(item['phone']) > 11 or item['phone'].startswith('0') or item['phone']=='':
                # print item['phone']
                continue

            # print item['phone']
            sql = '''
                insert into user_phone_list(mobile,name) values(%s,%s)
            '''
            mydb.insertRow(sql, (item['phone'], item['name']))
    except Exception as e:
        print e
    finally:
        pass
    print "import_mobile_list finish----------"

# 批量导入多个用户的通话记录数据到数据库
def import_all_contact_info(filepath):
    print "import_all_contact_info begin----------------"
    with open(filepath, "r") as load_f:
        load_datas = json.load(load_f)
    for load_data in load_datas['data']:
        import_contact_detail(load_data)
    
    print "import_all_contact_info finish------------------"

def import_contact_detail(load_data):
    # with open("/Users/yangjie/Desktop/temphoneU.txt", "r") as load_f:
    #     load_dict = json.load(load_f)
    load_dict=load_data
    name=load_dict['body']['base']['idName']
    idnum=load_dict['body']['base']['idNo']+ "'"
    mobile=load_dict['body']['base']['mobile']
    print name,idnum,mobile

    if not load_dict['body']['extensiveInner']['serviceResultDetails'].has_key('MoXieCarrierReport'):
        return
    contact_details = load_dict['body']['extensiveInner'][
        'serviceResultDetails']['MoXieCarrierReport'][0]['outputResult'][
            'call_contact_detail']

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
    print "export_contact_analysis begin---------------"
    wb = xlwt.Workbook()
    sheet_w = wb.add_sheet('sheet1')
    sheet_w.write(0, 0, unicode('姓名'))
    sheet_w.write(0, 1, unicode('手机号'))
    sheet_w.write(0, 2, unicode('身份证号'))
    sheet_w.write(0, 3, unicode('主叫联系人'))
    sheet_w.write(0, 4, unicode('主叫次数'))
    sheet_w.write(0, 5, unicode('主叫号码'))
    sheet_w.write(0, 6, unicode('被叫联系人'))
    sheet_w.write(0, 7, unicode('被叫次数'))
    sheet_w.write(0, 8, unicode('被叫号码'))
    
    gsql='''
        select name,mobile,idnum,count(1) from user_phone_call_analy group by name
    '''
    gresult=mydb.getAll(gsql,())
    index=0
    for item in gresult:
        startpos=(index)*30+1

        dialsql='''
            select upca.name,upca.mobile,upca.idnum,upca.dial_cnt_6m,upca.peer_num,ifnull(upl.name,'') as peer_name from user_phone_call_analy upca 
            left join user_phone_list upl 
            on upca.peer_num=upl.mobile
            where upca.mobile=%s order by dial_cnt_6m desc limit 30
        '''
        dialrecords=mydb.getAll(dialsql,(item['mobile'],))
       
        callsql='''
            select upca.name,upca.mobile,upca.idnum,upca.call_cnt_6m,upca.peer_num,ifnull(upl.name,'') as peer_name from user_phone_call_analy upca 
            left join user_phone_list upl 
            on upca.peer_num=upl.mobile
            where upca.mobile=%s order by call_cnt_6m desc limit 30
        '''
        callrecords=mydb.getAll(callsql,(item['mobile'],))

        for i in range(30):
            if startpos%30==1:
                sheet_w.write(startpos, 0, unicode(item['name']))
                sheet_w.write(startpos, 1, item['mobile'])
                sheet_w.write(startpos, 2, item['idnum'])
            
            sheet_w.write(startpos, 3, unicode(dialrecords[i]['peer_name']))
            sheet_w.write(startpos, 4, dialrecords[i]['dial_cnt_6m'])
            sheet_w.write(startpos, 5, dialrecords[i]['peer_num'])
            sheet_w.write(startpos, 6, unicode(callrecords[i]['peer_name']))
            sheet_w.write(startpos, 7, callrecords[i]['call_cnt_6m'])
            sheet_w.write(startpos, 8, callrecords[i]['peer_num'])
            startpos=startpos+1
            
            if i==0:
                pass;

        if index==0:
            pass;
        index=index+1
    
    curdate=time.strftime('%Y%m%d',time.localtime(time.time()))
    filename="通话详单解析"+str(curdate)+".xls"
    print "导出文件名:"+filename
    wb.save('/Users/yangjie/Desktop/'+filename)
    print 'export_contact_analysis finish--------------'


# 读取一个Excel表格内容写入到另一个Excel表格
def print_mobile_name():
    print "print_mobile_name begin----------------"
    try:
        curdate=time.strftime('%Y%m%d',time.localtime(time.time()))
        filename="通话详单解析"+str(curdate)+".xls"
        filename='/Users/yangjie/Desktop/'+filename
        print "导入文件名:"+filename
        readbook = xlrd.open_workbook(filename)
        sheet = readbook.sheet_by_index(0)
        nrows = sheet.nrows
        # ncols = sheet.ncols

        # print nrows, ncols
        # print sheet.cell_value(1, 1)
        # print sheet.row(1)[1]

        wb = xlwt.Workbook()
        sheet_w = wb.add_sheet('sheet2')

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

            namesql='''
                select name from user_phone_list where mobile=%s
            '''
            dialname=mydb.getOne(namesql,(str(sheet.cell_value(i, 5)),))
            callname=mydb.getOne(namesql,(str(sheet.cell_value(i, 8)),))
            if dialname is None:
                dialname=""
            if callname is None:
                callname=""
            sheet_w.write(i, 3, unicode(dialname))
            sheet_w.write(i, 6, unicode(callname))

            if i==1:
                break;

        curdate=time.strftime('%Y%m%d',time.localtime(time.time()))
        filename="通话详单解析-ulimate"+str(curdate)+".xls"
        print "导出文件名:"+filename
        wb.save('/Users/yangjie/Desktop/'+filename)
    except Exception, e:
        print e
    finally:
        pass
    print "print_mobile_name finish-----------------"


def cleandata():
    sql='''
        delete from user_phone_list
    '''
    mydb.delall(sql,())
    sql='''
        delete from user_phone_call_analy
    '''
    mydb.delall(sql,())


if __name__ == '__main__':
    import_all_contact_info("/Users/yangjie/Downloads/overdue1219_15.csv")
    # import_all_contact_info("/Users/yangjie/Downloads/overdue1217_1_2.csv")

    import_mobile_list("/Users/yangjie/Downloads/mobilelist1219_17.csv")
    export_contact_analysis()
    cleandata()
    # print_mobile_name()
