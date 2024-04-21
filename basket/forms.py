from django import forms

class AddToBasketForm(forms.Form):
    productid = forms.IntegerField(widget=forms.HiddenInput)
    productqty = forms.IntegerField()