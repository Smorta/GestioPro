from django.shortcuts import render, redirect
from Architect.models import Responsable, Phase, Chantier
from . import forms
from django.db import connection
from datetime import date
from Achat.timeline import Timeline

def New(request):
    if request.session.get('connected') == 'true':
        if request.method == 'POST':
            form = forms.ResponsableForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['inputName']
                firstName = form.cleaned_data['inputFirstName']
                Resp = Responsable.objects.get_or_create(
                    FirstName=firstName,
                    Name=name)[0]
                id = str(Resp.id)
                Resp.save()
                return redirect('./Modif' + id)
        form_list = forms.ResponsableForm()
        context = {
            'form': form_list,
            'connected': request.session.get('connected'),
        }
        return render(request, 'ResponsableNew.html', context)
    else:
        return redirect('/Home')

def PhasesPlan(resp_id):
    return Phase.objects.filter(id_Responsable=resp_id).exclude(State=2).exclude(Date_debut=None)

def PhasesNonPlan(resp_id):
    return Phase.objects.filter(Date_debut=None)

def PhaseFinish(resp_id):
    return Phase.objects.filter(id_Responsable=resp_id, State=2)

def chantierResp(resp_id):
    querySet = Phase.objects.filter(id_Responsable = resp_id).values('id_chantier').distinct()
    return querySet

def GetChantierList(begin, resp_id):
    chantier_list = list()
    chantiers = chantierResp(resp_id)
    j = 0
    for chant in chantiers:
        phases = Phase.objects.filter(id_Responsable=resp_id).filter(id_chantier=chant.get('id_chantier')).order_by('Name')
        Self = Chantier.objects.get(pk=chant.get('id_chantier'))
        timeline = Timeline(begin,2)
        for phase in phases:
            timeline.addTask(phase)
        chantier_list.append({"self": Self, "timeline": timeline, 'num': j})
        j += 1
    return chantier_list

def Modif(request, resp_id):
    if request.session.get('connected') == 'true':
        year = request.session['year']
        month = request.session['month']
        day = request.session['day']
        begin = date(int(year), int(month), int(day))
        weekList = Timeline(begin).WeekList
        resp = Responsable.objects.get(pk=resp_id)
        phasesPlan = PhasesPlan(resp_id)
        phasesNonPlan = PhasesNonPlan(resp_id)
        phasesFinish = PhaseFinish(resp_id)
        name = resp.Name
        firstName = resp.FirstName
        if request.method == 'POST':
            form = forms.ResponsableForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['inputName']
                firstName = form.cleaned_data['inputFirstName']
                resp.Name = name
                resp.FirstName = firstName
                resp.save()
                return redirect('/Architect/TimelineArchi/')

        form_list = forms.ResponsableForm(initial={
            'inputName': name,
            'inputFirstName': firstName
        })

        context = {
            'form': form_list,
            'Resp': resp,
            'PhasePlan': phasesPlan,
            'PhaseNonPlan': phasesNonPlan,
            'PhaseFinish': phasesFinish,
            'WeekList': weekList,
            'chantierList':GetChantierList(begin, resp_id),
            'connected': request.session.get('connected'),
        }
        return render(request, 'ResponsableModif.html', context)
    else:
        return redirect('/Home')