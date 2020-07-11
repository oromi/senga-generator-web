from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
import cv2
import numpy as np
import sys
import os
import time
import shutil
from django.conf import settings

def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = DocumentForm()
        max_id = Document.objects.latest('id').id
        obj = Document.objects.get(id = max_id)
        input_path = settings.BASE_DIR +  obj.photo.url # obj.photo.url
        rename(input_path)

        input_path = settings.BASE_DIR +  "./tmp/documents/input.jpg"
        output_path = settings.BASE_DIR + "/tmp/output/output.jpg"
        senga(input_path)

    return render(request, 'app1/index.html', {
        'form': form,
        'obj':obj,
    })

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

def rename(input):
    if not os.path.exists(input) :
        input =  settings.BASE_DIR + "./tmp/documents/sample.jpg"
        return 0
    shutil.copy(input, "./tmp/documents/input.jpg")
    dest =  "./tmp/documents/input.jpg"
    os.remove(input)

def senga(input):
    neighbourhood = np.array([[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1],[1,1,1,1,1,1]],np.uint8) #24
    gray = imread("./tmp/documents/input.jpg", cv2.IMREAD_GRAYSCALE)
    dilated = cv2.dilate(gray, neighbourhood, iterations= 1)
    out = cv2.absdiff(dilated, gray)
    inv = 255 - out
    imwrite("./tmp/output/output.jpg", inv)

