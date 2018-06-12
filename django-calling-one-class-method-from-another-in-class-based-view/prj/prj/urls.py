"""prj URL Configuration

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
from django.urls import path
from django.contrib import admin

import app.views
# import app.views

urlpatterns = [
    path("hello/fn", app.views.hello_fn),
    path("hello/class", app.views.HelloClass.hello),
    path("hello/class2", app.views.HelloClass.hello2),
    path('score/view', app.views.ScoreView.as_view()), # Intended use
    path('score/get_player_stats', app.views.ScoreView.get_player_stats), # Noto
]
