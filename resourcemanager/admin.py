from django.contrib import admin
from django import forms
from .models import Component,Port,ComponentInstance,Server,BizSystem,OperatingSystem,ServerGroup,ServerConnection,UserAndPassword

admin.site.register(ServerGroup)
admin.site.register(OperatingSystem)
admin.site.register(BizSystem)
# admin.site.register(Component)
# admin.site.register(UserAndPassword)
# admin.site.register(Port)

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name','version', 'description')
    fields = ['name','version', 'description']
    search_fields = ('name', 'description')
    list_per_page = 10

@admin.register(Port)
class PortAdmin(admin.ModelAdmin):
    list_display = ('name','port','description')
    fields = ['name','port','description']
    search_fields = ('name', 'port','description')
    list_per_page = 10

@admin.register(UserAndPassword)
class UserAndPasswordAdmin(admin.ModelAdmin):
    list_display = ('name_str','user_name','password')
    fields = ['name','user_name','password']
    search_fields = ('name',)

class ComponentInstanceInline(admin.StackedInline):
    model = ComponentInstance
    fields = [('component','usage'),'port',]
    extra = 1

class ServerConnectionInline(admin.StackedInline):
    model = ServerConnection
    fields = [('user_and_password','user_group')]
    extra = 0
    min_num = 1

def validate_ip(ip_str):
    sep = ip_str.split('.')
    if len(sep) != 4:
        return False
    for i,x in enumerate(sep):
        try:
            int_x = int(x)
            if int_x < 0 or int_x > 255:
                return False
        except ValueError:
            return False
    return True

class ServerAdminForm(forms.ModelForm):
    
    def clean_ip_address(self):
        if validate_ip(self.data["ip_address"]) == False:
            raise forms.ValidationError("IP地址格式错误")
        return self.cleaned_data["ip_address"]

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    form = ServerAdminForm
    list_display = ('name','ip_address', 'cpu_cores_text','memory_size_text','disc_sys_size_text','disc_biz_size_text','operating_system','groups_list','biz_system_list','user_group_list','remote_connect_ip','remote_connect_port','summary') 
    fields = [('name','ip_address','operating_system'), ('cpu_cores','memory_size','disc_sys_size','disc_biz_size'),('group','biz_system'),'user_group',('remote_connect_ip','remote_connect_port'),'summary']
    list_filter = ('group', 'biz_system', 'user_group')
    search_fields = ('name','ip_address')
    list_per_page = 10

    inlines = [ServerConnectionInline,ComponentInstanceInline]
    pass
