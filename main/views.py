from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import auth

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
    return render(request, 'main.html')

def logout(request):
    auth.logout(request)
    return redirect('/')