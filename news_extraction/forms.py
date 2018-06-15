from django import forms


class NameForm(forms.Form):
    news_title = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 50}))
    news_text = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}))
