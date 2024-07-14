from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import auth
from .forms import ImageUploadForm
import firebase_admin
from firebase_admin import storage
from django.core.files.storage import default_storage
import os
import PIL
import uuid


def login_page(request):
    if request.method == "POST":
        res_data = {}
        user_id = request.POST.get('id', None)
        password = request.POST.get('pw', None)
        id_check = ""
        try:
            id_check = Users.objects.get(user_id = user_id)
        except Users.DoesNotExist:
            pass
        
        if not id_check:
            res_data['error'] = '없는 아이디입니다.'
            return render(request, 'login.html', res_data)
        
        if not check_password(password, id_check.password):
            res_data['error'] = '비밀번호가 틀렸습니다.'
            return render(request, 'login.html', res_data)
        else:
            request.session['user'] = id_check.user_id
            return redirect('/')
        
    return render(request, 'login.html')

def register_page(request):
    if request.method == "POST":
        res_data = {}
        user_name = request.POST.get('username', None)
        user_id = request.POST.get('id', None)
        password = request.POST.get('pw', None)
        password_check = request.POST.get('pw_check', None)
        id_check = ""
        try:
            id_check = Users.objects.get(user_id = user_id)
        except Users.DoesNotExist:
            pass
        if id_check:
            res_data['error'] = "이미 존재하는 아이디입니다."
            return render(request, 'register.html', res_data)
        if password == password_check:
            user = Users(
                user_name = user_name,
                user_id = user_id,
                password = make_password(password)
            )
            user.save()
            user.save_to_firebase()
            return redirect('/login')
        else:

            res_data['error'] = '비밀번호가 일치하지 않습니다.'
            return render(request, 'register.html', res_data)
    
    return render(request, 'register.html')

def main_page(request):
    try:
        user = request.session['user']
    except:
        return redirect('/login')
    posts = Posts.objects.all().order_by('-id')
    content = {}
    content['post'] = posts
    print(posts)
    return render(request, 'home.html', content)

def logout(request):
    auth.logout(request)
    return redirect('/')

def post_page(request):
    if request.method == 'POST':
        user_id = request.session['user']
        user = Users.objects.get(user_id=user_id)
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            random_name = f"{uuid.uuid1()}{os.path.splitext(image.name)[1]}"
            # 로컬 파일 시스템에 이미지를 저장
            file_name = default_storage.save(random_name, image)
            file_path = default_storage.path(file_name)

            # Firebase Storage에 업로드
            bucket = storage.bucket()
            blob = bucket.blob(random_name)
            blob.upload_from_filename(file_path)

            # 이미지 URL 가져오기
            image_url = blob.public_url

            # 데이터베이스에 이미지 정보 저장
            uploaded_image = Posts(writer=user, contents=request.POST.get('comment'), image=file_name)
            uploaded_image.save()

            # 로컬에 저장된 파일 삭제
            os.remove(file_path)

            return redirect('/')
    
    else:
        form = ImageUploadForm()
        user_id = request.session['user']
        user = Users.objects.get(user_id=user_id)
        content = {
            'form' : form,
            'user' : user
        }
    
    return render(request, 'post.html', content)