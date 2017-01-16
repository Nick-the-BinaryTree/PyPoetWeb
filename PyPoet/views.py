from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import celery.task.control
from . import tasks

results = []
lines = ""
progress = 0

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
    global progress
    global lines
    global results
    if not request.method == 'GET':
        url = request.POST["URL"]
        si = request.POST["StartIndex"]
        tl = request.POST["TotalLines"]
        sl = request.POST["SentenceLength"]
        st = request.POST["SentenceThreshold"]
        tl = int(tl)
        for i in range(1, tl, 2):
            results.append(tasks.poemAdd.delay(url, si, sl, st, True))

        done = 0
        for x in results:
            if x.successful():
                done += 1
                progress = done//tl*100
                print(progress)
                lines += x.get()

        if tl % 2 == 1:
            lines += tasks.poemAdd(url, si, sl, st, False)
        return render(request, "PyPoet/index.html",
                      {"output": lines,
                       "tl" : tl,
                       "url" : url,
                       "si" : si,
                       "sl" : sl,
                       "st" : st,
                       })
    return HttpResponse("Something went terribly wrong.")

def leaving(request):
    stopAll()
    return JsonResponse({'Good':'bye'})

def update(request):
    global progress
    print(progress)
    return JsonResponse({'progress':progress})

def stopAll():
    global lines
    lines = ""
    global progress
    progress = 0
    for x in results:
        print("Stopping task: " + str(x))
        x.revoke(terminate=True)
    celery.task.control.discard_all()
    global results
    results = []