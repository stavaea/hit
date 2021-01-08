#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from models import *
from django.http import JsonResponse
import json
from django.db import connection
import os
import time
# Create your views here.

def home(request):
    if request.session.get('user'):
        return render(request, 'home.html')
    else:
        return HttpResponseRedirect('/login/')

def signup(request):
    return render(request, 'signup.html')

def signout(request):
    request.session['user'] = None
    return HttpResponseRedirect('/login/')

def login(request):
    return render(request, 'login.html')

def task_list(request):
    kw = request.GET.get('kw')
    data = {'data': []}
    if kw:
        tasks = Task.objects.filter(name__contains=kw)
    else:
        tasks = Task.objects.all()
    if len(tasks) > 0:
        for task in tasks:
            d = {}
            d['id'] = task.id
            d['name'] = task.name
            data['data'].append(d)
    return render(request, 'task_list.html', data)

def task_new(request):
    return render(request, 'task_new.html', {'all': Cases.objects.all()})

def get_task_list(request):
    kw = request.GET.get('kw')
    data = {'data': []}
    if kw:
        tasks = Task.objects.filter(name__contains=kw)
    else:
        tasks = Task.objects.all()
    if len(tasks) > 0:
        for task in tasks:
            d = {}
            d['id'] = task.id
            d['name'] = task.name
            data['data'].append(d)
    return HttpResponse(content_type='application/json', content=json.dumps(data, ensure_ascii=False))

def task_delete(request):
    id = request.POST.get('id')
    data = {}
    if id:
        if Task.objects.filter(id=id).exists():
            try:
                Task.objects.filter(id=id).delete()
                data['flag'] = 0
            except:
                data['flag'] = 1
        else:
            data['flag'] = 1
    else:
        data['flag'] = 1
    return HttpResponse(content_type='application/json', content=json.dumps(data, ensure_ascii=False))

def check_username(request):
    name = request.POST.get('name')
    if name:
        users = User.objects.filter(name=name)
        if users.exists():
            return JsonResponse({"valid": False})
    return JsonResponse({"valid": True})

def signup_submit(request):
    name = request.POST.get('username', None)
    password = request.POST.get('password', None)
    email = request.POST.get('email', None)
    if name and password and email:
        users = User.objects.filter(name=name)
        if not users.exists():
            try:
                User.objects.create(name=name, password=password, email=email)
                return render(request, 'alert.html',
                              {'data': json.dumps({'url': '/login/', 'flag': 0, 'message': u'注册成功'})})
            except:
                return render(request, 'alert.html',
                              {'data': json.dumps({'url': '/signup/', 'flag': 1, 'message': u'信息存储错误'})})
        else:
            return render(request, 'alert.html', {'data': json.dumps({'url': '/signup/', 'flag': 1, 'message': u'用户名重复'})})
    else:
        return render(request, 'alert.html', {'data': json.dumps({'url': '/signup/', 'flag': 1, 'message': u'缺少必填项'})})

def login_submit(request):
    name = request.POST.get('username', None)
    password = request.POST.get('password', None)
    print password
    if name and password:
        users = User.objects.filter(name=name, password=password)
        if users.exists():
            request.session['user'] = users.first().name
            request.session.set_expiry(0)
            return HttpResponseRedirect('/home/')
        else:
            return render(request, 'alert.html',
                          {'data': json.dumps({'url': '/login/', 'flag': 1, 'message': u'用户名或密码错误'})})
    return render(request, 'alert.html', {'data': json.dumps({'url': '/login/', 'flag': 1, 'message': u'登录失败'})})

def task_info(request):
    id = request.GET.get('id')
    if id:
        tasks = Task.objects.filter(id=id)
        if tasks.exists():
            #查询用例关联关系，并返回
            return render(request, 'task_info.html', {'data': tasks.first(), 'all': Cases.objects.all(), 'cases': tasks.first().cases.all()})
        return render(request, 'alert.html', {'data': json.dumps({'url': '/task/list', 'flag': 1, 'message': u'测试任务不存在'})})

def task_submit(request):
    name = request.POST.get('taskname')
    desc = request.POST.get('description')
    cases = request.POST.get('cases')
    if name:
        if cases:
            if not Task.objects.filter(name=name):
                try:
                    task = Task.objects.create(name=name, description=desc)
                    cases_id = cases.split(',')
                    for c in cases_id:
                        case = Cases.objects.get(id=c)
                        task.cases.add(case)
                    return render(request, 'alert.html',
                                  {'data': json.dumps({'url': '/task/list', 'flag': 0, 'message': u'新增任务成功'})})
                except Exception as e:
                    print e
            else:
                return render(request, 'alert.html',
                              {'data': json.dumps({'url': '/task/list', 'flag': 1, 'message': u'任务名称已存在'})})
        else:
            return render(request, 'alert.html',
                          {'data': json.dumps({'url': '/task/list', 'flag': 1, 'message': u'未关联测试用例'})})
    return render(request, 'alert.html',
                  {'data': json.dumps({'url': '/task/list', 'flag': 1, 'message': u'新增任务失败'})})

def task_update(request):
    id = request.POST.get('id')
    name = request.POST.get('taskname')
    desc = request.POST.get('description')
    cases = request.POST.get('cases')
    if id and name:
        if cases:
            try:
                task = Task.objects.get(id=id)
                task.name = name
                task.description = desc
                task.save()
                # 更新用例-任务映射关系
                cases_id = cases.split(',')
                for index in range(len(cases_id)):
                    if index == 0:
                        task.cases = cases_id[0]
                    else:
                        case = Cases.objects.get(id=cases_id[index])
                        task.cases.add(case)
                return render(request, 'alert.html',
                              {'data': json.dumps({'url': '/task/list', 'flag': 0, 'message': u'更新任务成功'})})
            except Exception as e:
                print e
        else:
            return render(request, 'alert.html',
                          {'data': json.dumps({'url': '/task/list', 'flag': 1, 'message': u'未关联测试用例'})})
    return render(request, 'alert.html',
                  {'data': json.dumps({'url': '/task/list', 'flag': 1, 'message': u'更新任务失败'})})

def case_new(request):
    return render(request, 'case_new.html')

def case_submit(request):
    name = request.POST.get("name")
    desc = request.POST.get("desc")
    url = request.POST.get("url")
    method = request.POST.get("method")
    headers = request.POST.get("headers")
    body = request.POST.get("body")
    checks = request.POST.get("checks")
    if name and url and method and checks:
        if not Cases.objects.filter(name=name).exists():
            try:
                Cases.objects.create(name=name, desc=desc, url=url,
                                     method=method, headers=headers,
                                     body=body, checks=checks)
                data = {'flag': 0, 'message': u'新增用例成功'}
            except:
                data = {'flag': 1, 'message': u'新增用例失败'}
        else:
            data = {'flag': 1, 'message': u'用例名称已存在'}
    else:
        data = {'flag': 1, 'message': u'缺少必要参数'}
    return HttpResponse(content_type='application/json', content=json.dumps(data, ensure_ascii=False))

def task_run(request):
    id = request.GET.get('id', None)
    task = Task.objects.filter(id=id)
    if task.exists():
        data = {'id': id, 'name': task.first().name}
        return render(request, 'run.html', data)
    else:
        return render(request, 'alert.html',
                      {'data': json.dumps({'url': '/task/list', 'flag': 1, 'message': u'测试任务不存在'})})

def task_execute(request):
    task_id = request.GET.get('id', None)
    if task_id:
        if Task.objects.filter(id=task_id).exists():
            case_list = []
            # 获取到所有测试用例，判断是否存在，是否可运行
            cursor = connection.cursor()
            sql = "select cases_id from index_task_cases where task_id=%s" % task_id
            if cursor.execute(sql) > 0:
                cases = cursor.fetchall()
                for case_id in cases:
                   case = Cases.objects.filter(id=case_id[0])
                   if case.exists():
                       case_list.append(str(case.first().id))
                       case_list_str = ','.join(case_list)
                if len(case_list) > 0:
                    time_temp = time.time()
                    status = os.system("python ./index/run.py %s %f %s" % (task_id, time_temp, case_list_str))
                    if status == 0:
                        # 轮询任务历史表中知否存在报告信息
                        flag = 0
                        while(flag < 10):
                            his = History.objects.filter(time=time_temp)
                            if his.exists():
                                result = {'error_code': 0, "report_path":his.first().report}
                                return JsonResponse(result)
                            else:
                                flag += 1
                                time.sleep(1)
                        result = {'error_code': 10010, 'info': '超时无法获取报告地址'}
                    else:
                        result = {'error_code': 10010}
                # 没有可运行的用例
                else:
                    result = {'error_code': 10010, 'info': '无可执行的测试用例'}
            else:
                result = {'error_code': 10010, 'info': '无可执行的测试用例'}
        else:
            result = {'error_code': 10009}
    else:
        result = {'error_code': 10001}
    return JsonResponse(result)
