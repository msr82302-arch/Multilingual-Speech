#from django.shortcuts import render

# Create your views here.



from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home(request):
    return render(request, "home.html")

@login_required(login_url="login")
def dashboard(request):
    return render(request, "dashboard.html")