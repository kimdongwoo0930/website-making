from django import forms
from .models import user
from django.contrib.auth.hashers import check_password

class Loginform(forms.Form):
    username =forms.CharField(
        error_messages={
            'required':  '아이디를 입력해주세요' 
        },
        max_length=32, label="사용자 이름")
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요'
        }
        ,label="비밀번호", widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            try:
                User = user.objects.get(username = username)
            except user.DoesNotExist:
                self.add_error("username",'아이디가 없습니다')
                return

            if not check_password(password,User.password):
                self.add_error("password",'비밀번호를 틀렸습니다.')
            else:
                self.User_id = User.id
