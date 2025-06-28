from django.urls import path
from . import views

urlpatterns = [
    path("", views.UpcomingBirthdays.as_view(), name="upcoming_birthdays"),
    path("customers/",       views.CustomerList.as_view(),      name="customer_list"),
    path("add/", views.CustomerCreate.as_view(), name="customer_add"),
    path("edit/<int:pk>/", views.CustomerUpdate.as_view(), name="customer_edit"),
    path("delete/<int:pk>/", views.CustomerDelete.as_view(),    name="customer_delete"),
]
