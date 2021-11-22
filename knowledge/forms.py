from django.utils.translation import ugettext_lazy as _

from django import forms

class SearchForm(forms.Form):
    input_class = 'form-control mr-sm-2'
    title = forms.CharField(label='', required=False, max_length=100)
    title.widget.attrs = {'class':input_class, 'placeholder':'标题'}
    content = forms.CharField(label='', required=False, max_length=100)
    content.widget.attrs = {'class':input_class, 'placeholder':'内容'}
    page = forms.CharField(required=False)
    page.widget = forms.HiddenInput()
    page_size = forms.CharField(required=False)
    page_size.widget = forms.HiddenInput()
