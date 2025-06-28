from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model  = Customer
        fields = [
            "name", "dob", "email", "phone",
            "last_visit", "last_billing",
        ]
        widgets = {
            "dob":         forms.DateInput(attrs={"type": "date"}),
            "last_visit":  forms.DateInput(attrs={"type": "date"}),

            # 👉 new NumberInput with placeholder & step
            "last_billing": forms.NumberInput(attrs={
                "step": "0.01",
                "placeholder": "e.g. 499.00",
            }),
        }
        labels = {
            # shorter label so the placeholder does the talking
            "last_billing": "Last billing amount",
        }
