# coding=utf8

import json
import re
import sys
import time

import xlwt

import db.mysqldbcenter as mydb

reload(sys)
sys.setdefaultencoding("utf-8")


def import_mobile_list(filepath):
    print '-------------手机号列表导入开始'
    arr = get_arr_from_file(filepath, ',')
    if len(arr) == 0:
        return

    for arr_index in range(len(arr)):
        arr_item = arr[arr_index]
        print arr_item['master_name'], arr_item['master_mobile'], arr_item[
            'master_idnum']
        contact_list_arr = json.loads(arr_item['contact_list'])
        for contact_item in contact_list_arr:
            qsql = '''
                select count(1) from user_phone_list where master_mobile=%s and mobile=%s
            '''
            qcount = mydb.getOne(
                qsql, (arr_item['master_mobile'], contact_item['phone']))
            if qcount > 0:
                continue

            sql = '''
                    insert into user_phone_list(master_name,master_mobile,master_idnum,name,mobile) values(%s,%s,%s,%s,%s)
                '''
            mydb.insertRow(sql,
                           (arr_item['master_name'], arr_item['master_mobile'],
                            arr_item['master_idnum'], contact_item['name'],
                            contact_item['phone']))

        if arr_index == 0:
            pass

    print '-------------手机号列表导入完成'


def import_report_moxie(filepath):
    print '-------------魔蝎通话详单数据导入开始'
    arr = get_arr_from_file(filepath, ',')
    for arr_item in arr:
        # print arr_item['master_name'],arr_item['master_mobile'],arr_item['master_idnum']
        import_report_moxie_detail(arr_item['contact_list'])
    print '-------------魔蝎通话详单数据导入完成'

def import_report_moxie_detail(load_data):
    load_dict=json.loads(load_data)
    name=load_dict['body']['base']['idName']
    idnum=load_dict['body']['base']['idNo']+ "'"
    mobile=load_dict['body']['base']['mobile']
    print name,idnum,mobile

    if not load_dict['body']['extensiveInner']['serviceResultDetails'].has_key('MoXieCarrierReport'):
        return
    contact_details = load_dict['body']['extensiveInner'][
        'serviceResultDetails']['MoXieCarrierReport'][0]['outputResult'][
            'call_contact_detail']

    qsql='''
        select count(1) from user_phone_call_analy where mobile=%s and peer_num=%s
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
                qcount=mydb.getOne(qsql,(mobile,contact['peer_num']))
                if qcount>0:
                    continue

                mydb.insertRow(
                    sql, (name,idnum,mobile,contact['dial_cnt_6m'], contact['call_cnt_6m'],
                            contact['peer_num']))
                index = index + 1
        except Exception, e:
            print e, contact['peer_num'].find('1')

# 导出表中的记录到excel表格中
def export_contact_analysis(filepath):
    print "---------------通话详单分析结果导出开始"
    print "导出文件名:",filepath
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
    
    wb.save(filepath)
    print '--------------通话详单分析结果导出完成'


def get_arr_from_file(filepath, seprate):
    arr = []
    with open(filepath, 'r') as mobile_stream:
        for index, line in enumerate(mobile_stream):
            dict_item = {}
            if index == 0:
                continue
            first_pos = line.index(seprate)
            name = line[0:first_pos]
            line = line[first_pos + 1:]
            second_pos = line.index(seprate)
            idnum = line[0:second_pos]
            line = line[second_pos + 1:]
            third_pos = line.index(seprate)
            mobile = line[0:third_pos]
            line = line[third_pos + 1:]
            dict_item['master_name'] = name
            dict_item['master_mobile'] = mobile
            dict_item['master_idnum'] = idnum
            dict_item['contact_list'] = line
            arr.append(dict_item)
    # print json.dumps(arr)
    return arr

def cleandata():
    # sql='''
    #     delete from user_phone_list
    # '''
    # mydb.delall(sql,())
    sql='''
        delete from user_phone_call_analy
    '''
    mydb.delall(sql,())


def process_order_line():
    curdate=time.strftime('%Y%m%d',time.localtime(time.time()))
    filename='/Users/yangjie/Downloads/txl_overdue_days_1-'+curdate+'.csv'
    # filename='/Users/yangjie/Desktop/txl_overdue_days_1-'+curdate+'.csv'
    import_mobile_list(filename)
    filename='/Users/yangjie/Downloads/overdue_days_1-'+curdate+'.csv'
    import_report_moxie(filename)
    export_filename="/Users/yangjie/Downloads/通话详单解析"+str(curdate)+"-逾期1天.xls"
    export_contact_analysis(export_filename)
    cleandata()

    curdate=time.strftime('%Y%m%d',time.localtime(time.time()))
    filename='/Users/yangjie/Downloads/txl_overdue_days_4-'+curdate+'.csv'
    import_mobile_list(filename)
    filename='/Users/yangjie/Downloads/overdue_days_4-'+curdate+'.csv'
    import_report_moxie(filename)
    export_filename="/Users/yangjie/Downloads/通话详单解析"+str(curdate)+"-逾期4天.xls"
    export_contact_analysis(export_filename)
    cleandata()

    curdate=time.strftime('%Y%m%d',time.localtime(time.time()))
    filename='/Users/yangjie/Downloads/txl_overdue_days_15-'+curdate+'.csv'
    import_mobile_list(filename)
    filename='/Users/yangjie/Downloads/overdue_days_15-'+curdate+'.csv'
    import_report_moxie(filename)
    export_filename="/Users/yangjie/Downloads/通话详单解析"+str(curdate)+"-逾期15天.xls"
    export_contact_analysis(export_filename)
    cleandata()

if __name__ == '__main__':
    process_order_line()

