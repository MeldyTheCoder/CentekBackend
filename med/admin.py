from django.contrib import admin
from .models import *

admin.site.register(Doctor)
admin.site.register(User)
admin.site.register(Speciality)
admin.site.register(Consultation)
admin.site.register(ConsultationMessage)
admin.site.register(Review)
