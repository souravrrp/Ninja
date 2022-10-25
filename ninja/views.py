from lib2to3.pgen2.pgen import DFAState
from multiprocessing import context
import os
from turtle import pd
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
        print(password)
        try:
            cx_Oracle.init_oracle_client(lib_dir=r"D:\Installed_Software\instantclient_11_2")
        except:
            pass

        try:
            with cx_Oracle.connect(user="ifsapp", password="ifsapp", dsn="192.168.101.23/test") as connection:
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
    return render(request, 'ninja/print_pdf.html', context)


import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
db_dsn = os.environ["DB_DSN"]
db_lib_dir = os.environ["DB_LIB_DIR"]


def oreport_view(request):
    context={}
    try:
        cx_Oracle.init_oracle_client(lib_dir=db_lib_dir)
    except:
        pass

    user_id = request.session.get('username')
    user_password = request.session.get('password')
    try:
        with cx_Oracle.connect(user=db_user, password=db_password,
                                dsn=db_dsn) as connection:
            with connection.cursor() as cursor:

                sql = """
                select t1.*, t2.pdf_file_name from ARCHIVE_TAB t1, ARCHIVE_FILE_NAME_TAB t2 where t1.Result_Key=t2.result_key and 
    to_char(t1.ROWVERSION,'DD-MM-RRRR') = TO_CHAR(sysdate,'DD-MM-RRRR') order by t1.ROWVERSION desc
                """
                print(sql)
                raw_res = dictfetchall(cursor.execute(sql))
                context = {"results": raw_res}

    except cx_Oracle.DatabaseError:
        pass
    return render(request, 'ninja/oreport.html', context)

import pandas as pd
import numpy as np

def preport_view(request):
    context={}
    try:
        cx_Oracle.init_oracle_client(lib_dir=db_lib_dir)
    except:
        pass

    user_id = request.session.get('username')
    user_password = request.session.get('password')
    try:
        with cx_Oracle.connect(user=db_user, password=db_password,
                                dsn=db_dsn) as connection:
            with connection.cursor() as cursor:

                sql = """
                SELECT t1.*, t2.pdf_file_name, rd.report_title
                FROM ARCHIVE_TAB t1, ARCHIVE_FILE_NAME_TAB t2, report_definition rd
                WHERE     t1.Result_Key = t2.result_key
                AND TO_CHAR (t1.ROWVERSION, 'DD-MM-RRRR') =
                TO_CHAR (SYSDATE, 'DD-MM-RRRR')
                AND t1.report_id = rd.report_id
                ORDER BY t1.ROWVERSION DESC
                """
                raw_res = dictfetchall(cursor.execute(sql))
                # print(raw_res)

                cursor.execute(sql)
                raw_data = cursor.fetchall()
                # print(raw_data)


                sql_data=pd.read_sql_query(sql,connection)
                df = pd.DataFrame(sql_data, columns=['RESULT_KEY', 'REPORT_TITLE', 'EXEC_TIME', 'SENDER', 'PDF_FILE_NAME'])
                pt=pd.pivot_table(df, values='EXEC_TIME', index='REPORT_TITLE', columns= 'SENDER', fill_value='-', margins=False)
                html=pt.to_html()
                # df = pd.DataFrame(raw_data)
                # pivot = pd.pivot_table(df, values='PDF_FILE_NAME', index='SENDER', columns='REPORT_ID')
                # print(pivot)

                # html = data.to_html()
                # res_data=pd.pivot_table(data=data)

                context = {"results": html}

    except cx_Oracle.DatabaseError:
        pass
    return render(request, 'ninja/preport.html', context)
