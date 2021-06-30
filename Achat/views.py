from django.shortcuts import render, redirect
from Architect.models import User, Chantier
from datetime import datetime, date
from . import forms, ScheduleChant, ScheduleAchat, phaseApp, chantierApp

def login(request, Pseudo, Password):
    Users = User.objects.values_list('Pseudo', 'Password')
    for i in range(len(Users)):
        if Users[i][0] == Pseudo:
            if Users[i][1] == Password:
                Today = datetime.today().date()
                request.session['connected'] = 'true'
                request.session['year'] = str(date.today().year)
                request.session['month'] = str(date.today().month)
                request.session['day'] = str(date.today().day)
                return 1;
    return 0;


def index(request):
    request.session.set_expiry(3600*4)
    form = forms.ConnexionForm()
    Pseudo = ''
    password = ''
    Users = {}
    Erreur = ''
    if request.method == 'POST':
        form = forms.ConnexionForm(request.POST)
        if form.is_valid():
            Pseudo = form.cleaned_data['inputPseudo']
            Password = form.cleaned_data['inputPassword']
            test = login(request, Pseudo, Password)
            if not test:
                Erreur = 'Le Pseudo ou le mot de passe est incorrect'
            else:
                year = request.session['year']
                month = request.session['month']
                day = request.session['day']
                return redirect('/Achat/TimelineChant/')
    my_dict = {
        'form': form,
        'connected': request.session.get('connected'),
        'Erreur': Erreur,
    }
    return render(request, 'Home.html', context=my_dict)


def achat(request):
    if request.session.get('connected') == 'true':
        chantier_list = Chantier.objects.order_by('Name')
        context = {
            'chantier': chantier_list,
            'connected': request.session.get('connected'),
        }
        return render(request, 'Achat.html', context)
    else:
        return redirect('/Home')

def scheduleChant(request):
    return ScheduleChant.schedule(request)

def refreshScheduleChant(request):
    return ScheduleChant.refreshSchedule(request)

def scheduleAcheteur(request):
    return ScheduleAchat.schedule(request)

def refreshScheduleAchat(request):
    return ScheduleAchat.refreshSchedule(request)

def resizeTask(request):
    return phaseApp.resize(request)

def setDateTimeline(request):
    return ScheduleChant.setDateTimeline(request)

def Chantier_new(request):
    return chantierApp.New(request)

def Chantier_modif(request, chant_id):
    return chantierApp.Modif(request,chant_id)

def chantierDelete(request, chant_id):
    return chantierApp.Delete(request,chant_id)

def Phase_new(request, chant_id, typePhase):
    return phaseApp.New(request, chant_id, typePhase)

def Phase_modif(request, phase_id):
    return phaseApp.Modif(request, phase_id)

def Phase_save(request, phase_id):
    return phaseApp.Save(request, phase_id)

def phaseDelete(request, phase_id):
    return phaseApp.Delete(request, phase_id)
