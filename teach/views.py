import base64
import logging
from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q, F
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

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
    try:
        count_per_page = int(request.GET.get('n', 5))
        if not 1 < count_per_page <= 10:
            count_per_page = 5
    except ValueError:
        count_per_page = 5

    print('count_per_page: %d' % count_per_page)

    paginator = Paginator(Employees.objects.all(), count_per_page)
    try:
        p = int(request.GET.get('p', 1))
        if not 0 < p <= paginator.num_pages:
            raise EmptyPage
    except (ValueError, EmptyPage):
        return render(request, '404.html')

    page = paginator.page(p)
    return render(request, 'teach/emp.html', context=check_is_login(locals()))


def index(request):
    title = 'Home'
    msg = 'Hello!'
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


class Search(ListView):
    model = Managers
    # allow_empty = True
    template_name = 'teach/search.html'
    # paginate_by = 2

    # can show all if no this 'get()', but can not search
    def get(self, request, *args, **kwargs):
        wd = request.GET.get('wd', '')
        print(wd)
        if wd != '':
            emp = Employees.objects.filter(name__contains=wd)
            ids = []
            print('********** 2')
            if emp.exists():
                for i in emp:
                    ids.append(i.id)
            self.queryset = self.model.objects.filter(emp_id__in=ids)
        else:
            self.queryset = self.model.objects.all()
        return super().get(request, args, kwargs)


class Detail(DetailView):
    id = None
    model = Employees
    pk_url_kwarg = 'id'
    template_name = 'teach/detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['id'] = 2
    #     return context

    def get(self, request, *args, **kwargs):
        pk = int(request.GET.get('id'))
        if pk:
            kwargs['id'] = pk
            print('\n**********************************')
            print(kwargs)
            return super().get(request, *args, **kwargs)
        else:
            return render(request, '404.html')


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

