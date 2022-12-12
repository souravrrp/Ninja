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

# import csv
# import json
# def download_csv(request):
#     if request.method == 'POST':
#         data = request.POST
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="csv.csv"'

#         csv_writer = csv.writer(response)
#         for row in json.loads(data['csv-data']):
#             print(row)
#             csv_writer.writerow(row)
#         return response 

def bireport_view(request):
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
    return render(request, 'ninja/bireport.html', context)

import matplotlib.pyplot as plt
# import matplotlib.pyplot as mpld3
import mpld3

def todojs_view(request):
    todo = "ToDO JS"
    print(todo)
    context={
        "ToDo": todo
    }
    return render(request, 'ninja/todojs.html',context)

def tododj_view(request):
    todo = "ToDO DJ"
    print(todo)
    context={
        "ToDo": todo
    }
    return render(request, 'ninja/tododj.html',context)

def todobs_view(request):
    todo = "ToDO DJ"
    print(todo)
    context={
        "ToDo": todo
    }
    return render(request, 'ninja/todobs.html',context)

def calender_view(request):
    todo = "ToDO"
    print(todo)
    context={
        "ToDo": todo
    }
    return render(request, 'ninja/calender.html',context)

from django.conf import settings


def chart_view(request):
    # creating dataframe
    df = pd.DataFrame({
        'Name': ['John', 'Sammy', 'Joe'],
        'Age': [45, 67, 55]
    })
    
    # plotting a bar chart
    df.plot(x="Name", y="Age", kind="bar")
    plt.savefig(r'D:\Sourav SBL\Projects\Ninja\files\barchart.png')


    # plotting a scatter chart
    scat_fig, sc = plt.subplots()
    sc.scatter([1, 10], [5, 9])
    scat_html_graph = mpld3.fig_to_html(scat_fig)
    # html_graph =mpld3.fig_to_html(fig, d3_url=None, mpld3_url=None, no_extras=False, template_type='general', figid=None, use_http=False)

    
    # plotting a Bar Polar Chart
    np.random.seed(19680801)
    # Compute pie slices
    N = 20
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    radii = 10 * np.random.rand(N)
    width = np.pi / 4 * np.random.rand(N)
    colors = plt.cm.viridis(radii / 10.)
    bpc = plt.subplot(111, projection='polar')
    bpc.bar(theta, radii, width=width, bottom=0.0, color=colors, alpha=0.5)
    
    rootfilename = 'barpolarchart.png'
    filename = settings.MEDIA_ROOT + '/' + rootfilename
    plt.savefig(filename)
    # plt.savefig(r'D:\Sourav SBL\Projects\ninja\Ninja\static\img\barpolarchart.png')

    # plotting a Histogram
    fig = plt.figure()
    hf = fig.add_subplot(111)
    hf.grid(color='white', linestyle='solid')
    x = np.random.normal(size=1000)
    hf.hist(x, 30, histtype='stepfilled', fc='blue', alpha=0.5);
    histogram = mpld3.fig_to_html(fig)

    # plotting a Carve Chart
    x = np.arange(0, 5, 0.1)
    y = np.sin(x)
    cav_fig, ax = plt.subplots()    
    ax.plot(x, y)
    cav_html_graph = mpld3.fig_to_html(cav_fig)


    # plotting HTML plot Chart 
    html_plot_fig = plt.figure()
    x= df["Name"]
    y=df["Age"]
    plt.plot(x,y,'ro')
    html_plot_graph = mpld3.fig_to_html(html_plot_fig)

    # plotting HTML Bar Chart
    html_bar_fig = plt.figure()
    plt.bar(df.Name, df['Age'])
    plt.xlabel("Name")
    plt.ylabel("Age")
    html_bar_graph = mpld3.fig_to_html(html_bar_fig)

    # plotting a Histogram Chart
    hist_fig = plt.figure()
    histy=np.random.normal(170, 10, 250);#df["Age"]
    plt.hist(histy,histtype='stepfilled', fc='green', alpha=0.5)
    hist_graph = mpld3.fig_to_html(hist_fig)

    # plotting a Pie Chart
    pie_chart_fig = plt.figure()
    piex= df["Name"]
    piey=df["Age"]
    myexplode = [0.2, 0, 0]
    plt.pie(piey,labels = piex, explode = myexplode, shadow = True,autopct='%1.2f%%')
    plt.legend(title = "Person:")
    pie_chart_graph = mpld3.fig_to_html(pie_chart_fig)

    # plotting a Donut Chart
    donut_chart_fig = plt.figure()
    # create data
    dcx= df["Name"]
    dcy=df["Age"]
    # Create a pieplot
    plt.pie(dcy,labels=dcx, labeldistance=0.60)
    # add a circle at the center to transform it in a donut chart
    dc_circle=plt.Circle( (0,0), 0.5, color='white')
    p=plt.gcf()
    p.gca().add_artist(dc_circle)
    donut_chart_graph = mpld3.fig_to_html(donut_chart_fig)

    # plotting a Line Chart
    line_chart_fig = plt.figure()
    # create data
    lcy=df["Age"]
    plt.plot(lcy)
    line_chart_graph = mpld3.fig_to_html(line_chart_fig)

    # plotting a Connected Scatterplot
    scatterplot_fig = plt.figure()
    # create data
    plt.plot('Name', 'Age', data=df, linestyle='-', marker='o')
    scatterplot_graph = mpld3.fig_to_html(scatterplot_fig)

    # plotting a Barplot
    barplot_fig = plt.figure()
    # Make a random dataset:
    barx = df["Age"]
    bary = df["Name"]
    y_pos = np.arange(len(bary))
    # Create bars
    plt.bar(y_pos, barx)
    # Create names on the x-axis
    plt.xticks(y_pos, bary)
    barplot_graph = mpld3.fig_to_html(barplot_fig)


    Chart = "Chart"
    print(Chart)
    context={
        "chart": Chart
        # ,"plot": hist
        ,'histogram_chart': [histogram]
        ,'scat_chart': [scat_html_graph]
        ,'cav_chart' : [cav_html_graph]
        ,'html_plot_chart': [html_plot_graph]
        ,'html_bar_chart': [html_bar_graph]
        ,'hist_chart': [hist_graph]
        ,'html_pie_chart': [pie_chart_graph]
        ,'html_donut_chart': [donut_chart_graph]
        ,'html_line_chart': [line_chart_graph]
        ,'html_scatterplot': [scatterplot_graph]
        ,'html_barplot': [barplot_graph]
    }
    return render(request, 'ninja/chart.html',context)