from django.urls import path
from .views import home, send_invitation, accept_invitation, reject_invitation
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', home, name = 'player_home'),
    path('login/', LoginView.as_view(template_name='player/login_form.html'), name='player_login'),
    path('logout/', LogoutView.as_view(), name='player_logout'),
    path('send_invite/', send_invitation, name='send_invitation'),
    path('accept/<str:username>', accept_invitation, name='accept_invitation'),
    path('reject/<str:username>', reject_invitation, name='reject_invitation'),
]