import re

from django import forms

from catalog.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("name", "phone", "message")
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ваше имя"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "+7 900 000-00-00"}
            ),
            "message": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Сообщение"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Все поля обязательны
        for field in self.fields.values():
            field.required = True

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Имя должно содержать хотя бы 2 символа.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if not re.fullmatch(r"\+?[\d\s\-()]{10,20}", phone):
            raise forms.ValidationError(
                "Введите телефон: только цифры, пробелы, «+», «-» и скобки, от 10 символов."
            )
        return phone

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 5:
            raise forms.ValidationError("Сообщение слишком короткое.")
        return message
