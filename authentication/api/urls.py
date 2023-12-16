from django.urls import path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register',RegisterView.as_view(),name='register'),
    path('googleuser',GoogleLoginView.as_view(),name='googleuser'),
    path('check-auth/', CheckAuth, name='check-auth'),


     path('login',LoginView.as_view(),name='login'),
     path('user',GetUserView.as_view(),name='user'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),


    path('changeprofile',ChangeProfilePicView.as_view(),name='changeprofile'),
    path('editprofile',EditProfileView.as_view(),name='editprofile'),


         

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


