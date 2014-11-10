# -*- coding: utf-8 -*-
from django import forms


class CommentForm(forms.Form):
    author_name = forms.CharField(max_length=128, label="Псевдоним")
    body = forms.CharField(widget=forms.Textarea, label="Отзыв")


class KievDeliveryForm(forms.Form):
    street = forms.CharField(max_length=256, label="Улица")
    house = forms.CharField(max_length=10, label="Дом")
    aparment = forms.CharField(max_length=128, label="Квартира")

class NovaPoshtaAddressDeliveryForm(forms.Form):
    city = forms.CharField(max_length=128, label="Город")
    street = forms.CharField(max_length=256, label="Улица")
    house = forms.CharField(max_length=10, label="Дом")
    aparment = forms.CharField(max_length=128, label="Квартира")

class NovaPoshtaDepartmentDeliveryForm(forms.Form):
    city = forms.CharField(max_length=128, label="Город")
    department_no = forms.CharField(max_length=128, label="Номер отделения")
