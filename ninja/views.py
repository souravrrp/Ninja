from multiprocessing import context
import os
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .forms import AddressForm

# Create your views here.
def index(request):
    return HttpResponse("Hello World!")

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