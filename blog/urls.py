from django.conf.urls import url

from . import views

from django.conf import settings

app_name = 'blog'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^post/(?P<pk>[0-9]+)/$',views.detail,name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.archives,name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$',views.category,name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$',views.tags,name='tag'),
    url(r'^category/(?P<pk>[^/]+)/$',views.categoryn,name='categoryn'),
    url(r'^author/(?P<pk>[^/]+)/$',views.authors,name='author'),
    url(r'^search/$',views.search,name='search'),
    url(r'^test/$',views.test,name='test'),
    url(r'^contact/$',views.contact,name='contact')

]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
