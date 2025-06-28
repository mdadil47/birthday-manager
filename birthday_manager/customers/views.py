"""
customers/views.py
==================
All public (staff) views for the Birthday Manager app.
"""

from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Sum
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import CustomerForm
from .models import Customer


# ────────────────────────────────────────────────────────────────
#  DASHBOARD – upcoming birthdays (next 30 days)
# ────────────────────────────────────────────────────────────────
class UpcomingBirthdays(LoginRequiredMixin, ListView):
    model = Customer
    template_name = "customers/list.html"      # Upcoming page
    context_object_name = "customers"

    def get_queryset(self):
        today = date.today()
        window_end = today + timedelta(days=30)

        # Collect customers whose next_birthday() lies in the window
        qs = [
            c for c in Customer.objects.all()
            if today <= c.next_birthday <= window_end
        ]
        # Sort by soonest birthday
        return sorted(qs, key=lambda c: c.next_birthday)


# ────────────────────────────────────────────────────────────────
#  FULL CRUD
# ────────────────────────────────────────────────────────────────
class CustomerList(LoginRequiredMixin, ListView):
    """
    /customers/  – list + search all customers.
    Shows total billing for *just* the customers returned.
    """
    model               = Customer
    template_name       = "customers/all.html"
    context_object_name = "customers"
    ordering            = ["name"]

    def get_queryset(self):
        qs = super().get_queryset()
        term = self.request.GET.get("q", "").strip()

        if term:
            qs = qs.filter(
                Q(name__icontains=term) |
                Q(email__icontains=term) |
                Q(phone__icontains=term)
            )

        self.filtered_qs = qs  # save for total aggregation
        return qs.order_by(*self.ordering)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")

        ctx["total_billing"] = (
            self.filtered_qs.aggregate(total=Sum("last_billing"))["total"] or 0
        )
        return ctx


class CustomerCreate(LoginRequiredMixin, CreateView):
    model         = Customer
    form_class    = CustomerForm
    template_name = "customers/form.html"
    success_url   = reverse_lazy("customer_list")


class CustomerUpdate(LoginRequiredMixin, UpdateView):
    model         = Customer
    form_class    = CustomerForm
    template_name = "customers/form.html"
    success_url   = reverse_lazy("customer_list")


class CustomerDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model         = Customer
    template_name = "customers/confirm_delete.html"
    success_url   = reverse_lazy("customer_list")
    success_message = "Customer deleted."

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)
