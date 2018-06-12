from django.urls import path
# from django.url import path
from django.http import HttpResponse
from django.utils.decorators import classonlymethod


# CASE 1: normal function - OK
def just_a_fun(request, **kwargs):
    context = kwargs if kwargs else {"method": "just a function"}
    return HttpResponse('method = %(method)s' % context)


class ViewClass(object):
    def get(self, request, **kwargs):
        return just_a_fun(request, **kwargs)

    # CASE 2: Object method - FAIL, not possible to use in `django.url.path`-calls
    def om_view(self, request):
        return self.get(request, **{"method": "object method"})

    # CASE 3: class method - OK
    @classmethod
    def cm_view(cls, request):
        return cls.get(cls, request, **{"method": "class method"})

    # CASE 4: static method - FAIL, not possible to call `cls.get` or `self.get`
    @staticmethod
    def sm_view(request):
        self = None  # This is a problem with static methods
        return self.get(self, request, **{"method": "static method"})

    # CASE 5: HOF-view, similar to django.views.generic.View.as_view - OK
    @classonlymethod
    def as_view(cls, **initkwargs):
        def view(request, **kwargs):
            self = cls(**initkwargs)  # Object construction
            self.request = request
            self.kwargs = kwargs
            return self.get(request, **{"method": "HOF as_view"})

        return view


urlpatterns = [
    path("just-a-fun", just_a_fun),  # OK
    path("object-method",
         ViewClass.om_view),  # Problem: redundant `self` for `path`
    path("class-method", ViewClass.cm_view),  # OK
    path('static-method',
         ViewClass.sm_view),  # Problem: not possible to call `get`
    path('hof-view', ViewClass.as_view()),  # OK. Object construc
]
