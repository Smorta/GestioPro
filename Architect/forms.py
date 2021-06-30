from django import forms


class ConnexionForm(forms.Form):
    inputPseudo = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Votre Pseudo', 'class': 'form-control'}),
        required=True
    )
    inputPassword = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-control', 'type': 'password'}),
        required=True
    )


class ChantierModif(object):
    inputName = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class': 'form-control'}),
        required=True
    )


class ChantierForm(forms.Form):
    Entite_choices = (
        ('progimo', 'Progimo'),
        ('prologe', 'Prologe'),
        ('prologeM', 'Prologe Marche')
    )

    Type_choices = (
        ('Av-Proj', 'Avant projet'),
        ('Rea-PU', 'Réalisation PU'),
        ('Att-Perm', 'Attente permis'),
        ('Pl-Exec', 'Plan exécution'),
        ('BR', 'Brochure'),
    )

    inputName = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class': 'form-control'}),
        required=True
    )

    inputEntite = forms.CharField(
        widget=forms.Select(choices=Entite_choices, attrs={'class': "form-control selectCustom"}),
        required=True
    )

    inputDebut = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )

    inputObjectif = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )

class ResponsableForm(forms.Form):
    inputFirstName = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Prénom', 'class': 'form-control'}),
        required = True
    )

    inputName = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class': 'form-control'}),
        required = False
    )


class PhaseForm(forms.Form):

    State_choices = (
        ('0', 'Pas commencé'),
        ('1', 'En cours'),
        ('2', 'Fini')
    )
    inputName = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class': 'form-control'}),
        required=True
    )

    inputType = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class': 'form-control'}),
        required=True
    )

    inputState = forms.CharField(
        widget=forms.Select(choices=State_choices, attrs={'class': "form-control selectCustom"}),
        required=True
    )

    inputDebut = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )
    inputObjectif = forms.DateField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )
