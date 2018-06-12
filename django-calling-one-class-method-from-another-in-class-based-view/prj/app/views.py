from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import classonlymethod


# CASE 1: normal function - OK
def hello_fun(request):
    context = dict(method="hello_fun")
    return render(request, 'hello.html', context)


class HelloClass(object):
    def get(self, request, **kwargs):
        return render(request, 'hello.html', kwargs)

    # Object method
    def om_hello(self, request):
        return self.get(request, 'hello.html', **{"method": "object method"})

    @classmethod
    def cm_hello(cls, request):
        return cls.get(cls, request, **{"method": "class method"})

    @staticmethod
    def sm_hello(request):
        self = None  # Problem
        return self.get(self, request, **{"method": "static method"})

    @classonlymethod
    def as_view(cls, **initkwargs):
        def view(request, **kwargs):
            self = cls(**initkwargs)
            self.request = request
            self.kwargs = kwargs
            return self.get(request, **{"method": "view construction"})

        return view
