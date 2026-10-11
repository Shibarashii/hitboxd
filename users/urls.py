from django.urls import path

from . import views

urlpatterns = [
        path('<str:username>', views.UserProfileDetailView.as_view(), name="user-profile-detail"),
    
]

