from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from account.models import Register
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request,"home.html")

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("account:dashboard")

        else:
            return render(request,"login.html",{"status":"Please enter valid username and password."})


    return render(request,"login.html")

def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        address = request.POST["address"]
        user_types = request.POST["type"]

        if "profile" in request.FILES:
            profile_pic = request.FILES["profile"]

        if password == confirm_password:
            objects = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            objects.save()
            create_account = Register(user=objects,address=address,user_type=user_types,profile_pic=profile_pic)
            create_account.save()
            return render(request,"register.html",{"status":"Registration success.. Please login to view your dashboard."})
        else:
            return render(request,"register.html",{"status":"Password does not match..."})

    return render(request,"register.html")

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        id = request.user.id
        detail = Register.objects.get(user__id=id)
        
    return render(request,"dashboard.html",{"data":detail})

def logout(request):
    auth.logout(request)
    return redirect("/")
