from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from account.models import Register,Blog,Appointment
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
            if user_types == "doctor":
                objects.is_staff = True
            objects.save()
            create_account = Register(user=objects,address=address,user_type=user_types,profile_pic=profile_pic)
            create_account.save()
            return render(request,"register.html",{"status":"Registration success.. Please login to view your dashboard."})
        else:
            return render(request,"register.html",{"status":"Password does not match..."})

    return render(request,"register.html")

@login_required
def dashboard(request):
    return render(request,"dashboard.html")

def logout(request):
    auth.logout(request)
    return redirect("/")


@login_required
def profile(request):
    if request.user.is_authenticated:
        id = request.user.id
        detail = Register.objects.get(user__id=id)
    return render(request,"profile.html",{"data":detail})

@login_required
def create_blog(request):
    if request.method == "POST":
        title = request.POST["title"]
        if request.FILES:
            image = request.FILES["image"]
        category = request.POST["category"]
        summary = request.POST["summary"]
        content = request.POST["content"]
        draft = request.POST["draft"]
        doctor_id = User.objects.get(id=request.user.id)
        create_blog = Blog.objects.create(title=title,image=image,category=category,summary=summary,content=content,draft=draft,doctor_id=doctor_id)
        create_blog.save()
        return render(request,"create_blog.html",{"status":"Blog created successfully.."})
    return render(request,"create_blog.html")

@login_required
def my_blog(request):
    if request.user.is_authenticated:
        my_blog = Blog.objects.filter(doctor_id=request.user.id)
    return render(request,"my_blog.html",{"data":my_blog})

@login_required
def read_full_article(request,id):
    full_data = Blog.objects.get(id=id)
    data={
        "full_data":full_data,
    }
    return render(request,"read_full_article.html",data)

@login_required
def all_blog(request):
    publish_post = Blog.objects.filter(draft="Published")
    data = {
        "publish_post":publish_post
    }
    return render(request,"all_blog.html",data)

@login_required
def all_doctor_detail(request):
    doctor_detail = Register.objects.filter(user__is_staff=True)
    return render(request,"doctor_detail.html",{"data":doctor_detail})

@login_required
def book_appointment(request,id):
    if request.method == "POST":
        specialist = request.POST["speciality"]
        date_of_appointment = request.POST["date"]
        time_of_appointment = request.POST["time"]
        doctor_name = request.POST["doctor_name"]

        doctor_detail = User.objects.get(id=id)
        doctor_first_name = doctor_detail.first_name
        doctor_last_name = doctor_detail.last_name

        doctor_full_name = doctor_first_name+" "+doctor_last_name


        patent_info = User.objects.get(id=request.user.id)

        appointment_data = Appointment.objects.create(speciality=specialist,appointment_date=date_of_appointment,appointment_time=time_of_appointment,patient_name=patent_info,doctor_name=doctor_full_name)
        appointment_data.save()
        status = {
            "status":"Your appointment successfully..."
        }

        return render(request,"appointment_form.html",status)

    return render(request,"appointment_form.html")

@login_required
def my_appointment(request):
    appointment_detail = Appointment.objects.filter(patient_name=request.user.id)
    return render(request,"my_appointment.html",{"data":appointment_detail})

