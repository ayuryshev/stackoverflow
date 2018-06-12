# django-calling-one-class-method-from-another-in-class-based-view

## Question

https://stackoverflow.com/questions/50806626/django-calling-one-class-method-from-another-in-class-based-view


## Answer

I see here 2 problems: 

1. Misconceptions about `class-based views` in `django`  
2. Misconceptions about `object-` and `class-` methods in `python`

Let's look in more detail.

# 1. Django class-based views 

It must be sound strange (especially for newcomers) but `class-based view` in django does not means that you bind methods of  `objects`/`classes` to `url`-routes. 

More so:  

 - `django.urls.path` can use only functions of `fn(request, *args, **kwargs)`

 - Pythonic `it's better explicite`  for `self`-param  makes `object-methods` unusable for `views` (at least without "special magic").

**So what the meaning of `class-based views`?**


https://github.com/django/django/blob/2bc014750adb093131f77e4c20bc17ba64b75cac/django/views/generic/base.py#L48

In fact it's very simple: 

 1. `class-based view` expose class method `as_view`
 2. `as_view` is a high-order function and not used directly in  `path`/`url` calls.
 3. `as_view` constructs actual view function at runtime
 4. generated function is not very complicated too. Roughly speaking, it looks for existence of defined `get`/`post`/`put`/`head`-methods, calls them when they exists and raises exceptions when not exists. 


So you can see that "one does not simply binds methods of class-view to url-routes in django".

It is a tool that can be hardly recommended for general cases, it works good in cases when this inflexibility is desirable.


# 2. `object-`,`class-`, `static-` methods

OK. Now the second problem. 

Can we call from methods of `class-based view` other methods?

Yes we can but with some restrictions.

Let's look at `one-file` demo in django  2.0. (For 1.11 - `%s/path/url/g`)

    from django.urls import path    
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
        path('hof-view', ViewClass.as_view()),  # OK. 
    ]


Summary:

 1. Plain functions are best in general
 2. Object methods are not usable (at least without some "special magic")
 3. Class methods: have no problems. But keep in mind that class methods can use only other class methods
 4. Static methods: OK for using in `path`/`url` calls but they can't use other methods of classes 
 5. If you really really want to use OOP:  you can do it in "django way" - create HOFs that will generate actual views functions at runtime. Look at `django.views.generic` source code for inspiration

...

I hope that must clear things up but questions, critique, corrections - you are welcome!
