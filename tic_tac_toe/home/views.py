from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('player_home')
    return render(request, 'gameplay/home.html')