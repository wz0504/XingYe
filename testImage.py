# -*- coding: UTF-8 -*_
from PIL import Image
from pytesseract import *

import PIL.ImageOps

import requests
import random
import json
import sys


headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        # 'Cookie':'route=fa5c35794f08bdb124232541bd13efbb; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22163af02a770542-0fa13927b80b8-336e7707-2359296-163af02a771127b%22%2C%22%24device_id%22%3A%22163af02a770542-0fa13927b80b8-336e7707-2359296-163af02a771127b%22%2C%22props%22%3A%7B%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%7D%7D; JSESSIONID=9kyvoTC9p28mJndgAzQonT5C3EEU6-Eu-h-NuQGsMZ4Fya-sGUyd!519313586',
        'Content-Type': 'text/html; charset=UTF-8',
}

session = requests.session()

def initTable(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


def getValidateCode():

    img_name = 'validateImg.png'
    code_url = 'https://ccshop.cib.com.cn:8010/application/cardapp/fastprogress/FastProgress/getValidateImg?' + str(random.random())

    resp = session.post(code_url, headers=headers)

    cat_img = resp.content
    with open(img_name, 'wb') as f:
        f.write(cat_img)
    # 图片的处理过程
    im = Image.open(img_name)
    im = im.convert('L')
    binaryImage = im.point(initTable(), '1')
    im1 = binaryImage.convert('L')
    im2 = PIL.ImageOps.invert(im1)
    im3 = im2.convert('1')
    im4 = im3.convert('L')

    # 将图片中字符裁剪保留
    box = (0, 0, 60, 28)
    region = im4.crop(box)
    # 将图片字符放大
    out = region.resize((120, 38))
    asd = pytesseract.image_to_string(out)

    code = asd.replace(' ', '')
    # print(code)
    if len(code) == 4:
        # print('4位验证码')
        return code
    else:
        return '0000'



def queryInfo(identity):


    code = getValidateCode()

    url = 'https://ccshop.cib.com.cn:8010/application/cardapp/fastprogress/FastProgress/query?id=' + identity + '&code=' + code
    # resp = requests.post(url, headers=headers, cookies=requests.utils.dict_from_cookiejar(home_conent.cookies),
    #                      data=data)
    resp = session.post(url, headers=headers)

    result = resp.content.decode("utf-8")


    if isinstance(result,str):

        result_json = json.loads(result)

        if isinstance(result_json,dict):

            return result_json

        else:
            return {}


def main():


    # print(sys.argv);
    isloop = True
    while isloop :


        query_result = queryInfo("341221199205045230")

        if 'code' in query_result.keys():
            if (query_result['code'] == 'err' and query_result['resInfo'] == '验证码不正确'):
                isloop = True
            else:
                isloop = False
        else:
            print('{}')


    print(query_result)

if __name__ == '__main__':
    main()