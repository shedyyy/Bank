from django import forms
from core.amount import AMOUNT


class DepositForm(forms.Form):
    amount = forms.FloatField(
        required=True,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Amount"}
        ),
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Description",
                "rows": 3,
            }
        ),
    )

    def clean_amount(self):
        amount = self.cleaned_data.get("amount", 0)
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0")
        return amount

    def clean_description(self):
        amount = self.cleaned_data.get("amount", 0)
        if amount > AMOUNT:
            description = self.cleaned_data.get("description")
            if len(description) < 10:
                raise forms.ValidationError(
                    "Description must be greater than 10 characters"
                )
        else:
            description = ""
            # not required
        return description






