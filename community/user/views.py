from django.shortcuts import render , redirect
from .models import user
from django.contrib.auth.hashers import make_password , check_password
from django.http import HttpResponse
from .forms import Loginform


def home(request):
        
    return render(request,'home.html')

def logout(request):
    if request.session.get('user'):
        del(request.session['user'])
    
    return redirect("/")

def login(request):
    if request.method == "POST":
        form = Loginform(request.POST)
        if form.is_valid():
            request.session['user'] = form.User_id
            return redirect("/")
    else:
        form = Loginform()
    
    return render(request, "login.html", {'form':  form})

# Create your views here.
def register(request):
    if request.method == 'GET':
        return render(request, "register.html")
    elif request.method == "POST":
        username = request.POST.get('username',None)
        useremail = request.POST.get('useremail',None)
        password = request.POST.get('password',None)
        re_password = request.POST.get("re-password",None)

        res_data = {}

        if not (username and password and re_password and useremail):
            res_data['error'] = '모든 값을 입력해야합니다'
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
        else:
            User = user(
                username=username,
                password=make_password(password),
                useremail = useremail
            )
            User.save()


        return render(request, "register.html",res_data)