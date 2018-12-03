# coding=utf-8

import json

def process_contact_detail():
    with open("/Users/yangjie/Desktop/temphoneU.txt", "rw") as load_f:
        load_dict = json.load(load_f)
        print load_dict['body']['extensiveInner']['serviceResultDetails']['MoXieCarrierReport'][0]['inputParams']

        contact_details = load_dict['body']['extensiveInner']['serviceResultDetails']['MoXieCarrierReport'][0]['outputResult']['call_contact_detail']
        sql='''
            insert into user_phone_call_6m(dial_cnt_6m,call_cnt_6m,peer_num) values(%s,%s,%s)
        '''
        index=1
        for contact in contact_details:
            try:
                pnum=contact['peer_num']
                pnum=str(pnum)
                if pnum.find('1')==-1:
                    continue
                if pnum is not None and pnum.index('1')==0 and len(pnum)>10:
                    # py_db.insert_one(sql,(contact['dial_cnt_6m'],contact['call_cnt_6m'],contact['peer_num']))
                    # print str(index)+","+str(contact['call_cnt_6m'])+","+str(contact['peer_num'])+","+str(contact['dial_cnt_6m'])
                    index=index+1
            except Exception,e:
                print e,contact['peer_num'].find('1')


if __name__=='__main__':
    print "main method"
    print 111





