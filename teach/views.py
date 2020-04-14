import base64
import logging
from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q, F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from teach.models import *


logging.basicConfig(level=logging.DEBUG)


# def check_is_login():
#     def wraper(fn):
#         fn.is_login = True
#         return fn
#     return wraper

def check_is_login(dc):
    name = dc['request'].COOKIES.get('my_cookie_key', '')
    name = base64.standard_b64decode(name.encode('utf-8')).decode('utf-8')
    if name == 'abc':
        dc['is_login'] = True
    else:
        dc['is_login'] = False
    return dc


# @check_is_login
def get_teachers(request):
    title = 'Teacher'
    teachers = Teachers.objects.all()
    # teachers = Teachers.objects.filter(emp__name='peipei')
    if teachers.exists():
        return render(request, 'teach/teacher.html', context=check_is_login(locals()))
    else:
        return HttpResponseRedirect(reverse('teach:emp'))


def get_subjects(request):
    subjects = Subjects.objects.all()
    # subjects = Subjects.objects.filter(name='abc')
    if subjects.exists():
        return render(request, 'teach/subjects.html', context=check_is_login(locals()))
    else:
        return HttpResponseRedirect(reverse('teach:emp'))


def get_emp(request):
    title = 'Employees'
    emps = Employees.objects.all()
    return render(request, 'teach/emp.html', context=check_is_login(locals()))


def index(request):
    title = 'Home'
    msg = 'This is Home Page!'

    return render(request, 'index.html', check_is_login(locals()))


def search(request):
    title = 'Search'
    msg = ''
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        wd = request.POST['wd']
        if wd == '':
            msg += 'search content can not be null'
        else:
            msg = request.POST.dict

    return render(request, 'teach/search.html', context=check_is_login(locals()))


def jsontest(request):
    title = 'JsonTest'
    msg = ''
    if request.method == 'GET':
        return render(request, 'teach/jsontest.html', context=check_is_login(locals()))

    elif request.method == 'POST':
        response = JsonResponse(request.POST.dict(), content_type='application/json')
        return response


MY_HEX_SALT = r'adsfljf465asdf aeq&((*fasdf321wq#@&<>?'


def login(request):
    data = {'title': 'Login'}

    if request.method == 'POST':
        name, pw, cf = get_user_and_pw(request.POST.dict())
        if name != '' and pw != '':
            if Guests.objects.filter(username=name).exists():
                guest = Guests.objects.first()
                if check_password(pw, guest.password):  # login success!
                    data['msg'] = 'Welcome Back, %s!' % name
                    data['is_login'] = True

                    guest.datetime = datetime.now()
                    guest.save()

                    logging.info(data)

                    rsp = render(request, 'index.html', context=data)
                    name = base64.standard_b64encode(name.encode('utf-8')).decode('utf-8')
                    rsp.set_cookie('my_cookie_key', name)
                    return rsp

            data['msg'] = 'Wrong Account or Password'
        else:
            data['msg'] = 'Wrong Input, unexpect empty! '

        return render(request, 'teach/login.html', data)

    elif request.method == 'GET':
        return render(request, 'teach/login.html', data)


def register(request):
    data = {'title': 'Register'}
    msg = ''

    if request.method == 'POST':
        name, pw, cf = get_user_and_pw(request.POST.dict())
        if name != '' and pw != '' and pw == cf:
            if not Guests.objects.filter(username=name).exists():
                guest = Guests()
                guest.username = name
                guest.password = make_password(pw, MY_HEX_SALT)
                guest.datetime = datetime.now()
                guest.save()

                data['msg'] = 'Congratulations!'
                return render(request, 'index.html', context=data)
            else:
                msg = 'This Account Name Has been Registered, please change another!'
        else:
            if name == '' or pw == '':
                msg = 'Wrong Input, unexpect empty! '
            else:
                msg = 'Two input password must be consistent'

        data['msg'] = msg
        return render(request, 'teach/register.html', data)

    elif request.method == 'GET':
        return render(request, 'teach/register.html', data)


def get_user_and_pw(dc: dict) -> tuple:
    name = dc.get('username', '')
    pw = dc.get('password', '')
    cf = dc.get('confirm', '')
    return name, pw, cf


def personal(request):
    title = 'Personal'
    msg = 'your COOKIE is : '
    for c in request.COOKIES.keys():
        msg += '\n' + c + ' : '
        msg += request.COOKIES[c] + '\n'
    name = request.COOKIES.get('my_cookie_key', '')
    if name != '':
        name = base64.standard_b64decode(name.encode('utf-8')).decode('utf-8')
        guest = Guests.objects.filter(username=name)
        if guest.exists():
            date_time = guest.first().datetime
    rsp = render(request, 'teach/personal.html', check_is_login(locals()))
    return rsp


def logout(request):
    title = 'Login'
    rsp = render(request, 'teach/login.html', locals())
    rsp.delete_cookie('my_cookie_key')
    return rsp


def get_single_emp(request, number):
    number = int(number)
    if 0 < number <= Employees.objects.count():
        emps = Employees.objects.all().order_by('birth')[number-1:number]

    title = 'Employees'
    return render(request, 'teach/emp.html', context=check_is_login(locals()))

