from django import forms
class contactform(forms.Form):
    First_number=forms.CharField(label="value 1",widget=forms.TextInput(attrs={'class':"forms-control"}))
    Second_number=forms.CharField(label="value 1",widget=forms.TextInput(attrs={'class':"forms-control"}))