from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseServerError
from Architect.models import Responsable, Chantier, Phase
from datetime import timedelta, date
import calendar
from django.db import connection
from Achat.timeline import Timeline

def refreshSchedule(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            id_phase = request.POST.get("ID")
            id_phase = id_phase.split("-")[1]
            phase = Phase.objects.get(pk=id_phase)
            colStart = request.POST.get('DGA').split("/")[1]
            colEnd = request.POST.get('GC').split("/")[0]
            delay = int(colEnd) - int(colStart)
            Debut = phase.Date_debut
            Fin = phase.Deadline
            phase.Date_debut = Debut + timedelta(days=delay * 7)
            phase.Deadline = Fin + timedelta(days=delay * 7)
            phase.save()
        except KeyError:
            HttpResponseServerError("Malformed data!")

        return JsonResponse({"success": True}, status=200)

    else:
        return JsonResponse({"success": False}, status=400)

def acheteursChantier(chantier):
    querySet = Phase.objects.filter(id_chantier=chantier.id).values('id_Responsable').distinct()
    return querySet

def schedule(request):
    if request.session.get('connected') == 'true':
        responsable_list = Responsable.objects.order_by('Name')
        chantiers = Chantier.objects.order_by('Name')
        i = 0
        k = 2
        chantier_list = list()
        begin = date(int(request.session.get('year')), int(request.session.get('month')), int(request.session.get('day')))
        weekList = Timeline(begin).WeekList
        for chant in chantiers:
            acheteurList = list()
            acheteur = acheteursChantier(chant)
            j = 0
            for A in acheteur:
                if A.get('id_Responsable') != None:
                    phases = Phase.objects.filter(id_chantier=chant.id).filter(id_Responsable=A.get('id_Responsable')).exclude(Date_debut=None).order_by('Name')
                    Self = Responsable.objects.get(pk=A.get('id_Responsable'))
                    timeline = Timeline(begin)
                    for phase in phases:
                        timeline.addTask(phase)
                    acheteurList.append({"self": Self, "timeline": timeline, "num": j})
                    j += 1

            if i%3 == 0:
                l = list()
                chantier_list.append(l)
                k=2

            if (len(acheteurList) > 1):
                row = [k, (k + len(acheteurList))]
                k += len(acheteurList)

            else:
                row = [k, (k + 1)]
                k += 1

            chantier_list[int(i/3)].append({"self": chant, "acheteurList": acheteurList, "row": row})
            i += 1

        context = {
            'WeekList': weekList,
            'chantier_list': chantier_list,
            'connected': request.session.get('connected'),
            'responsableList': responsable_list,
        }
        return render(request, 'timeline.html', context)
    else:
        return redirect('/Home')

def addMonths(inputDate, month):
    tmpMonth = inputDate.month - 1 + month
    # Add floor((input month - 1 + k)/12) to input year component to get result year component
    resYr = inputDate.year + tmpMonth // 12
    # Result month component would be (input month - 1 + k)%12 + 1
    resMnth = tmpMonth % 12 + 1
    # Result day component would be minimum of input date component and max date of the result month (For example we cant have day component as 30 in February month)
    # Maximum date in a month can be found using the calendar module monthrange function as shown below
    resDay = min(inputDate.day, calendar.monthrange(resYr, resMnth)[1])
    # construct result datetime with the components derived above
    resDate = date(resYr, resMnth, resDay)

    return resDate

def setDateTimeline(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            Data = int(request.POST.get("data"))
            if Data == 0:
                request.session['year'] = str(date.today().year)
                request.session['month'] = str(date.today().month)
                request.session['day'] = str(date.today().day)

            else:
                actualDate = date(int(request.session['year']), int(request.session['month']), int(request.session['day']))
                newDate = addMonths(actualDate, Data)
                request.session['year'] = str(newDate.year)
                request.session['month'] = str(newDate.month)
                request.session['day'] = str(newDate.day)

        except KeyError:
            HttpResponseServerError("Malformed data!")

        return JsonResponse({"success": True}, status=200)
    else:
        return JsonResponse({"success": False}, status=400)