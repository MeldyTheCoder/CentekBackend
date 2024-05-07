from django.urls import path, include
from djoser.views import TokenCreateView

from . import views

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('api/v1/profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('auth/token/create/', TokenCreateView.as_view(), name='token_create'),
    path('api/v1/authenticated_users/', views.GetMeView.as_view(), name='get_me'),
    path('api/v1/specialities/', views.SpecialityListView.as_view(), name='speciality_list'),
    path('api/v1/create', views.HospitalizationView.as_view(), name='create_hosp'),
]