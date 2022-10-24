from django.urls import path
from . import views

app_name = "ninja"

urlpatterns = [
    # path('', views.dashboard, name='dashboard'),
    path('print/<pdffilename>/', views.print_pdf, name='print_pdf'),
    path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name= "logout"),
    path('home/', views.home_view, name= "home"),
    path('report/', views.report_view, name= "report"),
    path('signup/', views.signup, name="signup"),
    path('profile/', views.profile, name="profile"),
    path('',views.index,name='index'),
]