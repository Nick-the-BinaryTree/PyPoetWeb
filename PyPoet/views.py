from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from . import PyPoetMod

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'PyPoet/index.html'

def submit(request):
    if not request.method == 'GET':
        cl = 0
        p = ""
        url = request.POST["URL"]
        si = request.POST["StartIndex"]
        tl = request.POST["TotalLines"]
        sl = request.POST["SentenceLength"]
        st = request.POST["SentenceThreshold"]
        if "CurrentLine" in request.POST and request.POST["CurrentLine"] != "":
            cl = request.POST["CurrentLine"]
            cl = int(cl)
            p = request.POST["Progress"]
        lines = poemAdd(url, si, sl, st, cl, p)
        return render(request, "PyPoet/index.html", {"output": lines["output"], "cl" : lines["cl"], "tl" : tl})
    return HttpResponse("Something went terribly wrong.")

def poemAdd(url, si, sl, st, cl, p):
    output = "" # -1 random start index, 2 for 2 lines
    failLimit = 10

    for i in range(failLimit+1):
        output = PyPoetMod.getTwoLines(p, url, si, 2, sl, st)
        if not "Could not complete" in output:
            break

    return {"output" : output, "cl": cl + 3}