from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import celery.task.control
from celery.result import ResultSet
from . import tasks

results = ResultSet([])

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'PyPoet/index.html'

# def submit(request):
#     if not request.method == 'GET':
#         cl = 0
#         p = ""
#         lines = {}
#         url = request.POST["URL"]
#         si = request.POST["StartIndex"]
#         tl = request.POST["TotalLines"]
#         sl = request.POST["SentenceLength"]
#         st = request.POST["SentenceThreshold"]
#         if "CurrentLine" in request.POST and request.POST["CurrentLine"] != "":
#             cl = request.POST["CurrentLine"]
#             cl = int(cl)
#             p = request.POST["Progress"]
#         if int(tl) - cl == 1:
#             print("\n\nADDING ONE")
#             print("Current Line: " + str(cl) + "\n\n")
#             lines = poemAdd(url, si, sl, st, cl, p, False)
#         else:
#             lines = poemAdd(url, si, sl, st, cl, p, True)
#         return render(request, "PyPoet/index.html",
#                       {"output": lines["output"],
#                        "cl" : lines["cl"],
#                        "tl" : tl,
#                        "url" : url,
#                        "si" : si,
#                        "sl" : sl,
#                        "st" : st,
#                        })
#     return HttpResponse("Something went terribly wrong.")
#
# def poemAdd(url, si, sl, st, cl, p, twoLines):
#     output = "" # -1 random start index, 2 for 2 lines
#
#     if twoLines:
#         failLimit = 0
#
#         for i in range(failLimit+1):
#             output = tasks.getTwoLines(p, url, si, 2, sl, st)
#             if not "Could not complete" in output:
#                 break
#
#         return {"output" : output, "cl": cl + 2}
#     output = tasks.getOneLine(p, url, si, 1, sl, st)
#     return {"output": output, "cl": cl + 1}

def submit(request):
    stopAll()
    global results
    if not request.method == 'GET':
        url = request.POST["URL"]
        si = request.POST["StartIndex"]
        tl = request.POST["TotalLines"]
        sl = request.POST["SentenceLength"]
        st = request.POST["SentenceThreshold"]
        tl = int(tl)
        for i in range(1, tl, 2):
            results.add(tasks.poemAdd.delay(url, si, sl, st, True))

        if tl % 2 == 1:
            results.add(tasks.poemAdd.delay(url, si, sl, st, False))

        return JsonResponse({'Down to':'business'})
    return HttpResponse("Something went terribly wrong.")

def leaving(request):
    stopAll()
    return JsonResponse({'Good':'bye'})

def update(request):
    global results
    done = results.completed_count()
    total = len(results)
    progStr = "Progress: " + str(done) + " / " + str(total) + " operations"
    if results.ready() and total != 0:
        return JsonResponse({'progress':progStr, 'output':results.get()})
    return JsonResponse({'progress':progStr})

def stopAll():
    global results
    results.revoke(terminate=True)
    results.clear()
    # celery.task.control.discard_all()