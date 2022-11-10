from django.urls import path
from . import views

app_name = "ninja"

urlpatterns = [
    # path('', views.dashboard, name='dashboard'),
    path('print/<pdffilename>/', views.print_pdf, name='print_pdf'),
    path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name= "logout"),
    path('home/', views.home_view, name= "home"),
    path('todojs/', views.todojs_view, name= "todojs"),
    path('tododj/', views.tododj_view, name= "tododj"),
    path('todobs/', views.todobs_view, name= "todobs"),
    path('calender/', views.calender_view, name= "calender"),
    path('chart/', views.chart_view, name= "chart"),
    path('report/', views.report_view, name= "report"),
    path('oreport/', views.oreport_view, name= "oreport"),
    path('preport/', views.preport_view, name= "preport"),
    path('wreport/', views.wreport_view, name= "wreport"),
    path('bireport/', views.bireport_view, name= "bireport"),
    path('signup/', views.signup, name="signup"),
    path('profile/', views.profile, name="profile"),
    path('',views.index,name='index'),
]