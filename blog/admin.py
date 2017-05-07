from django.contrib import admin
from .models import Post,Category,Tag,ViewNum
from django.utils import timezone
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','created_time','was_published_recently','view_num_count','modified_time','category']
    fieldsets = [
        (None,{'fields':[('title','author'),'body','excerpt']}),
        ('Category and Tags',{'fields':['category','tags']})
    ]
    list_per_page = 50
    filter_horizontal = ('tags',)

    search_fields = ('title',)
    list_filter = ('category','tags')

    def view_num_count(self,obj):
        return sum(map(lambda x:x.view_nums,obj.view_num.all()))
    view_num_count.short_description = '阅读量'


    def was_published_recently(self,obj):
        return str(( timezone.now() - timezone.timedelta(hours=1)-obj.created_time).days)+ '天前'
    was_published_recently.short_description = '发表距今'
    #was_published_recently.boolean = True

class ViewNumsAdmin(admin.ModelAdmin):
    list_display = ('content_type','object_id','view_nums')

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ViewNum,ViewNumsAdmin)
