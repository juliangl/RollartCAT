"""RollartCAT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name='index'),
    path('login/', views.Login, name='login'),
    path('login_view/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('enter/', views.enter, name='enter'),
    path('enter/<str:next>', views.enter, name='enter'),
    path('addskater/', views.addskater, name='addskater'),
    path('delskater/<str:event_id>', views.delskater, name='delskater'),
    path('playmusic/', views.playmusic, name='playmusic'),
    path('modal/<str:pk>', views.modal.as_view(), name='modal'),
    path('judges/', views.judges, name='judges'),
    path('triaevent/', views.triaevent, name='triaevent'),
    path('triaevent/<str:next>', views.triaevent, name='triaevent'),
    path('genorder/', views.genorder, name='genorder'),
    path('pdforder/', views.pdforder, name='pdforder'),
    path('technical/', views.technical, name='technical'),
    path('contechnical/', views.contechnical, name='contechnical'),
    path('deltechnical/<str:resultat_id>', views.deltechnical, name='deltechnical'),
    path('conartistic/', views.conartistic, name='conartistic'),
    path('condeduction/', views.condeduction, name='condeduction'),
    path('result/', views.result, name='result'),
    path('punctuation/', views.punctuation, name='punctuation'),
    path('classification/', views.classification, name='classification'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)   

handler500 = views.handler500
handler404 = views.handler404
