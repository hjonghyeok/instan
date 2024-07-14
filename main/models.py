from django.db import models

class Users(models.Model):
    user_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    
    def save_to_firebase(self):
        from firebase_admin import db
        ref = db.reference('users')  # 'users'라는 경로에 데이터를 저장
        ref.push({
            'user_name': self.user_name,
            'user_id': self.user_id,
            'password': self.password,
        })

    def __str__(self):
        return self.user_name
    
class Posts(models.Model):
    writer = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    contents = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    like = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.writer)