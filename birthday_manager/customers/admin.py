from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display  = ("name", "dob", "email", "phone", "last_billing")
    search_fields = ("name", "email", "phone")
