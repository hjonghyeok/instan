from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()

    def save_to_firebase(self):
        from firebase_admin import db
        ref = db.reference('users')  # 'users'라는 경로에 데이터를 저장
        ref.push({
            'name': self.name,
            'email': self.email,
            'age': self.age
        })

    def __str__(self):
        return self.name
