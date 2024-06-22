from django.urls import path

from .views import ConfirmUser, ProfileView

urlpatterns = [
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
    path('<str:username>/', ProfileView.as_view(), name='profile'),
    # path('profile/', ProfileView.as_view(), name='profile')
]
