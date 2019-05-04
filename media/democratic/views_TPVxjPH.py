from django.shortcuts import render, HttpResponse
from . models import tableData
import xml.etree.ElementTree as ET
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
# Create your views here.


@csrf_exempt
def post(request):
    if request.method == 'POST':
        xml = ET.fromstring(request.body)
        xmlstr = ET.tostring(xml, encoding='utf8', method='xml')
        reqId = xml.find('request_id').text
        ref = xml.find('reference').text
        if(xml.find('customer/id') != None):  # 2
            ip = xml.find('customer/ip').text
            xid = xml.find('customer/id').text
            operator = xml.find('customer/operator').text
            m = tableData(reqId=reqId, ref=ref, ip=ip,
                          xid=xid, operator=operator, xmlData=xmlstr)

        elif(xml.find('customer/msisdn') != None):  # 3
            channel = xml.find('payment_parameters/channel').text
            ip = xml.find('customer/ip').text
            msisdn = xml.find('customer/msisdn').text
            operator = xml.find('customer/operator').text
            m = tableData(reqId=reqId, ref=ref, ip=ip,
                          msisdn=msisdn, operator=operator, channel=channel, xmlData=xmlstr)

        elif(xml.find('action_result/code') != None):  # 4
            code = xml.find('action_result/code').text
            detail = xml.find('action_result/detail').text
            status = xml.find('action_result/status').text
            order = xml.find('payment_parameters/order').text
            m = tableData(reqId=reqId, ref=ref,
                          code=code, details=detail, status=status, order=order, xmlData=xmlstr)

        elif(xml.find('customer/customer') == None):  # 1
            channel = xml.find('payment_parameters/channel').text
            m = tableData(reqId=reqId, ref=ref,
                          channel=channel, xmlData=xmlstr)

        m.save()
        return HttpResponse("Success")
    else:
        return HttpResponse("Data in not stored")
