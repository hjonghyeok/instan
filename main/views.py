from django.shortcuts import render
from django.http import JsonResponse
from .models import User

def create_user(request):
    user = User(name="John Doe", email="john@example.com", age=30)
    user.save()
    user.save_to_firebase()
    return JsonResponse({'status': 'user created'})

def get_users(request):
    from firebase_admin import db
    ref = db.reference('users')
    users = ref.get()
    user_list = [{'name': user['name'], 'email': user['email'], 'age': user['age']} for user in users.values()]
    return JsonResponse(user_list, safe=False)
