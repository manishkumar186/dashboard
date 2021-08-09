from django.urls import path
from . import views

app_name="account"
urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.login,name="login"),
    path('register/',views.register,name="register"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('profile/',views.profile,name="profile"),
    path('create_blog/',views.create_blog,name="create_blog"),
    path('my_blog/',views.my_blog,name="my_blog"),
    path('<int:id>/',views.read_full_article,name="read_full_article"),
    path('all_blog/',views.all_blog,name="all_blog"),
    path('logout/',views.logout,name="logout"),

    
    
]