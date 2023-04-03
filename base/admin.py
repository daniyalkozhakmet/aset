from django.contrib import admin
from .models import  User,Category,Neighborhood,Contact,Complaint,Sub_category
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Neighborhood)
admin.site.register(Contact)
admin.site.register(Complaint)
admin.site.register(Sub_category)