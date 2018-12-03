# -*- coding: utf-8 -*-

import urllib2
import xlrd
import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')


def getFile(file_name, url):
    # file_name = "/Users/yangjie/Desktop/test111.pdf"
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')

    block_sz = 8192 * 6
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        f.write(buffer)
    u.close
    f.close()
    print(file_name + " successful download")
    return 1


def get_pdf_by_boid(real_name, bo_id):

    del_url = "https://www.nonobank.com/User/deleteLoanAgreement/" + bo_id + "/1414"
    urllib2.urlopen(del_url)
    print del_url

    file_name = "/Users/yangjie/Desktop/tempPdf/" + real_name + "_借款协议_" + bo_id + ".pdf"
    url = "https://www.nonobank.com/User/agreement_borrow/" + bo_id + "/9527"
    print url
    getFile(file_name, url)
    getFile(file_name, url)

    file_name = "/Users/yangjie/Desktop/tempPdf/" + real_name + "_咨询服务协议_" + bo_id + ".pdf"
    url = "https://www.nonobank.com/User/GetBorrowCreditAgreement/" + bo_id + "/3306"
    print url
    getFile(file_name, url)
    getFile(file_name, url)


def get_pdf_by_url():
    real_name = "朱建中"
    bo_id = "1306426"

    del_url = "https://www.nonobank.com/User/deleteLoanAgreement/" + bo_id + "/1414"
    urllib2.urlopen(del_url)
    print del_url

    file_name = "/Users/yangjie/Desktop/tempPdf/" + real_name + "_借款协议_" + bo_id + ".pdf"
    url = "https://www.nonobank.com/ceph/download?bucket=e-signature-bucket&objid=7be3ac3d98c44dd8a1712ec60914cd54"
    print url
    getFile(file_name, url)
    # getFile(file_name, url)

    file_name = "/Users/yangjie/Desktop/tempPdf/" + real_name + "_咨询服务协议_" + bo_id + ".pdf"
    url = "https://extapi.fadada.com/api2//viewdocs.action?app_id=000307" \
          "&send_app_id=null&v=2.0&timestamp=20180111103651&transaction_id=TRANS1515637203057528567" \
          "&msg_digest=MjgyQjA0OUZEM0M3QUFEOEQ1MDlFM0Q5NEUxNEREMDdEMEY5NTRFOA=="
    print url
    getFile(file_name, url)
    # getFile(file_name, url)


if __name__ == '__main__':
    # file_name = "/Users/yangjie/Desktop/test111.pdf"
    # url = "https://www.nonobank.com/User/agreement_borrow/298022/2048"
    # getFile(file_name, url)
    real_name = "闫福强"
    bo_id = "2007647"
    get_pdf_by_boid(real_name,bo_id)
