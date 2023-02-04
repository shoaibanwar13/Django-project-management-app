from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import team
from .models import image
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.core.mail import send_mail
from .form import contactform
from .models import contact
def show(request):
    return render(request,'show.html')
def about(request):
    teamMember=image.objects.all()
    return render(request,'about.html',{'teamMember':teamMember})
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Log the user in
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
        
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:

           
            return redirect('/about')
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})
    else:
        return render(request, 'login.html')
def forms(request):

    ad_img=image.objects.all()

    return render(request,'forms.html',{'image1':ad_img})        
        



    
    
   
