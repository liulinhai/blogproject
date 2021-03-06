from django.contrib import admin
from .models import Post,Category,Tag,ViewNum
from django.utils import timezone
from django.utils.html import format_html
from django.core.urlresolvers import reverse
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','created_time','was_published_recently','view_num_count','modified_time','category','status','preview']
    list_display_links = ('title','author','created_time' )
    fieldsets = [
        (None,{'fields':[('title',),'body',]}),
        ('Category and Tags',{'fields':['category','tags']}),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('excerpt', ),
        }),
    ]
    list_per_page = 50
    filter_horizontal = ('tags',)
    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='p')
        if rows_updated == 1:
            message_bit = "1 post was"
        else:
            message_bit = "%s posts were" % rows_updated
        self.message_user(request, "%s successfully marked public." % message_bit)
    make_published.short_description = '公开发布'
    def make_withdrawn(self, request, queryset):
        rows_updated = queryset.update(status='w')
        if rows_updated == 1:
            message_bit = "1 post was"
        else:
            message_bit = "%s posts were" % rows_updated
        self.message_user(request, "%s successfully marked private." % message_bit)
    make_withdrawn.short_description = '仅个人可见'
    actions = [make_published,make_withdrawn]

    search_fields = ('title',)
    list_filter = ('category','tags')

    save_on_top = True

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
    def save_model(self, request, obj, form, change):
        #print(change)
        #if obj.author == '' :print('空值')
        if not change :
            #if obj.author == '' :
            obj.author = request.user

        super(PostAdmin, self).save_model(request, obj, form, change)

    def view_num_count(self,obj):
        return sum(map(lambda x:x.view_nums,obj.view_num.all()))
    view_num_count.short_description = '阅读量'


    def was_published_recently(self,obj):
        return str(( timezone.now() - timezone.timedelta(hours=0)-obj.created_time).days)+ '天前'
    was_published_recently.short_description = '发表距今'
    #was_published_recently.boolean = True
    was_published_recently.admin_order_field = 'created_time'

    def preview(self,obj):
        url = reverse('blog:detail', kwargs={'pk': obj.pk})

        return format_html(
            '<a href="{0}">浏览</a>',url,
        )
    preview.short_description = '站点浏览'

class ViewNumsAdmin(admin.ModelAdmin):
    list_display = ('content_type','object_id','view_nums')

admin.site.register(Post,PostAdmin)


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(ViewNum,ViewNumsAdmin)