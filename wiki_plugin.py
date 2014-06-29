# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.conf.urls import include, patterns, url
from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wikicitations.markdown_extensions import CitationExtension
from wikicitations import views
from django.core.urlresolvers import reverse_lazy
 
 
class CitationPlugin(BasePlugin):
    slug = 'citations'

    urlpatterns = {
        'article': patterns('',
            url(r'^json/query-urlpath/$', views.QueryUrlPath.as_view(), name='citations_query_urlpath'),
        )
    }
     
    sidebar = {'headline': _('Citations'),
            'icon_class': 'icon-file',
            'template': 'wikicitations/sidebar.html',
            'form_class': None,
            'get_form_kwargs': (lambda a: {})}
     
    wikipath_config = [
            ('base_url', ""),
            ('default_level', 2 ),
            ]
     
     
    markdown_extensions = [CitationExtension()]
 
registry.register(CitationPlugin)
