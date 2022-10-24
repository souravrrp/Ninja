from multiprocessing import context
import os
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .forms import AddressForm

import cx_Oracle
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def index(request):
    return HttpResponse("Hello World!")

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def login_view(request):
    context={}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
    try:
        cx_Oracle.init_oracle_client(lib_dir=r"D:\Installed_Software\instantclient_10_1\network\ADMIN")
    except:
        pass

        try:
            with cx_Oracle.connect(user="ifsapp", password="userofifs", dsn="192.168.101.22/singerbd") as connection:
                with connection.cursor() as cursor:
                    sql = """select sysdate from dual"""
                    print(dictfetchall(cursor.execute(sql)))

                    request.session['username'] = username.upper()
                    request.session['password'] = password.upper()
                    return redirect('ninja:home')

        except cx_Oracle.DatabaseError:
            messages.warning(request, "Username or Password is incorrect !")
        return render(request, 'ninja/login.html', context)
    else:
        return render(request, 'ninja/login.html', context)

def signup(request):
    signup_form=AddressForm
    context={'form': signup_form}
    return render(request, 'ninja/signup.html',context)

def profile(request):
    return HttpResponse("This is profile page! This Page is under construction !!!")

def home_view(request):
    # folder path
    dir_path = r'files'

    # list to store files
    res = []

    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            res.append(path)
    print(res)
    context={'files': res}
    return render(request, 'ninja/home.html',context)

def report_view(request):
    create_form=AddressForm
    context={'form':create_form}
    return render(request, 'ninja/report.html',context)

def print_pdf(request, pdffilename):
    context={}
    context = {"pdffilename": pdffilename}
    filename = [pdffilename]    
    return render(request, 'ninja/print.html', context)