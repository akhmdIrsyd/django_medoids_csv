from django.db import models
import os
from uuid import uuid4
# Create your models here.


def path_and_rename(instance, filename):
    upload_to = 'data'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class upload_data(models.Model):
    isi = models.FileField(upload_to='documents/')

JK_choice=[
    ('laki','Laki-Laki'),
    ('perempuan','perempuan')
]
class mahasiswa(models.Model):
    nama = models.CharField(max_length=50)
    jurusan = models.CharField(max_length=30)
    JK = models.CharField(max_length=30)
    asal = models.CharField(max_length=30)
    semester = models.CharField(max_length=30)
    info = models.CharField(max_length=30)
    dorongan = models.CharField(max_length=30)
    alasan = models.CharField(max_length=30)
    pendapat = models.CharField(max_length=30)
    peluang = models.CharField(max_length=30)
    

