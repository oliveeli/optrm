from django.contrib import admin

from django.contrib import admin
from .models import Category, Article

from mptt.admin import DraggableMPTTAdmin
import datetime

admin.site.register(Category, DraggableMPTTAdmin)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','category', 'create_time','create_user','user_group_list',)
    fields = ['title','category','content','user_group']
    search_fields = ('title',)
    list_per_page = 10
    
    def save_model(self, request, obj, form, change):
        if change == False:
            # save 
            obj.create_time = datetime.datetime.now() 
            obj.create_user = request.user
        else:
            # update
            obj.update_time = datetime.datetime.now() 
            obj.update_user = request.user
        super(ArticleAdmin, self).save_model(request, obj, form, change)