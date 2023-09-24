"""DataVisualizationProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webapp import views
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('index/', views.index),
    path('adminlogin/', views.adminlogin),
    path('adminviewusers/', views.adminviewusers),
    path('adminshowchart/', views.adminshowchart),
    path('usershowchart/', views.usershowchart),
    path('usermainpage/', views.usermainpage),
    path('logout/', views.logout),
    path('adminmainpage/', views.adminmainpage),
    path('userlogin/', views.userlogin),
    path('userlogincheck/', views.userlogincheck),
    path('newuser/', views.newuser),
    path('contact/', views.contact),
    path('barchart/', views.barchart),
    path('piechart/', views.piechart),
    path('linechart/', views.linechart),
    path('doughnutchart/', views.doughnutchart),
    path('scatterchart/', views.scatterchart),
     path('passwordchangepage/', views.passwordchangepage),
    path('userforgotpassword/', views.userforgotpassword),
    path('generateotp/', views.generateotppage),
    path('enterotppage/', views.enterotppage),
    path('doc/', views.doc),
]
