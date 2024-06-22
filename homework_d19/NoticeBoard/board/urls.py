from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from .views import AnnounceList, AnnounceDetail, AnnounceCreate, AnnounceUpdate, AnnounceDelete, LogoutView, \
    ReplyUpdate, ReplyDelete

urlpatterns = [
    path('', AnnounceList.as_view(), name='announce_list'),
    path('<int:pk>/', AnnounceDetail.as_view(), name='announce_detail'),
    path('create/', AnnounceCreate.as_view(), name='announce_create'),
    path('<int:pk>/update/', AnnounceUpdate.as_view(), name='announce_update'),
    path('<int:pk>/delete/', AnnounceDelete.as_view(), name='announce_delete'),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('replies/<int:pk>/update/', ReplyUpdate.as_view(), name='reply_update'),
    path('replies/<int:pk>/delete/', ReplyDelete.as_view(), name='reply_delete'),
]
