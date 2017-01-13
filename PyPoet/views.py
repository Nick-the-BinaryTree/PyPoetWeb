from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from . import PyPoetMod

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'PyPoet/index.html'

def submit(request):
    if not request.method == 'GET':
        poem = ""
        url = request.POST["URL"]
        si = request.POST["StartIndex"]
        tl = request.POST["TotalLines"]
        sl = request.POST["SentenceLength"]
        st = request.POST["SentenceThreshold"]
        if url and si and tl and sl and st:
            poem = PyPoetMod.getPoem(url, si, tl, sl, st)
        else:
            poem = "Were all the boxes filled?"
        return render(request, "PyPoet/index.html", {"output": poem})
    return HttpResponse("Something went terribly wrong.")