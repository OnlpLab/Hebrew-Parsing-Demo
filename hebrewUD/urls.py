"""hebrewUD URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls import include, url
from treeFetcher import views, views_api




urlpatterns = [
    #path('', views.submit_utterance, name="home"),
    path('home', views.landing_page, name="home"),
    path('', views_api.submit_utterance, name="demo"),
    # path('conll-reader', views.submit_conll, name="conll-reader"),
    path('resources', views.resources, name="resources"),
    path('documentation', views.documentation, name="documentation"),
    path('faq', views.faq, name="faq"),
    path('admin/', admin.site.urls),
    path('contact', views.contact, name="contact"),
    path('about', views.about, name="about"),
    path('postags', views.postags, name="postags"),
    path('spmrl_dependencies', views.spmrl_dependencies, name="spmrl_dependencies"),
    path('spmrl_features', views.spmrl_features, name="spmrl_features")

]
