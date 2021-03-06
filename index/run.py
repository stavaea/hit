#coding:utf-8
import sys
import unittest
import HTMLTestRunnerCN
import time
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hit.settings")
django.setup()
from index.models import *
import http

class ITest(unittest.TestCase):
    case_list = sys.argv[3].split(',')
    for case_id in case_list:
        case = Cases.objects.filter(id=case_id).first()
        FUNC_TEMPLATE = '''def {test_id}(self):
                           '{desc}'
                           ITest.execute_case({data})
                        '''
        exec(FUNC_TEMPLATE.format(test_id='test_'+case.name, desc=case.desc, data=case_id))

    @classmethod
    def execute_case(cls, case_id):
        case = Cases.objects.filter(case=case_id).first()
        url = case.url
        method = case.method
        headers_str = case.headers
        body_str = case.body
        check_str = case.checks
        headers = {}
        if headers_str:
            list = headers_str.split('&')
            for l in list:
                headers[l.split('=')[0]] = l.split('=')[1]
        if body_str:
            if headers.get('content-type', None) == 'application/x-www-form-urlencoded' \
                or headers.get('content-type', None) == 'multipart/form-data':
                data = {}
                list = body_str.split('&')
                for l in list:
                    data[l.split('=')[0]] = l.split('=')[1]
            else:
                data = body_str
        client = http.client(url=url, method=method, headers=headers, data=data)
        if check_str:
            list = check_str.split('&')
            for l in list:
                if l.split('=')[0] == "response_code":
                    client.check_status_code(l.split('=')[1])
                elif l.split('=')[0] == "response_time":
                    pass

if __name__ == '__main__':
    task_id = sys.argv[1]
    task_time = sys.argv[2]
    suite = unittest.defaultTestLoader.discover('./index/', pattern='run.py')
    time_str = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    fp = open('./static/report/' + time_str + '.html', 'wb')
    HTMLTestRunnerCN.HTMLTestRunner(stream=fp, title='接口自动化测试报告').run(suite)
    History.objects.create(time=task_time, report='/static/report/'+time_str+'.html', status=1, task_id=task_id)
    # unittest.TextTestRunner().run(suite)

