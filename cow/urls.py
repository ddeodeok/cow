from xml.etree.ElementInclude import include
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('',views.login),
    path('main/', views.cow),
    path('charts/', views.charts),
    path('tables/', views.cowtables),
    path('sensor_tables/', views.sensorTables),
    path('create_post/', views.CowCreate.as_view()),
    path('tables_calf/', views.calf),
    path('tables_estrus/', views.estrus),
    path('tables_pregnant/', views.pregnant),
    path('tables_rearingcalf/', views.rearingcalf),
    path('tables_farm1/', views.farm1),
    path('tables_farm2/', views.farm2),
    path('tables_farm3/', views.farm3),
    path('cow_detail/<int:pk>/', views.cow_detail),
    path('tables_recentDelivery/', views.recentDelivery),
    path('sensor_tables2/', views.sensorTables2),
    path('create_sensor/', views.CreateSensor.as_view()),

    # path('create_post/', views.create_post, name='create_post'),
    # path('create/', views.create, name='create'),

]