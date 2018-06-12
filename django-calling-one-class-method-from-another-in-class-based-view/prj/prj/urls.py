"""
    
"""
from django.conf.urls import url
from django.contrib import admin

import app.views
# import app.views

urlpatterns = [
    url("hello/fun", app.views.hello_fun),  # OK
    url("hello/object_method", app.views.HelloClass.om_hello),  # Problem 
    url("hello/class_method", app.views.HelloClass.cm_hello),  # OK
    url('hello/static_method', app.views.HelloClass.sm_hello),  # Problem 
    url('hello/as_view', app.views.HelloClass.as_view()),  # Noto
]
