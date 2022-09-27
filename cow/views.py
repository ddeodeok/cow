from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.db.models import Q
from .models import Cow, Sensor, SensorID, Event
from datetime import datetime
from datetime import timedelta
from datetime import date
from django.contrib import auth
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import login
import time
import logging
import pandas as pd
import numpy as np
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

# 메인 페이지 
def cow (request):
    results = Sensor.objects.raw('SELECT * from cow_cow WHERE SensorID_id_id in ( select sensorID from cow_sensor where time in (select max(time) from cow_sensor group by sensorID) and vector > 50)')
    
    return render(
        request,
        'cow/main.html',{
            'results':results

        }
    )

# 로그인
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/main/')
        else:
            return render(request, 'cow/login.html', {'error': 'username or password is incorrect'})
    else:
        return render(request, 'cow/login.html')




# 로그아웃
def logout(request):
  auth.logout(request)
  return redirect('/')

   


# 차트 페이지 관리
def charts (request):
    pregnants = Cow.objects.filter(stats='임신')

    for i in range(len(pregnants)) :
        ev_time = pregnants[i].pregnancy_date
        childbirth_day =  ev_time + timedelta(days=285)
        print(childbirth_day)
        
    return render(
        request,
        'cow/charts.html',
        {
            'pregnants_count':Cow.objects.filter(stats='임신').count(),
            'fertilizations_count':Cow.objects.filter(stats='수정 완료').count(),
            'recent_count':Cow.objects.filter(stats__contains='최근 분만 우').count(),
            'preparations_count':Cow.objects.filter(stats='육성 우').count(),
            'total':Cow.objects.all().count()
     
        }
    )



# 소객체 테이블
def cowtables (request):
    cows = Cow.objects.order_by('-pk')

     # 현재날짜로 일령 계산
    for i in range(len(cows)) : 
        since_time = datetime.strptime(cows[i].birthday,'%Y.%m.%d')
        result = datetime.now() - since_time
        test = str(result).split()
        cows[i].age = int(test[0])
    return render(
        request,
        'cow/tables.html',
        {
            'cows':cows,
            'total':Cow.objects.all().count()
        }
    )



# 센서기록 테이블
def sensorTables (request):
    sensors = Sensor.objects.order_by('-pk')[:100]

    return render(
        request,
        'cow/sensor_tables.html',
        {
            'sensors':sensors,
        }
    )

# 센서 목록 테이블
def sensorTables2 (request):
    sensors2 = SensorID.objects.order_by('-pk')

    return render(
        request,
        'cow/sensor_tables2.html',
        {
            'sensors2':sensors2,
        }
    )


def calf (request):
    calfs = Cow.objects.filter(group__contains='송아지')
     # 현재날짜로 일령 계산
    for i in range(len(calfs)) : 
        since_time = datetime.strptime(calfs[i].birthday,'%Y.%m.%d')
        result = datetime.now() - since_time
        test = str(result).split()
        calfs[i].age = int(test[0])

    return render(
        request,
        'cow/tables_calf.html',
        {
            'calfs':calfs,
            'calf_count':Cow.objects.filter(group__contains='송아지').count()
        }
        
    )


def farm1 (request):
    farm1s = Cow.objects.filter(group__contains='제1')
         # 현재날짜로 일령 계산
    for i in range(len(farm1s)) : 
        since_time = datetime.strptime(farm1s[i].birthday,'%Y.%m.%d')
        result = datetime.now() - since_time
        test = str(result).split()
        farm1s[i].age = int(test[0])

    return render(
        request,
        'cow/tables_farm1.html',
        {
            'farm1s':farm1s,
            'farm1_count':Cow.objects.filter(group__contains='제1').count()
        }
    )


def farm2 (request):
    farm2s = Cow.objects.filter(group__contains='제2')
     # 현재날짜로 일령 계산
    for i in range(len(farm2s)) : 
        since_time = datetime.strptime(farm2s[i].birthday,'%Y.%m.%d')
        result = datetime.now() - since_time
        test = str(result).split()
        farm2s[i].age = int(test[0])

    return render(
        request,
        'cow/tables_farm2.html',
        {
            'farm2s':farm2s,
            'farm2_count':Cow.objects.filter(group__contains='제2').count()
        }
    )


def farm3 (request):
    farm3s = Cow.objects.filter(group__contains='제3')
         # 현재날짜로 일령 계산
    for i in range(len(farm3s)) : 
        since_time = datetime.strptime(farm3s[i].birthday,'%Y.%m.%d')
        result = datetime.now() - since_time
        test = str(result).split()
        farm3s[i].age = int(test[0])

    return render(
        request,
        'cow/tables_farm3.html',
        {
            'farm3s':farm3s,
            'farm3_count':Cow.objects.filter(group__contains='제3').count()
        }
    )



# 소 상세 페이지
def cow_detail (request, pk):
    # 센서, 상태 수정 페이지
    if request.POST:
        stat = request.POST['stats']
        print("stat:", stat)
        cowd = Cow.objects.get(pk=pk)
        cowd.stats = stat
        cowd.save()
    
    if request.POST:
        SensorID_ids = request.POST['SensorID_id']
        print('SensorID_id:', SensorID_ids)
        cowd = Cow.objects.get(pk=pk)
        cowd.SensorID_id = SensorID.objects.get(sensor_serial=SensorID_ids)
        cowd.save()
    # 이벤트 기록 입력 페이지
    if request.POST:
        event_nums = request.POST['event_name']
        event_ti = request.POST['event_time']
        event_de = request.POST['description']

        event_data = Event()
        event_data.event_name = event_nums
        event_data.event_time = event_ti
        event_data.description = event_de
        event_data.cid = Cow.objects.get(pk=pk)
        event_data.save()

        # str_left = str(event_data.event_time).split()
        # event_data.left=int(str_left[0])
    
    cowd = Cow.objects.get(pk=pk)
    sensors = Sensor.objects.all().order_by('-pk')[:100]
    sensorid = Sensor.objects.filter(sensorID=cowd.SensorID_id)[:250]
    sensorIDs = SensorID.objects.all()
    events = Event.objects.filter(cid=cowd)

    
    return render(
        request, 
        'cow/cow_detail.html',
        {
            'sensors':sensors,
            'cowd':cowd,
            'sensorid':sensorid,
            'sensorIDs':sensorIDs,
            'events':events,
            # 'cowdage':cowdage,
            
        }
    )



# 발정 객체 테이블
def estrus (request):
    fertilizations = Cow.objects.filter(stats='수정 완료')
    # 현재날짜로 일령 계산
    for i in range(len(fertilizations)) : 
        since_time = datetime.strptime(fertilizations[i].birthday,'%Y.%m.%d')
        result = datetime.now() - since_time
        test = str(result).split()
        fertilizations[i].age = int(test[0])

    return render(
        request,
        'cow/tables_estrus.html',
        {
            "fertilizations":fertilizations,
            'fertilizations_count':Cow.objects.filter(stats='수정 완료').count(),
        }
    )



# 최근 분만 객체 테이블
def recentDelivery (request):
    recentDeliverys = Cow.objects.filter(stats__contains='최근')
    print(recentDeliverys)
        # 현재날짜로 일령 계산
    for i in range(len(recentDeliverys)) : 
        since_time = datetime.strptime(recentDeliverys[i].birthday,'%Y.%m.%d')
        result = datetime.now() - since_time
        test = str(result).split()
        recentDeliverys[i].age = int(test[0])

    return render(
        request,
        'cow/tables_recentDelivery.html',
        {
            'recentDeliverys':recentDeliverys,
            'recent_count':Cow.objects.filter(stats__contains='최근').count(),
        }
    )



# 임신 테이블
def pregnant (request):
    pregnants = Cow.objects.filter(stats='임신')
    # 현재날짜로 일령(나이) 계산
    for i in range(len(pregnants)) : 
        since_time = datetime.strptime(pregnants[i].birthday,'%Y.%m.%d')
        result = datetime.now() - since_time
        test = str(result).split()
        pregnants[i].age = int(test[0])

    # 예상 분만 날짜 계산
    for i in range(len(pregnants)) :
        ev_time = pregnants[i].pregnancy_date
        childbirth_day =  ev_time + timedelta(days=285)
        pregnants[i].pregnancy_date = childbirth_day
        left_days = childbirth_day - datetime.now().date()
        str_left = str(left_days).split()
        pregnants[i].left=int(str_left[0])
        

    return render(
        request,
        'cow/tables_pregnant.html',
        {
            "pregnants":pregnants,
            'pregnants_count':Cow.objects.filter(stats='임신').count(),
            'childbirth_day':childbirth_day
            
        }
    )



# 수정대기 테이블
def rearingcalf (request):
    preparations = Cow.objects.filter(stats='육성 우')
        # 현재날짜로 일령 계산
    for i in range(len(preparations)) : 
        since_time = datetime.strptime(preparations[i].birthday,'%Y.%m.%d')
        result = datetime.now() - since_time
        test = str(result).split()
        preparations[i].age = int(test[0])

    return render(
        request,
        'cow/tables_rearingcalf.html',
        {
            'preparations':preparations,
            'preparations_count':Cow.objects.filter(stats='육성 우').count(),
        }
    )

    

# 소 추가 기능
class CowCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Cow
    
    template_name = 'cow/create_cow.html'
    fields=['cow_num','group','SensorID_id','age','stats','empyt_days','carving_num','birthday']

    def form_valid(self,form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(CowCreate, self).form_valid(form)
        else:
            return redirect('/login/')
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff



class CreateSensor(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = SensorID

    template_name = 'cow/create_sensor.html'
    fields = '__all__'
    def form_valid(self,form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(CreateSensor, self).form_valid(form)
        else:
            return redirect('/sensor_tables2/')
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff



        


        