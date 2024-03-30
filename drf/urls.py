from django.urls import path, include
from . import views

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('api/v1/profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('api/v1/authenticated_users/', views.GetMeView.as_view(), name='get_me'),
    path('api/v1/specialities/', views.SpecialityListView.as_view(), name='speciality_list'),
    path('api/v1/doctors/', views.DoctorListView.as_view(), name='doctors_list'),
    path('api/v1/specialities/<int:pk>', views.SpecialityDetailView.as_view(), name='speciality_detail'),
    path('api/v1/doctors/<int:pk>', views.DoctorDetailView.as_view(), name='doctors_detail'),
    path('consultations/<int:consultation_id>/reviews/', views.ConsultationReviewView.as_view(), name='review_list_create'),
]