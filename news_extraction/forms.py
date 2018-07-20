from django import forms


class NameForm(forms.Form):
    news_link = forms.CharField(max_length=500)
