from django.shortcuts import render, redirect
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
from .k_medoids import k_medoids
import json
from django.template.loader import render_to_string
# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View


from django.contrib.auth import authenticate, login
from .forms import Upload_dataForm
from .models import upload_data

import os
from django.conf import settings


def index2(request):
    Upload_data = upload_data.objects.filter(id=108).values_list('isi')[0]
    Upload_data = Upload_data[0]
    dat = open(os.path.join(settings.MEDIA_ROOT, Upload_data))
    df = pd.read_csv(dat, delimiter=';', encoding='utf-8')
    df = df.dropna()
    df.columns = ['Date', 'nama', 'kelamin', 'asal', 'jurusan', 'semester', 'info', 'dorogan', 'alasan', 'pendapat',
                  'peluang']
    
    df_jurusan = df.groupby(['jurusan']).size().reset_index(name='value')
    nama_jurusan=df_jurusan.jurusan.tolist()
    jml_jurusan=df_jurusan.value.tolist()

    df_JK = df.groupby(['kelamin']).size().reset_index(name='value')
    nama_JK = df_JK.kelamin.tolist()
    jml_JK = df_JK.value.tolist()
    le = LabelEncoder()
    df_encoded = df.apply(le.fit_transform)
    df_encoded
    X = np.array(df_encoded)

    k = 3
    model = k_medoids(k)
    # print('Centers found by your model:')
    
    model.fit(X)
    m = model.fit(X)
    context={
        'nama_JK':nama_JK,
        'jml_JK': jml_JK,
        'jml_jurusan':jml_jurusan,
        'nama_jurusan':nama_jurusan
    }
    return render(request, 'home2.html', context )

def model_form_upload(request):
    if request.method == 'POST':
        form = Upload_dataForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('data')
    else:
        form = Upload_dataForm()
    return render(request, 'upload_form.html', {
        'form': form
    })

def update(request, id):
    upload_datas = upload_data.objects.get(id=id)
    
    if request.method == 'POST':
        form = Upload_dataForm(request.POST, request.FILES, instance=upload_datas)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = Upload_dataForm(instance=upload_datas)
        return render(request, 'upload_form.html', {'form': form})

   

def data_list(request):
    Upload_data = upload_data.objects.all()
    Upload_data1 = upload_data.objects.filter(id=108).values_list('isi')[0]
    Upload_data1 = Upload_data1[0]
    dat = open(os.path.join(settings.MEDIA_ROOT, Upload_data1))
    df = pd.read_csv(dat, delimiter=';', encoding='utf-8')
    df = df.dropna()
    df.columns = ['Date', 'nama', 'kelamin', 'asal', 'jurusan', 'semester', 'info', 'dorogan', 'alasan', 'pendapat',
                  'peluang']
    context = {'columns': df.columns, 'rows': df.to_dict('records'), 'Upload_data': Upload_data}
    return render(request, 'data.html', context)


def cluster_list(request):
    Upload_data = upload_data.objects.filter(id=108).values_list('isi')[0]
    Upload_data = Upload_data[0]
    dat = open(os.path.join(settings.MEDIA_ROOT, Upload_data))
    df = pd.read_csv(dat, delimiter=';', encoding='utf-8')
    df = df.dropna()
    df.columns = ['Date', 'nama', 'kelamin', 'asal', 'jurusan', 'semester', 'info', 'dorogan', 'alasan', 'pendapat',
                  'peluang']

    le = LabelEncoder()
    df_encoded = df.apply(le.fit_transform)
    df_encoded
    X = np.array(df_encoded)

    k = 3
    model = k_medoids(k)
    # print('Centers found by your model:')
    model.fit(X)

    pred = model.predict(X)
    # gambar(X, pred)
    X = X.tolist()
    pred = pred.tolist()
    mahasiswa = df.values.tolist()
    df['pred']=pred
    context = {
        'columns': df.columns, 
        'rows': df.to_dict('records'),
        'Upload_data': Upload_data,
        'test': df,
        'mahasiswa': mahasiswa,
        'data': X,
        'cluster': pred,
        'hello': 'hello world'
    }
    return render(request, 'cluster.html', context)


#def data_list(request):
#    Upload_data = upload_data.objects.all()
#    return render(request, 'data.html', {'Upload_data': Upload_data})


def login(request):
    return render(request, 'login.html', {})

def gambar(X, label):
    x1 = []
    K = np.amax(label) + 1
    for i in range(K):
        x1.append(i)
        x1[i] = X[label == i, :]

    # you can fix this dpi
    # print(K)
    plt.figure(dpi=120)
    colors = ['b^', 'go', 'rs', 'd']
    # print('koor')

    for i in range(len(x1)):
        plt.plot(x1[i][:, 0], x1[i][:, 1], colors[i], markersize=4, alpha=.8)

    plt.axis('equal')
    plt.plot()
    plt.show()

def visual(request):
    Upload_data = upload_data.objects.filter(id=108).values_list('isi')[0]
    Upload_data = Upload_data[0]
    dat = open(os.path.join(settings.MEDIA_ROOT, Upload_data))
    df = pd.read_csv(dat, delimiter=';', encoding='utf-8')
    df = df.dropna()
    df.columns = ['Date', 'nama', 'kelamin', 'asal', 'jurusan', 'semester', 'info', 'dorogan', 'alasan', 'pendapat',
                  'peluang']
    list(df.columns.values)
    sentiment_counts = df.jurusan.value_counts()

    le = LabelEncoder()
    df_encoded = df.apply(le.fit_transform)
    df_encoded
    X = np.array(df_encoded)

    k = 3
    model = k_medoids(k)
    # print('Centers found by your model:')
    model.fit(X)

    pred = model.predict(X)
    m = model.fit(X)
    # gambar(X, pred)
    X = X.tolist()
    pred = pred.tolist()
    mahasiswa = df.values.tolist()
    
    

    dd1f = pd.DataFrame(m).reset_index()


    del dd1f['index']
    dd1f.columns = df.columns
    df_decoded = pd.DataFrame(columns=df.columns)

    for col in df.columns:
        le = le.fit(df[col])
        df_decoded[col] = le.inverse_transform(dd1f[col])
    
    context = {
        'test' : df,
        'mahasiswa' : mahasiswa,
        'data' : X,
        'cluster' : pred,
        'hello' : 'hello world',
        'columns': df_decoded.columns,
        'rows': df_decoded.to_dict('records')
    }
    return render(request, 'visual.html', context)
