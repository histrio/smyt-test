import os.path
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
if settings.DEBUG:
    document_root = os.path.abspath(os.path.join(
        settings.BASE_DIR, '../public_html'))
    urlpatterns += static('/assets/',
        document_root=document_root+'/assets')
    urlpatterns += static('/',
        path='index.html',
        #show_indexes=True,
        document_root=document_root)


