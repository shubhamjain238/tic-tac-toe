from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from gameplay.models import Game
from .forms import Invitation_Form
from .models import Invitation
from django.contrib.auth.models import User

@login_required
def home(request):
    all_user_games = Game.objects.games_for_user(request.user)
    invitations = Invitation.objects.filter(to_user = request.user)
    return render(request, 'player/home.html', {'games': all_user_games, 'invitations': invitations})

@login_required
def send_invitation(request):
    invitation = Invitation(from_user = request.user)
    if request.method == 'POST':
        form = Invitation_Form(instance = invitation, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_home')
    form = Invitation_Form()
    return render(request, 'player/send_invitation.html', {'form': form})

@login_required
def accept_invitation(request, username):
    user = User.objects.filter(username = username).first()
    game = Game.objects.create(first_user = user, second_user = request.user)
    Invitation.objects.filter(from_user = user, to_user = request.user).delete()
    return redirect(game)
    #return redirect('player_home')

@login_required
def reject_invitation(request, username):
    user = User.objects.filter(username = username).first()
    Invitation.objects.filter(from_user=user, to_user=request.user).delete()
    return redirect('player_home')