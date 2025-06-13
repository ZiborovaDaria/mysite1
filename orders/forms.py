import re
from django import forms
from django.core.validators import RegexValidator

class CreateOrderForm(forms.Form):
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        }),
        error_messages={
            'required': 'Пожалуйста, укажите ваше имя',
        }
    )
    
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вашу фамилию'
        }),
        error_messages={
            'required': 'Пожалуйста, укажите вашу фамилию',
        }
    )
    
    phone_number = forms.CharField(
        label="Номер телефона",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '79991234567',
            'data-mask': '00000000000'
        }),
        error_messages={
            'required': 'Пожалуйста, укажите номер телефона',
        }
    )
    
    requires_delivery = forms.ChoiceField(
        choices=[
            ("1", "Доставка курьером"),
            ("0", "Самовывоз"),
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        initial="1"
    )
    
    delivery_address = forms.CharField(
        label="Адрес доставки",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Город, улица, дом, квартира',
            'rows': 3
        }),
        required=False
    )
    
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", "Оплата картой онлайн"),
            ("1", "Оплата при получении"),
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        initial="0"
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        
        if not phone_number.isdigit():
            raise forms.ValidationError(
                "Номер телефона должен содержать только цифры",
                code='invalid_phone_format'
            )
        
        if len(phone_number) != 11:
            raise forms.ValidationError(
                "Номер телефона должен содержать 11 цифр",
                code='invalid_phone_length'
            )
        
        if not phone_number.startswith(('7', '8')):
            raise forms.ValidationError(
                "Номер должен начинаться с 7 или 8",
                code='invalid_phone_start'
            )
        
        return phone_number


    def clean(self):
        cleaned_data = super().clean()
        requires_delivery = cleaned_data.get('requires_delivery')
        delivery_address = cleaned_data.get('delivery_address')
        pickup_store = cleaned_data.get('pickup_store')

        if requires_delivery == "1" and not delivery_address:
            self.add_error('delivery_address', "Пожалуйста, укажите адрес доставки")
        
        if requires_delivery == "0" and not pickup_store:
            self.add_error(None, "Пожалуйста, выберите магазин для самовывоза")
        
        return cleaned_data


   