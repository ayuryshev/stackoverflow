from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render


def hello_fn(request):
    context = dict(
        method="hello_fn",
        player_id=1,
        stats = 1,
    )
    return render(request, 'hello.html', context)

class HelloClass(object):
    @classmethod
    def hello(self, request):
        context = dict(
            method="HelloClass.hello",
            player_id=1,
            stats = 1,
        )     
        
        return render(request, 'hello.html', context)

    def hello2(self, request):
        context = dict(
            method="HelloClass.hello",
            player_id=1,
            stats = 1,
        )        
        return render(request, 'hello.html', context)



class ScoreView(TemplateView):    
    template_name="hello.html"

    def get_context_data(self,**kwargs):        
        context = super().get_context_data(**kwargs)
        context['method'] = "get_content_data"
        context['player_id'] = 1
        context['stats'] = self.get_team_stats(1)
        return context

    @classmethod
    def get_player_stats(cls, request):        
        context = {            
            "method":"get_player_stats",
            "player_id": 2,
            "stats": cls.get_team_stats(cls,2)
        }        
        return render(request, 'hello.html', context)

    def get_team_stats(self, player_id):
        return player_id*2
