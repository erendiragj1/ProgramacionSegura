from django.shortcuts import render
from .forms import userForm
# Create your views here.
def login(request):
    if request.method == "POST":
        user_form = userForm(request.POST)
        print(request.POST)
        if user_form.is_valid():
            pass
    else:
        user_form = userForm()
        print(user_form)
    return render(request,"login.html",{"user_form":user_form})
