from flask import session
from django.http import HttpResponse
import random
import re
import csv, io
from django.shortcuts import render
from django.contrib import messages
import pandas as pd
import os
from django.template import loader
from django.shortcuts import render
from csv import reader
from .models import NewUser
from .models import *

import os
#import pickle
#import traceback
#import warnings
#import matplotlib.pyplot as plt
#import numpy as np
#import pandas as pd
#import seaborn as sns
#from sklearn import linear_model
#from sklearn import preprocessing
#np.random.seed()
#from sklearn.ensemble import RandomForestRegressor
#from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score, mean_absolute_error
#from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import MinMaxScaler
import os
from pathlib import Path
# Create your views here.
def index(request):
    return render(request, 'index.html')

MEDIA_ROOT="C:\Users\vedan\OneDrive\Desktop\4th sem\DataVisualizationProject\webapp\media"
BASE_DIR = Path(__file__).resolve().parent.parent
def load_dataset():
    path=str(BASE_DIR)+"\media\SampleCovid.csv"
    print(path)
    dataset = pd.read_csv(path, parse_dates=['Country'])
    print("DataSet : \n", dataset)
    output_dir = str(BASE_DIR) + '/output/'
    try:
        os.makedirs(output_dir)
    except OSError as e:
        pass



"""
is_data_loaded = False
def load_dataset():
    global ax, fig, x_train, x_test, y_train, y_test, dataset, output_dir
    if not is_data_loaded:
        print('Loading Dataset ...')
        dataset = pd.read_csv(MEDIA_ROOT + 'dataset.csv', parse_dates=['Country'])
        output_dir = MEDIA_ROOT + 'output_dir/'
        try:
            os.makedirs(output_dir)
        except OSError as e:
            pass

        print('Loaded Dataset!')
    else:
        print('Loaded Already Dataset!')
"""

def adminlogin(request):
    load_dataset()
    if request.method == 'POST':
        print("Admin Login Click Page")
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        if(uname=="admin" and pwd == "admin"):
            return render(request, 'adminmainpage.html', {'response':""})
        else:
            return render(request, 'adminlogin.html', {'response':"Invalid UserName/Password"})
    return render(request, "adminlogin.html",{'response':""})

def userlogincheck(request):
    print("User Login Page")
    if request.method == 'POST':
        print("User Login Click Page")
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        mydata = NewUser.objects.all()
        flag=False
        response=""
        for data in mydata:
            print("Data : ",data)
            if(data.username==uname and pwd == data.password):
                flag=True
                break
        if(flag):
            return render(request, 'usermainpage.html', {'response': response})
        else:
            return render(request, 'usermainpage.html', {'response': "Invalid UserName/Password"})
    return render(request, 'userlogin.html')

def userlogin(request):
    print("User Login Page")
    if request.method == 'POST':
        print("User Login Click Page")
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        mydata = NewUser.objects.all()
        flag=False
        response=""
        for data in mydata:
            print("Data : ",data)
            if(data.username==uname and pwd == data.password):
                flag=True
                break
        if(flag):
            return render(request, 'usermainpage.html', {'response': response})
        else:
            return render(request, 'usermainpage.html', {'response': "Invalid UserName/Password"})
    return render(request, 'userlogin.html')

def logout(request):
    return render(request, "index.html")

def adminviewusers(request):
    mydata = NewUser.objects.all()
    template = loader.get_template('adminviewusers.html')
    context = {'data': mydata}
    return HttpResponse(template.render(context, request))

def newuser(request):
    print("Add New User")
    form = NewUser
    if request.method == 'POST':
        print("Fname  : ", request.POST.get('fname'))
        print("Lname  : ", request.POST.get('lname'))
        print("Uname  : ", request.POST.get('uname'))
        print("Pwd    : ", request.POST.get('pwd'))
        print("Email  : ", request.POST.get('emailid'))
        print("Phone  : ", request.POST.get('phnum'))
        print("Gender : ", request.POST.get('gender'))
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        emailid = request.POST.get('emailid')
        phonenum = request.POST.get('phnum')
        gender = request.POST.get('gender')
        form = NewUser.objects.create(firstname=fname, lastname=lname,
                                      username=uname, password=pwd,
                                      emailid=emailid, phonenumber=phonenum, gender=gender)
        form.save()
        print("New User Saved Success")
    context = {'form': form, 'msg':"New User Saved Success"}
    return render(request, 'newuser.html', context)

def adminshowchart(request):
    print("Admin Show Chart")
    load_dataset()
    response=""
    headings=[]
    tabledata=[]
    data=[]
    if request.method == 'POST':
        graphtype = request.POST.get('graphtype')
        selectedcolumns = request.POST.getlist('column')
        selectedcountries = request.POST.getlist('country')
        print("Graph Type : ", graphtype)
        print("Selected Columns : ", selectedcolumns)
        print("Selected Countries : ", selectedcountries)
        # opening the CSV file
        #filename = request.session['filename']
        path=str(BASE_DIR) + "\media\SampleCovid.csv"
        with open(path, mode='r') as file:
            # reading the CSV file
            csvFile = csv.reader(file)
            # displaying the contents of the CSV file
            for lines in csvFile:
                #print(lines)
                tabledata.append(lines)
        
        tabledata = tabledata[1:]
        #print(data)
        for country in selectedcountries:
            print(country, " : ", end=' ')
            for row in tabledata:
                if(country in row):
                    #print(row[1:])
                    data.append(row[1:])

        if(graphtype=='BarChart'):
            tempdata={}
            bardata=[]
            i=0
            for country in selectedcountries:
                sum = 0
                for temp in data[i]:
                    sum = sum+float(temp)
                tempdata = {"label": country, "y": sum}
                bardata.append(tempdata)
                i+=1
            #print("Bar Data : ", bardata)
            return render(request, 'adminbarchart.html', {"bardata": bardata})
        elif (graphtype == 'ColumnChart'):
            tempdata = {}
            columndata = []
            i = 0
            for country in selectedcountries:
                sum = 0
                for temp in data[i]:
                    sum = sum + float(temp)
                tempdata = {"label": country, "y": sum}
                columndata.append(tempdata)
                i += 1
            # print("Bar Data : ", bardata)
            return render(request, 'admincolumnchart.html', {"columndata": columndata})
        elif (graphtype == 'PieChart'):
            tempdata = {}
            piedata = []
            i = 0
            for country in selectedcountries:
                sum = 0
                for temp in data[i]:
                    sum = sum + float(temp)
                tempdata = {"label": country, "y": sum}
                piedata.append(tempdata)
                i += 1
            return render(request, 'adminpiechart.html', {"pie_data": piedata})
        elif (graphtype == 'LineChart'):
            tempdata = {}
            linedata = []
            i = 0
            for country in selectedcountries:
                sum = 0
                for temp in data[i]:
                    sum = sum + float(temp)
                tempdata = {"label": country, "y": sum}
                linedata.append(tempdata)
                i += 1
            return render(request, 'adminlinechart.html', {"linedata": linedata})
        elif (graphtype == 'DoughnutChart'):
            tempdata = {}
            doughnutdata = []
            i = 0
            for country in selectedcountries:
                sum = 0
                for temp in data[i]:
                    sum = sum + float(temp)
                tempdata = {"label": country, "y": sum}
                doughnutdata.append(tempdata)
                i += 1
            return render(request, 'admindoughnutchart.html', {"doughnut_data": doughnutdata})
        elif (graphtype == 'AreaChart'):
            tempdata = {}
            areadata = []
            i = 0
            for country in selectedcountries:
                sum = 0
                for temp in data[i]:
                    sum = sum + float(temp)
                tempdata = {"label": country, "y": sum}
                areadata.append(tempdata)
                i += 1
        return render(request, 'adminareachart.html', {"areadata": areadata})
    return render(request, 'adminmainpage.html', {'response': response, 'headings': headings, 'data': data})

"""
def adminshowchart(request):
    print("Admin Show Chart")
    if request.method == 'POST':
        graphtype = request.POST.get('graphtype')
        selectedcolumns = request.POST.getlist('column')
        selectedcountries = request.POST.getlist('country')
        print("Graph Type : ", graphtype)
        print("Selected Columns : ", selectedcolumns)
        print("Selected Countries : ", selectedcountries)
        doc = request.FILES  # returns a dict-like object
        doc_name = doc['file']
        print("File name : ", doc_name)
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')
        print("Data Set : ", data_set)
        data = data_set.split("\r")
        tabledata = []
        for row in data:
            temp = row.split(",")
            temprow = []
            i=0
            flag=True
            for data in temp:
                temprow.append(data.replace("\n", ""))
                if(i!=0 and not data.isnumeric()):
                    flag=False
                    break
            if(flag):
                tabledata.append(temprow)

        columns = []
        data = []
        #print("Table Data : ", tabledata)

        for row in tabledata:
            print(row)

        for i in range(1, len(tabledata) - 1):
            temp = tabledata[i][0]
            columns.append(temp.replace("\n", ""))
            data.append(tabledata[i])

        collength = len(tabledata[0])
        rowlength = len(tabledata)
        print("Column Length : ", collength, " Row Length : ", rowlength)
        print("Columns : ", columns)
        matrixdata=[]
        for j in range(0, collength):
            temp=[]
            for i in range(0, rowlength-1):
                temp.append(tabledata[i][j])
            matrixdata.append(temp)

        print("Matrix Data : ", matrixdata)

        for row in matrixdata:
            print("Row : ", row)

        matrixdata2=[]
        matrixdata2.append(matrixdata[0])
        for i in range(1, len(matrixdata)):
            flag=True
            for j in range(1, len(matrixdata[i])):
                if (not isfloat(matrixdata[i][j])):
                    flag=False
                    break
            if(flag):
                matrixdata2.append(matrixdata[i])
        print("Matrix Data2 : ", matrixdata2)
        matrixdata=matrixdata2
        matrixdata1 = matrixdata[1:]
        #print("Matrix Data1 : ", matrixdata1)
        matrixdata2=[]
        for row in matrixdata1:
            temp = row[0].replace("\n", "")
            if temp in selectedcolumns:
                matrixdata2.append(row)

        #print("Matrix Data2 : ", matrixdata2)

        collength = len(matrixdata2[0])
        rowlength = len(matrixdata2)

        matrixdata3=[]
        for j in range(0, collength):
            temp=[]
            for i in range(0, rowlength):
                temp.append(matrixdata2[i][j])
            matrixdata3.append(temp)

        #print("Matrix Data3 : ", matrixdata3)
        headings = tabledata[0]
        countrynames = matrixdata[0]
        print("Headings      : ", headings)
        print("Country Names : ", countrynames)

        collength = len(matrixdata3)
        rowlength = len(countrynames)

        #print("Column Length : ", collength, " Row Length : ", rowlength)

        matrixdata4=[]
        for i in range(0,len(countrynames)):
            temp=[]
            temp.append(countrynames[i])
            for j in range(0,len(matrixdata3[0])):
                temp.append(matrixdata3[i][j])
            matrixdata4.append(temp)

        #print("Matrix Data4 : ", matrixdata4)

        matrixdata5 = []
        for i in range(1,len(matrixdata4)):
            temp = matrixdata4[i][0]
            if(temp in selectedcountries):
                matrixdata5.append(matrixdata4[i])

        #print("Matrix Data5 : ", matrixdata5)
        headings=[]
        for row in matrixdata5:
            headings.append(row[0])

        if(graphtype=="BarChart"):
            tempheading=tabledata[0]
            bardata1=[]
            numberdata=[]
            for row in matrixdata5:
                tempdata=row[1:]
                numberdata.append(tempdata)
            bardata = []
            for row in matrixdata5:
                sum = 0
                label = row[0].replace("\n", "")
                if label in selectedcountries:
                    for i in range(1, len(row)):
                        sum = sum + int(row[i])
                    tempdata = {"label": label, "y": sum}
                    bardata.append(tempdata)
            print("Bar Data : ", bardata)

            return render(request, 'barchart.html', {"bardata": bardata})
        elif (graphtype == "ColumnChart"):
            columndata=[]
            for row in matrixdata5:
                sum = 0
                label = row[0].replace("\n", "")
                if label in selectedcountries:
                    for i in range(1, len(row)):
                        sum = sum + int(row[i])
                    tempdata = {"label": label, "y": sum}
                    columndata.append(tempdata)
            return render(request, 'columnchart.html', {"columndata": columndata})
        elif (graphtype == "PieChart"):
            piedata=[]
            for row in matrixdata5:
                sum = 0
                label = row[0].replace("\n", "")
                if label in selectedcountries:
                    for i in range(1, len(row)):
                        sum = sum + int(row[i])
                    tempdata = {"label": label, "y": sum}
                    piedata.append(tempdata)
            return render(request, 'piechart.html', {"pie_data": piedata})
        elif (graphtype == "LineChart"):
            linedata = []
            for row in matrixdata5:
                sum = 0
                label = row[0].replace("\n", "")
                if label in selectedcountries:
                    for i in range(1, len(row)):
                        sum = sum + int(row[i])
                    tempdata = {"label": label, "y": sum}
                    linedata.append(tempdata)
            print("Line Data : ",linedata)
            return render(request, 'linechart.html', {"linedata": linedata})
        elif (graphtype == "DounutChart"):
            doughnutdata = []
            for row in matrixdata5:
                sum = 0
                label = row[0].replace("\n", "")
                if label in selectedcountries:
                    for i in range(1, len(row)):
                        sum = sum + int(row[i])
                    tempdata = {"label": label, "y": sum}
                    doughnutdata.append(tempdata)
            return render(request, 'doughnutchart.html', {"doughnut_data": doughnutdata})
        elif (graphtype == "AreaChart"):

            #print("Data : ", data)
            areadata = []
            for row in matrixdata5:
                sum = 0
                label = row[0].replace("\n", "")
                if label in selectedcountries:
                    for i in range(1, len(row)):
                        sum = sum + int(row[i])
                    tempdata = {"label": label, "y": sum}
                    areadata.append(tempdata)
            return render(request, 'areachart.html', {"areadata": areadata})
    response=""
    headings=""
    data=""
    return render(request, 'adminmainpage.html', {'response': response, 'headings': headings, 'data': data})
"""
def usershowchart(request):
    print("User Show Chart")
    load_dataset()
    response=""
    headings=[]
    tabledata=[]
    data=[]
    if request.method == 'POST':
        graphtype = request.POST.get('graphtype')
        selectedcolumns = request.POST.getlist('column')
        selectedcountries = request.POST.getlist('country')
        print("Graph Type : ", graphtype)
        print("Selected Columns : ", selectedcolumns)
        print("Selected Countries : ", selectedcountries)
        # opening the CSV file
        #filename = request.session['filename']
        path=str(BASE_DIR) + "\media\SampleCovid.csv"
        #path=str(BASE_DIR)+filename
        with open(path, mode='r') as file:
            # reading the CSV file
            csvFile = csv.reader(file)
            # displaying the contents of the CSV file
            for lines in csvFile:
                #print(lines)
                tabledata.append(lines)

        print("Date : ")
        tabledata = tabledata[1:]
        #print(data)
        for country in selectedcountries:
            print(country, " : ", end=' ')
            for row in tabledata:
                if(country in row):
                    #print(row[1:])
                    data.append(row[1:])

        if(graphtype=='BarChart'):
            tempdata={}
            bardata=[]
            i=0
            for country in selectedcountries:
                sum = 0
                for temp in data[i]:
                    sum = sum+float(temp)
                tempdata = {"label": country, "y": sum}
                bardata.append(tempdata)
                i+=1
            #print("Bar Data : ", bardata)
            return render(request, 'userbarchart.html', {"bardata": bardata})
        elif (graphtype == 'ColumnChart'):
            tempdata = {}
            columndata = []
            i = 0
            for country in selectedcountries:
                sum = 0
                for temp in data[i]:
                    sum = sum + float(temp)
                tempdata = {"label": country, "y": sum}
                columndata.append(tempdata)
                i += 1
            # print("Bar Data : ", bardata)
            return render(request, 'usercolumnchart.html', {"columndata": columndata})
        elif (graphtype == 'PieChart'):
            tempdata = {}
            piedata = []
            i = 0
            for country in selectedcountries:
                sum = 0
                for temp in data[i]:
                    sum = sum + float(temp)
                tempdata = {"label": country, "y": sum}
                piedata.append(tempdata)
                i += 1
            return render(request, 'userpiechart.html', {"pie_data": piedata})
        elif (graphtype == 'LineChart'):
            tempdata = {}
            linedata = []
            i = 0
            for country in selectedcountries:
                sum = 0
                for temp in data[i]:
                    sum = sum + float(temp)
                tempdata = {"label": country, "y": sum}
                linedata.append(tempdata)
                i += 1
            return render(request, 'userlinechart.html', {"linedata": linedata})
        elif (graphtype == 'DoughnutChart'):
            tempdata = {}
            doughnutdata = []
            i = 0
            for country in selectedcountries:
                sum = 0
                for temp in data[i]:
                    sum = sum + float(temp)
                tempdata = {"label": country, "y": sum}
                doughnutdata.append(tempdata)
                i += 1
            return render(request, 'userdoughnutchart.html', {"doughnut_data": doughnutdata})
        elif (graphtype == 'AreaChart'):
            tempdata = {}
            areadata = []
            i = 0
            for country in selectedcountries:
                sum = 0
                for temp in data[i]:
                    sum = sum + float(temp)
                tempdata = {"label": country, "y": sum}
                areadata.append(tempdata)
                i += 1
        return render(request, 'userareachart.html', {"areadata": areadata})

    return render(request, 'usermainpage.html', {'response': response, 'headings': headings, 'data': data})

"""
def usershowchart(request):
    print("User Show Chart")
    if request.method == 'POST':
        graphtype = request.POST.get('graphtype')
        selectedcolumns = request.POST.getlist('column')
        selectedcountries = request.POST.getlist('country')
        print("Graph Type : ", graphtype)
        print("Selected Columns : ", selectedcolumns)
        print("Selected Countries : ", selectedcountries)
        doc = request.FILES  # returns a dict-like object
        doc_name = doc['file']
        print("File name : ", doc_name)
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')
        print("Data Set : ", data_set)
        data = data_set.split("\r")
        tabledata = []
        for row in data:
            temp = row.split(",")
            temprow = []
            i=0
            flag=True
            for data in temp:
                temprow.append(data.replace("\n", ""))
                if(i!=0 and not data.isnumeric()):
                    flag=False
                    break
            if(flag):
                tabledata.append(temprow)

        columns = []
        data = []

        for i in range(1, len(tabledata) - 1):
            temp = tabledata[i][0]
            columns.append(temp.replace("\n", ""))
            data.append(tabledata[i])

        collength = len(tabledata[0])
        rowlength = len(tabledata)
        print("Column Length : ", collength, " Row Length : ", rowlength)
        print("Columns : ", columns)
        matrixdata=[]
        for j in range(0, collength):
            temp=[]
            for i in range(0, rowlength-1):
                temp.append(tabledata[i][j])
            matrixdata.append(temp)

        matrixdata2=[]
        matrixdata2.append(matrixdata[0])
        for i in range(1, len(matrixdata)):
            flag=True
            for j in range(1, len(matrixdata[i])):
                if (not isfloat(matrixdata[i][j])):
                    flag=False
                    break
            if(flag):
                matrixdata2.append(matrixdata[i])
        print("Matrix Data2 : ", matrixdata2)
        matrixdata=matrixdata2
        matrixdata1 = matrixdata[1:]
        matrixdata2=[]
        for row in matrixdata1:
            temp = row[0].replace("\n", "")
            if temp in selectedcolumns:
                matrixdata2.append(row)


        collength = len(matrixdata2[0])
        rowlength = len(matrixdata2)

        matrixdata3=[]
        for j in range(0, collength):
            temp=[]
            for i in range(0, rowlength):
                temp.append(matrixdata2[i][j])
            matrixdata3.append(temp)

        headings = tabledata[0]
        countrynames = matrixdata[0]
        print("Headings      : ", headings)
        print("Country Names : ", countrynames)

        collength = len(matrixdata3)
        rowlength = len(countrynames)

        matrixdata4=[]
        for i in range(0,len(countrynames)):
            temp=[]
            temp.append(countrynames[i])
            for j in range(0,len(matrixdata3[0])):
                temp.append(matrixdata3[i][j])
            matrixdata4.append(temp)

        matrixdata5 = []
        for i in range(1,len(matrixdata4)):
            temp = matrixdata4[i][0]
            if(temp in selectedcountries):
                matrixdata5.append(matrixdata4[i])
        headings=[]
        for row in matrixdata5:
            headings.append(row[0])
        if(graphtype=="BarChart"):
            tempheading=tabledata[0]
            bardata1=[]
            numberdata=[]
            for row in matrixdata5:
                tempdata=row[1:]
                numberdata.append(tempdata)
            bardata = []
            for row in matrixdata5:
                sum = 0
                label = row[0].replace("\n", "")
                if label in selectedcountries:
                    for i in range(1, len(row)):
                        sum = sum + int(row[i])
                    tempdata = {"label": label, "y": sum}
                    bardata.append(tempdata)
            return render(request, 'userbarchart.html', {"bardata": bardata})
        elif (graphtype == "ColumnChart"):
            columndata=[]
            for row in matrixdata5:
                sum = 0
                label = row[0].replace("\n", "")
                if label in selectedcountries:
                    for i in range(1, len(row)):
                        sum = sum + int(row[i])
                    tempdata = {"label": label, "y": sum}
                    columndata.append(tempdata)
            return render(request, 'usercolumnchart.html', {"columndata": columndata})
        elif (graphtype == "PieChart"):
            piedata=[]
            for row in matrixdata5:
                sum = 0
                label = row[0].replace("\n", "")
                if label in selectedcountries:
                    for i in range(1, len(row)):
                        sum = sum + int(row[i])
                    tempdata = {"label": label, "y": sum}
                    piedata.append(tempdata)
            return render(request, 'userpiechart.html', {"pie_data": piedata})
        elif (graphtype == "LineChart"):
            linedata = []
            for row in matrixdata5:
                sum = 0
                label = row[0].replace("\n", "")
                if label in selectedcountries:
                    for i in range(1, len(row)):
                        sum = sum + int(row[i])
                    tempdata = {"label": label, "y": sum}
                    linedata.append(tempdata)
            print("Line Data : ",linedata)
            return render(request, 'userlinechart.html', {"linedata": linedata})
        elif (graphtype == "DounutChart"):
            doughnutdata = []
            for row in matrixdata5:
                sum = 0
                label = row[0].replace("\n", "")
                if label in selectedcountries:
                    for i in range(1, len(row)):
                        sum = sum + int(row[i])
                    tempdata = {"label": label, "y": sum}
                    doughnutdata.append(tempdata)
            return render(request, 'userdoughnutchart.html', {"doughnut_data": doughnutdata})
        elif (graphtype == "AreaChart"):

            #print("Data : ", data)
            areadata = []
            for row in matrixdata5:
                sum = 0
                label = row[0].replace("\n", "")
                if label in selectedcountries:
                    for i in range(1, len(row)):
                        sum = sum + int(row[i])
                    tempdata = {"label": label, "y": sum}
                    areadata.append(tempdata)
            return render(request, 'userareachart.html', {"areadata": areadata})
    response=""
    headings=""
    data=""
    return render(request, 'usermainpage.html', {'response': response, 'headings': headings, 'data': data})
"""
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def adminmainpage(request):
    response="Upload Excel Page"
    headings=[]
    headings1=[]
    columns=[]
    tabledata=[]
    if request.method == 'POST':
        print("Uploading Excel Page")
        response = "Uploading Excel Page"
        doc = request.FILES  # returns a dict-like object
        print("Document : ", doc)
        doc_name = doc['file']
        print("File name : ", doc_name)        
        #request.session['filename'] = doc_name
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')
        print("Data Set : \n", data_set)
        #data =data_set.split("\r")
        data = re.split(r'\r|\n', data_set)

        data1 = []
        for row in data:
            if (len(row) > 2):
                data1.append(row)

        for row in data1:
            print(row)

        matrixdata = []
        for row in data1:
            temp = row.split(",")
            temprow = []
            for value in temp:
                temprow.append(value)
            matrixdata.append(temprow)

        print("Matrix Data : ")
        for row in matrixdata:
            print(row)

        rows = len(matrixdata)
        cols = len(matrixdata[0])

        transposedmatrix = []
        print("Transposed Matrix : ")
        for c in range(0, cols):
            temprow = []
            for r in range(0, rows):
                temprow.append(matrixdata[r][c])
            transposedmatrix.append(temprow)

        print("\nTransposed Matrix Data : ")
        for row in transposedmatrix:
            print(row)

        matrixdata1 = transposedmatrix[1:]
        matrixdata2 = []
        for temp in matrixdata1:
            temprow = []
            i = 0
            flag = True
            for data1 in temp:
                temprow.append(data1.replace("\n", ""))
                if (i != 0):
                    if (not isfloat(data1)):
                        print("Non Numeric Value : ", data1)
                        flag = False
                        break
                i += 1
            if(flag):
                matrixdata2.append(temprow)

        print("\nTransposed Matrix Data : ")
        for row in matrixdata2:
            print(row)

        rows = len(matrixdata2)
        cols = len(matrixdata2[0])

        matrixdata3 = []
        for c in range(0, cols):
            temprow = []
            for r in range(0, rows):
                temprow.append(matrixdata2[r][c])
            matrixdata3.append(temprow)

        headings=transposedmatrix[0]
        columns=matrixdata3[0]

        print("Headings : ", headings)
        print("Columns  : ", columns)

        tabledata=[]
        r=0
        for data in headings:
            temprow=[]
            temprow.append(data)
            for c in range(0,len(matrixdata3[0])):
                temprow.append(matrixdata3[r][c])
            tabledata.append(temprow)
            r+=1

        columns=[]
        for i in range(1, len(tabledata)):
            columns.append(tabledata[i][0])

        for i in range(1, len(tabledata)):
            columns.append(tabledata[i][0])

        headings = tabledata[0]
        headings1 = headings[1:]
        tabledata = tabledata[1:]

    return render(request, 'adminmainpage.html',{'response':response, 'headings':headings,
                                                 'headings1': headings1,'columns':columns,'data':tabledata})

def usermainpage(request):
    response="Upload Excel Page"
    headings=[]
    headings1=[]
    columns=[]
    tabledata=[]
    if request.method == 'POST':
        print("Uploading Excel Page")
        response = "Uploading Excel Page"
        doc = request.FILES  # returns a dict-like object
        print("Document : ", doc)
        doc_name = doc['file']
        print("File name : ", doc_name)
        request.session['filename'] = doc_name
        #session["filename"]=doc_name
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        data_set = csv_file.read().decode('UTF-8')
        print("Data Set : \n", data_set)
        #data =data_set.split("\r")
        data = re.split(r'\r|\n', data_set)

        data1 = []
        for row in data:
            if (len(row) > 2):
                data1.append(row)

        for row in data1:
            print(row)

        matrixdata = []
        for row in data1:
            temp = row.split(",")
            temprow = []
            for value in temp:
                temprow.append(value)
            matrixdata.append(temprow)

        print("Matrix Data : ")
        for row in matrixdata:
            print(row)

        rows = len(matrixdata)
        cols = len(matrixdata[0])

        transposedmatrix = []
        print("Transposed Matrix : ")
        for c in range(0, cols):
            temprow = []
            for r in range(0, rows):
                temprow.append(matrixdata[r][c])
            transposedmatrix.append(temprow)

        print("\nTransposed Matrix Data : ")
        for row in transposedmatrix:
            print(row)

        matrixdata1 = transposedmatrix[1:]
        matrixdata2 = []
        for temp in matrixdata1:
            temprow = []
            i = 0
            flag = True
            for data1 in temp:
                temprow.append(data1.replace("\n", ""))
                if (i != 0):
                    if (not isfloat(data1)):
                        print("Non Numeric Value : ", data1)
                        flag = False
                        break
                i += 1
            if(flag):
                matrixdata2.append(temprow)

        print("\nTransposed Matrix Data : ")
        for row in matrixdata2:
            print(row)

        rows = len(matrixdata2)
        cols = len(matrixdata2[0])

        matrixdata3 = []
        for c in range(0, cols):
            temprow = []
            for r in range(0, rows):
                temprow.append(matrixdata2[r][c])
            matrixdata3.append(temprow)

        headings=transposedmatrix[0]
        columns=matrixdata3[0]

        print("Headings : ", headings)
        print("Columns  : ", columns)

        tabledata=[]
        r=0
        for data in headings:
            temprow=[]
            temprow.append(data)
            for c in range(0,len(matrixdata3[0])):
                temprow.append(matrixdata3[r][c])
            tabledata.append(temprow)
            r+=1

        columns=[]
        for i in range(1, len(tabledata)):
            columns.append(tabledata[i][0])

        for i in range(1, len(tabledata)):
            columns.append(tabledata[i][0])

        headings = tabledata[0]
        headings1 = headings[1:]
        tabledata = tabledata[1:]

    return render(request, 'usermainpage.html',{'response':response, 'headings':headings,
                                                 'headings1': headings1,'columns':columns,'data':tabledata})

def contact(request):
    return render(request, 'contact.html')

def barchart(request):
    datapoints = [
        {"x": 10, "y": 171},
        {"x": 20, "y": 155},
        {"x": 30, "y": 150},
        {"x": 40, "y": 165},
        {"x": 50, "y": 195},
        {"x": 60, "y": 168},
        {"x": 70, "y": 128},
        {"x": 80, "y": 134},
        {"x": 90, "y": 114}
    ]
    datapoints2 = [
        {"x": 10, "y": 71},
        {"x": 20, "y": 55},
        {"x": 30, "y": 50},
        {"x": 40, "y": 65},
        {"x": 50, "y": 95},
        {"x": 60, "y": 68},
        {"x": 70, "y": 28},
        {"x": 80, "y": 34},
        {"x": 90, "y": 14}
    ]
    datapoints3 = [
        {"x": 10, "y": 71},
        {"x": 20, "y": 55},
        {"x": 30, "y": 50},
        {"x": 40, "y": 65},
        {"x": 50, "y": 95},
        {"x": 60, "y": 68},
        {"x": 70, "y": 28},
        {"x": 80, "y": 34},
        {"x": 90, "y": 14}
    ]
    return render(request, 'barchart.html', {"datapoints": datapoints, "datapoints2": datapoints2,
                                             "datapoints3": datapoints3})

def piechart(request):
    monthly_expense_data = [
        {"label": "Accomodation", "y": 30},
        {"label": "Food & Groceries", "y": 25},
        {"label": "Utilities", "y": 5},
        {"label": "Entertainment & Fun", "y": 20},
        {"label": "Savings", "y": 10},
        {"label": "Cellphone & Internet", "y": 10}
    ]
    return render(request, 'piechart.html', {"monthly_expense_data": monthly_expense_data})


def doughnutchart(request):
    magma_composition_data = [
        {"label": "Oxygen", "symbol": "O", "y": 46.6},
        {"label": "Silicon", "symbol": "Si", "y": 27.7},
        {"label": "Aluminium", "symbol": "Al", "y": 13.9},
        {"label": "Iron", "symbol": "Fe", "y": 5},
        {"label": "Calcium", "symbol": "Ca", "y": 3.6},
        {"label": "Sodium", "symbol": "Na", "y": 2.6},
        {"label": "Magnesium", "symbol": "Mg", "y": 2.1},
        {"label": "Others", "symbol": "Others", "y": 1.5}
    ]
    return render(request, 'doughnutchart.html', {"magma_composition_data": magma_composition_data})

def linechart(request):
  china_life_expectancy = [
    { "label": "2000", "y": 71.397 },
    { "label": "2001", "y": 71.732 },
    { "label": "2002", "y": 72.061 },
    { "label": "2003", "y": 72.381 },
    { "label": "2004", "y": 72.689 },
    { "label": "2005", "y": 72.985 },
    { "label": "2006", "y": 73.271 },
    { "label": "2007", "y": 73.553 },
    { "label": "2008", "y": 73.835 },
    { "label": "2009", "y": 74.119 },
    { "label": "2010", "y": 74.409 },
    { "label": "2011", "y": 74.708 },
    { "label": "2012", "y": 75.013 },
    { "label": "2013", "y": 75.321 },
    { "label": "2014", "y": 75.629 },
    { "label": "2015", "y": 75.928 },
    { "label": "2016", "y": 76.21 },
    { "label": "2017", "y": 76.47 },
    { "label": "2018", "y": 76.704 },
    { "label": "2019", "y": 76.912 },
    { "label": "2020", "y": 77.097 }
  ]
  brazil_life_expectancy = [
    { "label": "2000", "y": 70.116 },
    { "label": "2001", "y": 70.462 },
    { "label": "2002", "y": 70.813 },
    { "label": "2003", "y": 71.17 },
    { "label": "2004", "y": 71.531 },
    { "label": "2005", "y": 71.896 },
    { "label": "2006", "y": 72.26 },
    { "label": "2007", "y": 72.618 },
    { "label": "2008", "y": 72.966 },
    { "label": "2009", "y": 73.3 },
    { "label": "2010", "y": 73.619 },
    { "label": "2011", "y": 73.921 },
    { "label": "2012", "y": 74.209 },
    { "label": "2013", "y": 74.483 },
    { "label": "2014", "y": 74.745 },
    { "label": "2015", "y": 74.994 },
    { "label": "2016", "y": 75.23 },
    { "label": "2017", "y": 75.456 },
    { "label": "2018", "y": 75.672 },
    { "label": "2019", "y": 75.881 },
    { "label": "2020", "y": 76.084 }
  ]
  india_life_expectancy = [
    { "label": "2000", "y": 62.505 },
    { "label": "2001", "y": 62.907 },
    { "label": "2002", "y": 63.304 },
    { "label": "2003", "y": 63.699 },
    { "label": "2004", "y": 64.095 },
    { "label": "2005", "y": 64.5 },
    { "label": "2006", "y": 64.918 },
    { "label": "2007", "y": 65.35 },
    { "label": "2008", "y": 65.794 },
    { "label": "2009", "y": 66.244 },
    { "label": "2010", "y": 66.693 },
    { "label": "2011", "y": 67.13 },
    { "label": "2012", "y": 67.545 },
    { "label": "2013", "y": 67.931 },
    { "label": "2014", "y": 68.286 },
    { "label": "2015", "y": 68.607 },
    { "label": "2016", "y": 68.897 },
    { "label": "2017", "y": 69.165 },
    { "label": "2018", "y": 69.416 },
    { "label": "2019", "y": 69.656 },
    { "label": "2020", "y": 69.887 }
  ]
  japan_life_expectancy = [
    { "label": "2000", "y": 81.07609756 },
    { "label": "2001", "y": 81.41707317 },
    { "label": "2002", "y": 81.56341463 },
    { "label": "2003", "y": 81.76 },
    { "label": "2004", "y": 82.0302439 },
    { "label": "2005", "y": 81.92512195 },
    { "label": "2006", "y": 82.32195122 },
    { "label": "2007", "y": 82.50707317 },
    { "label": "2008", "y": 82.58756098 },
    { "label": "2009", "y": 82.93146341 },
    { "label": "2010", "y": 82.84268293 },
    { "label": "2011", "y": 82.59121951 },
    { "label": "2012", "y": 83.09609756 },
    { "label": "2013", "y": 83.33195122 },
    { "label": "2014", "y": 83.58780488 },
    { "label": "2015", "y": 83.79390244 },
    { "label": "2016", "y": 83.98487805 },
    { "label": "2017", "y": 84.0997561 },
    { "label": "2018", "y": 84.21097561 },
    { "label": "2019", "y": 84.35634146 },
    { "label": "2020", "y": 84.61560976 }
  ]
  return render(request, 'linechart.html', { "china_life_expectancy" : china_life_expectancy, "brazil_life_expectancy" : brazil_life_expectancy, "india_life_expectancy": india_life_expectancy, "japan_life_expectancy": japan_life_expectancy })

def scatterchart(request):
    vehicle_weight_fuel_economy_data = [
        {"x": 4.36, "y": 16.9},
        {"x": 4.054, "y": 15.5},
        {"x": 3.605, "y": 19.2},
        {"x": 3.94, "y": 18.5},
        {"x": 2.155, "y": 30},
        {"x": 2.56, "y": 27.5},
        {"x": 2.3, "y": 27.2},
        {"x": 2.23, "y": 30.9},
        {"x": 2.83, "y": 20.3},
        {"x": 3.14, "y": 19.5},
        {"x": 2.795, "y": 21.6},
        {"x": 3.41, "y": 16.2},
        {"x": 3.38, "y": 20.6},
        {"x": 3.07, "y": 20.8},
        {"x": 3.62, "y": 18.6},
        {"x": 3.41, "y": 18.1},
        {"x": 3.84, "y": 17},
        {"x": 3.725, "y": 17.6},
        {"x": 3.955, "y": 16.5},
        {"x": 3.83, "y": 18.2},
        {"x": 2.585, "y": 26.5},
        {"x": 2.91, "y": 21.9},
        {"x": 1.975, "y": 34.1},
        {"x": 1.915, "y": 35.1},
        {"x": 2.67, "y": 27.4},
        {"x": 1.99, "y": 31.5},
        {"x": 2.135, "y": 29.5},
        {"x": 2.67, "y": 28.4},
        {"x": 2.595, "y": 28.8},
        {"x": 2.7, "y": 26.8},
        {"x": 2.556, "y": 33.5},
        {"x": 2.2, "y": 34.2},
        {"x": 2.02, "y": 31.8},
        {"x": 2.13, "y": 37.3},
        {"x": 2.19, "y": 30.5},
        {"x": 2.815, "y": 22},
        {"x": 2.6, "y": 21.5}
    ]
    return render(request, 'areachart.html', {"vehicle_weight_fuel_economy_data": vehicle_weight_fuel_economy_data})

def passwordchangepage(request):
    print("Password Change Page")
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        userid=request.session['userid']
        NewUser.objects.filter(id=userid).update(password=pwd)
        print("Password Updated Success")
        return render(request, 'userlogin.html', {'msg': 'Password Updated Success'})
    return render(request, 'userlogin.html', {'msg': 'Password Not Updated'})

def userforgotpassword(request):
    flag = False
    if request.method == 'POST':
        uname = request.POST.get('uname')
        toemail = request.POST.get('email')
        print("User Name : ", uname, " EmailId : ", toemail)
        mydata = NewUser.objects.all()
        for data in mydata:
            if (data.username == uname and data.emailid == toemail):
                flag = True
                print("User Id : ", data.id)
                request.session['userid'] = data.id
                break
        if (flag == True):
            otp = random.randint(1000, 9999)
            print("OTP : ", otp)
            request.session['toemail'] = toemail
            request.session['uname'] = uname
            request.session['otp'] = otp
            print("User Id : ", request.session['userid'])
            return render(request, "generateotp.html", {'uname': uname, 'toemail': toemail, 'otp': otp,
                      'redirecturl': 'http://127.0.0.1:8000/enterotppage/'})
        else:
            context = {'msg': 'Invalid UserName/EmailId'}
            template = loader.get_template('userforgotpassword.html')
    else:
        template = loader.get_template('userforgotpassword.html')
        context = {'msg': ''}
    return HttpResponse(template.render(context, request))

def generateotppage(request):
    return render(request, "generateotp.html", {'uname': 'uname', 'toemail': 'toemail', 'otp': 'otp',
                                               'redirecturl': 'http://127.0.0.1:8000/userlogin/'})

def enterotppage(request):
    if request.method == 'POST':
        storedotp=request.session['otp']
        enteredotp = request.POST.get('otp')
        print("Entered OTP : ", enteredotp, " Stored OTP : ", storedotp)
        template = loader.get_template('passwordchangepage.html')
        if(int(storedotp)==int(enteredotp)):
            context = {'msg': ''}
            return HttpResponse(template.render(context, request))
        else:
            context = {'msg': ''}
            return render(request, "enterotppage.html",{'msg': 'Incorrect OTP'})
    return render(request, "enterotppage.html",{'msg': ''})