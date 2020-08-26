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

def likert2target(internet):
    return {
        'sangat setuju': 10,
        'setuju': 8,
        'netral' : 6,
        'tidak setuju': 4,
        'sangat tidak setuju' : 2
    }[internet]



def index2(request):
    Upload_data = upload_data.objects.filter(id=108).values_list('isi')[0]
    Upload_data = Upload_data[0]
    dat = open(os.path.join(settings.MEDIA_ROOT, Upload_data))
    df = pd.read_csv(dat, delimiter=';', encoding='utf-8')
    df = df.dropna()
    df.columns = ['Date', 'nama', 'jurusan', 'semester', 'internet', 'alumni', 'media', 'beasiswa','kerja',
                  'belajar']
    df_semester = df.groupby(['semester']).size().reset_index(name='value')
    nama_semester=df_semester.semester.tolist()
    jml_semester=df_semester.value.tolist()
    df_jurusan = df.groupby(['jurusan']).size().reset_index(name='value')
    nama_jurusan=df_jurusan.jurusan.tolist()
    jml_jurusan=df_jurusan.value.tolist()
    IT=df_jurusan.loc[df_jurusan['jurusan']=='Informatika']
    if IT.empty:
        jml_it=0
    else:
        jml_it=IT.iloc[0]['value']
        pass
    
    sipil=df_jurusan.loc[df_jurusan['jurusan']=='Sipil']
    if sipil.empty:
        jml_sipil=0
    else:
        jml_sipil=sipil.iloc[0]['value']
    
    arsitek=df_jurusan.loc[df_jurusan['jurusan']=='Arsitek']
    if arsitek.empty:
        jml_arsitek=0
    else:
        jml_arsitek=arsitek.iloc[0]['value']
    
    elektro=df_jurusan.loc[df_jurusan['jurusan']=='Elektro']
    if elektro.empty:
        jml_elektro=0
    else:
        jml_elektro=elektro.iloc[0]['value']
    
    mesin=df_jurusan.loc[df_jurusan['jurusan']=='Mesin']
    if mesin.empty:
        jml_mesin=0
    else:
        jml_mesin=mesin.iloc[0]['value']
    

    
    le = LabelEncoder()
    df_encoded = df.apply(le.fit_transform)
    df_encoded
    X = np.array(df_encoded)

    k = 3
    model = k_medoids(k)
    df_count = len(df.index)
    # print('Centers found by your model:')
    
    model.fit(X)
    m = model.fit(X)

    df_semester = df.groupby(['semester']).size().reset_index(name='value')
    nama_semester = df_semester.semester.tolist()
    jml_semester = df_semester.value.tolist()
    context={
        'jml_jurusan':jml_jurusan,
        'nama_jurusan':nama_jurusan,
        'jml_semester':jml_semester,
        'nama_semester':nama_semester,
        'jml_it':jml_it,
        'jml_sipil':jml_sipil,
        'jml_mesin':jml_mesin,
        'jml_eletro':jml_elektro,
        'jml_arsitek':jml_arsitek,
        'total':df_count,
        'nama_semester':nama_semester,
        'jml_semester': jml_semester,

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
            return redirect('index2')
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
    df.columns = ['Date', 'nama', 'jurusan', 'semester', 'internet', 'alumni', 'media', 'beasiswa','kerja',
                  'belajar']
    context = {'columns': df.columns, 'rows': df.to_dict('records'), 'Upload_data': Upload_data}
    return render(request, 'data.html', context)


def cluster_list(request):
    Upload_data = upload_data.objects.filter(id=108).values_list('isi')[0]
    Upload_data = Upload_data[0]
    dat = open(os.path.join(settings.MEDIA_ROOT, Upload_data))
    df = pd.read_csv(dat, delimiter=';', encoding='utf-8')
    df = df.dropna()
    df.columns = ['Date', 'nama', 'jurusan', 'semester', 'internet', 'alumni', 'media', 'beasiswa','kerja',
                  'belajar']
    df=df.apply(lambda x: x.astype(str).str.lower())
    #le = LabelEncoder()
    #df_encoded = df.apply(le.fit_transform)
    #df_encoded
    internet = df.internet.apply(likert2target)
    alumni = df.alumni.apply(likert2target)
    media = df.media.apply(likert2target)
    beasiswa = df.beasiswa.apply(likert2target)
    kerja = df.kerja.apply(likert2target)
    belajar = df.belajar.apply(likert2target)
    #X = np.array(df_encoded)
    df_en=pd.DataFrame(zip(internet, alumni, media,beasiswa,kerja,belajar))
    X = np.array(df_en)
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
    #baca data
    Upload_data = upload_data.objects.filter(id=108).values_list('isi')[0]
    Upload_data = Upload_data[0]
    dat = open(os.path.join(settings.MEDIA_ROOT, Upload_data))
    df = pd.read_csv(dat, delimiter=';', encoding='utf-8')
    df = df.dropna()
    df.columns = ['Date', 'nama', 'jurusan', 'semester', 'internet', 'alumni', 'media', 'beasiswa','kerja',
                  'belajar']
    df=df.apply(lambda x: x.astype(str).str.lower())
    #proses encode
    le = LabelEncoder()
    df_encoded = df.apply(le.fit_transform)
    df_encoded
    nama= df_encoded.nama
    jurusan=df_encoded.jurusan
    semester=df_encoded.semester
    internet = df.internet.apply(likert2target)
    alumni = df.alumni.apply(likert2target)
    media = df.media.apply(likert2target)
    beasiswa = df.beasiswa.apply(likert2target)
    kerja = df.kerja.apply(likert2target)
    belajar = df.belajar.apply(likert2target)
    ind=df.index
    X = np.array(df_encoded)
    df_en=pd.DataFrame(zip(nama,jurusan,semester,internet, alumni, media,beasiswa,kerja,belajar))
    X = np.array(X)
    #kmedoids
    k = 4
    model = k_medoids(k)
    # print('Centers found by your model:')
    model.fit(X)

    pred = model.predict(X)
    m = model.fit(X)
    # gambar(X, pred)
    X = X.tolist()
    pred = pred.tolist()
    mahasiswa = df.values.tolist()
    
    
    #u=[]
    #dd1f.columns = ['ind','inde','a','b','c','d','e','f','g','h','i']
    #for j in dd1f.inde:
    #    for i in df.index:
    #        if  i==j:
    #            u.append(df.nama[i])
    #dd1f['nama']=u
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
        'rows': df_decoded.to_dict('records'),
        #'u':u
    }
    return render(request, 'visual.html', context)
