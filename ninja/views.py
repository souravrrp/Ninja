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
import datatable as dt
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
                df = df.rename(columns = {'REPORT_TITLE':'Report Title'})
                df = df.rename(columns = {'SENDER':'Sender'})
                pt=pd.pivot_table(df, values='EXEC_TIME', index='Report Title', columns= 'Sender', fill_value='-', margins=False)
                html=pt.to_html(table_id='preport')
                #table=dt.Frame(df)
                
                #html_table=df.to_html(classes='table table-stripped')
                # df = pd.DataFrame(raw_data)
                # pivot = pd.pivot_table(df, values='PDF_FILE_NAME', index='SENDER', columns='REPORT_ID')
                # print(pivot)

                # html = data.to_html()
                # res_data=pd.pivot_table(data=data)

                context = {"results": html}

    except cx_Oracle.DatabaseError:
        pass
    return render(request, 'ninja/preport.html', context)

def wreport_view(request):
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
                SELECT colt.order_no,
                colt.contract                tr_place,
                ecot.internal_po_no          doc_ref1,
                TRUNC (polt.rowversion)      tr_date,
                colt.catalog_no              part_code,
                polt.actual_qty_reserved     qty_out,
                polt.debit_note_no,
                --polt.debit_note_no           doc_ref2,
                --ecot.customer_no             dest_source,
                polt.debit_note_no           debit_note
            FROM ifsapp.customer_order_line_tab    colt,
                ifsapp.external_customer_order_tab ecot,
                ifsapp.trn_trip_plan_co_line_tab  polt,
                ifsapp.purchase_order_line_tab    o
        WHERE     colt.order_no = ecot.order_no
                AND colt.order_no = polt.order_no
                AND colt.line_no = polt.line_no
                AND colt.rel_no = polt.rel_no
                AND ecot.internal_po_no = o.order_no
                AND colt.contract in ( 'ABCW','SRMF','CMWH')
                AND colt.rowstate IN ('Invoiced', 'Delivered', 'PartiallyDelivered')
                AND TO_DATE (TO_CHAR (TRUNC (polt.rowversion), 'dd-MON-yy')) BETWEEN TO_DATE (
                                                                                        '2022/10/22',
                                                                                        'yyyy/mm/dd')
                                                                                AND TO_DATE (
                                                                                        '2022/10/22',
                                                                                        'yyyy/mm/dd')
                AND cust_ord_customer_api.get_cust_grp (
                        customer_order_api.get_customer_no (o.demand_order_no))
                        IS NULL
        ORDER BY polt.debit_note_no
                """
                # raw_res = dictfetchall(cursor.execute(sql))
                # raw_df=pd.DataFrame(raw_res)
                # raw_pt=pd.pivot_table(raw_df, values='QTY_OUT', index=['ORDER_NO', 'TR_DATE', 'TR_PLACE'], columns= 'PART_CODE', fill_value=0, aggfunc=np.sum)
                # raw_html=raw_pt.to_html()
                # print(raw_res)

                
                # cursor.execute(sql)
                # raw_data = cursor.fetchall()
                # print(raw_data)


                sql_data=pd.read_sql_query(sql,connection)
                columns=['ORDER_NO', 'TR_PLACE', 'DOC_REF1', 'TR_DATE', 'PART_CODE', 'QTY_OUT', 'DEBIT_NOTE_NO', 'DEBIT_NOTE']
                df = pd.DataFrame(sql_data)
                pt=pd.pivot_table(df, values='QTY_OUT', index=['ORDER_NO', 'TR_DATE', 'TR_PLACE'], columns= 'PART_CODE', fill_value=0, aggfunc='mean')
                html=pt.to_html()

                # df.to_csv(r'E:\file\FileName.csv', index = False, header=True)
                
                

                # df = pd.DataFrame(raw_data)
                # pivot = pd.pivot_table(df, values='PDF_FILE_NAME', index='SENDER', columns='REPORT_ID')
                # print(pivot)

                # html = data.to_html()
                # res_data=pd.pivot_table(data=data)

                context = {"results": html}

    except cx_Oracle.DatabaseError:
        pass
    return render(request, 'ninja/wreport.html', context)

import csv
import json
def download_csv(request):
    if request.method == 'POST':
        data = request.POST
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="csv.csv"'

        csv_writer = csv.writer(response)
        for row in json.loads(data['csv-data']):
            print(row)
            csv_writer.writerow(row)
        return response 