from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.db.models import Q
from .models import Cow, Sensor, SensorID
from datetime import datetime
from datetime import timedelta
import time
import logging

# Create your views here.

# 메인 페이지 
def cow (request):
    # cowd = Cow.objects.get(pk=pk)
    # sensors = Sensor.objects.all().order_by('-pk')[:100]
    # sensorid = Sensor.objects.filter(sensorID=cowd.SensorID_id)[:250]
    # if sensorid.vector >= 200:
    #     bar_li.append(senso)

    return render(
        request,
        'cow/main.html'
    )



# 차트 페이지 관리
def charts (request):
    pregnants = Cow.objects.filter(stats='Pregnancy')
    return render(
        request,
        'cow/charts.html',
        {
            'pregnants_count':Cow.objects.filter(stats='Pregnancy').count(),
            'fertilizations_count':Cow.objects.filter(stats='fertilization').count(),
            'recent_count':Cow.objects.filter(stats__contains='recent').count(),
            'preparations_count':Cow.objects.filter(stats='preparation for pregnancy').count(),
            'total':Cow.objects.all().count()

        }
    )



# 소객체 테이블
def cowtables (request):
    cows = Cow.objects.order_by('-pk')

    # print(cows[3].group)
    # if cows[3].group == 'calf farm':
    #     print("11111111111~",cows[3].group)
    #     cows[3].group = '송아지 농장'

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
        }
    )



# 소 상세 페이지
def cow_detail (request, pk):
        if request.POST:
          stat = request.POST['stats']
          print("stat:", stat)
          cowd = Cow.objects.get(pk=pk)
          cowd.stats = stat
          cowd.save()

        cowd = Cow.objects.get(pk=pk)
        sensors = Sensor.objects.all().order_by('-pk')[:100]
        sensorid = Sensor.objects.filter(sensorID=cowd.SensorID_id)[:250]
        
        return render(
            request, 
            'cow/cow_detail.html',
            {
                'sensors':sensors,
                'cowd':cowd,
                'sensorid':sensorid,
                
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
            'fertilizations_count':Cow.objects.filter(stats='fertilization').count(),
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
            'recent_count':Cow.objects.filter(stats__contains='recent').count(),
        }
    )



# 임신 테이블
def pregnant (request):
    pregnants = Cow.objects.filter(stats='임신')
    # 현재날짜로 일령 계산
    for i in range(len(pregnants)) : 
        since_time = datetime.strptime(pregnants[i].birthday,'%Y.%m.%d')
        result = datetime.now() - since_time
        test = str(result).split()
        pregnants[i].age = int(test[0])

    return render(
        request,
        'cow/tables_pregnant.html',
        {
            "pregnants":pregnants,
            'pregnants_count':Cow.objects.filter(stats='Pregnancy').count(),
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
            'preparations_count':Cow.objects.filter(stats='preparation for pregnancy').count(),
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
            return redirect('/login/')
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff



        


        