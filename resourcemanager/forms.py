from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms
from .models import ServerGroup,BizSystem,Component


class SearchForm(forms.Form):
    input_class = 'form-control mr-sm-2'
    server_group = forms.ModelChoiceField(label='服务器分组', required=False, queryset=ServerGroup.objects.all().order_by('name'))
    server_group.widget.attrs = {'class':input_class,'placeholder':'服务器分组'}
    biz_system = forms.ModelChoiceField(label='业务系统', required=False, queryset=BizSystem.objects.all().order_by('name'))
    biz_system.widget.attrs = {'class':input_class,'placeholder':'业务系统'}
    component = forms.ModelChoiceField(label='组件', required=False, queryset=Component.objects.all())
    component.widget.attrs = {'class':input_class,'placeholder':'组件'}
    query = forms.CharField(label='', required=False, max_length=100)
    query.widget.attrs = {'class':input_class, 'placeholder':'服务器名称或IP'}
