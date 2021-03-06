import os.path
from django.db import models
import json
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

MODELS_CACHE = None
ROOT_URL = 'smyt_items/'


def get_smyt_models():
    global MODELS_CACHE
    if MODELS_CACHE is not None:
        return MODELS_CACHE
    items = []
    for mdl in models.get_models(include_auto_created=False):
        if getattr(mdl, 'is_smyt', False):
            items.append(mdl)
    MODELS_CACHE = items
    return items


def smyt_items_json_view(request):
    items = [{
        'title': mdl._meta.verbose_name,
        'url': ROOT_URL + mdl._meta.db_table,
        'name': mdl._meta.db_table,
        'fields': [{
            "name": fld,
            "type": mdl._meta.get_field(fld).get_internal_type(),
            "title": mdl._meta.get_field(fld).verbose_name
        } for fld in mdl._meta.get_all_field_names()]
    } for mdl in get_smyt_models()]
    data = json.dumps(items)
    return HttpResponse(data, content_type='application/json')


urlpatterns += [
    url(r'^%s$' % ROOT_URL, smyt_items_json_view),
]

#FIXME: ugly thing, but works
urlpatterns += [
    url(r'^' + ROOT_URL + mdl._meta.db_table, mdl.__module__.rsplit('.', 1)[0] + '.views.' + mdl._meta.db_table + '_list_view') for mdl in get_smyt_models()
]


if settings.DEBUG:
    document_root = os.path.abspath(os.path.join(
        settings.BASE_DIR, '../public_html'))
    urlpatterns += static('/assets/',
        document_root=document_root + '/assets')
    urlpatterns += static('/',
        path='index.html',
        document_root=document_root)
