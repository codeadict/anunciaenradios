# -*- coding: utf-8 -*-
"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'anunciaenradios.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """
    
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # append a group for "Administration" & "Applications"
        self.children.append(modules.Group(
            'Administración & Aplicaciones',
            column=1,
            collapsible=True,
            children = [
                modules.AppList(
                    'Administración',
                    column=1,
                    models=('django.contrib.*',),
                    exclude=('django.contrib.sites.*', 'django.contrib.comments.*'),
                ),
                modules.AppList(
                    'Applicaciones',
                    column=1,
                    css_classes=('collapse closed',),
                    exclude=('django.contrib.*', 'djcelery.*', 'tastypie.*', 'taggit.*'),
                )
            ]
        ))
        
        # append an app list module for "Applications"
        #self.children.append(modules.AppList(
        #    _('AppList: Applications'),
        #    collapsible=True,
        #    column=1,
        #    css_classes=('collapse closed',),
        #    exclude=('django.contrib.*',),
        #))
        
        # append an app list module for "Administration"
        #self.children.append(modules.ModelList(
        #    _('ModelList: Administration'),
        #    column=1,
        #    collapsible=False,
        #    models=('django.contrib.*',),
        #))
        
        # append another link list module for "support".
        #self.children.append(modules.LinkList(
        #    _('Media Management'),
        #    column=2,
        #    children=[
        #        {
        #            'title': _('FileBrowser'),
        #            'url': '/admin/filebrowser/browse/',
        #            'external': False,
        #        },
        #    ]
        #))
        
        # TODO: Configurar varios links aqui
        self.children.append(modules.LinkList(
            _('Soporte'),
            column=2,
            children=[
                {
                    'title': _('Visitar el sitio'),
                    'url': 'http://localhost:8080/',
                    'external': False,
                },
                {
                    'title': _('Contactar con Daganet'),
                    'url': 'mailto:dairon@daganet.net?subject=Soporte Servidinamica',
                    'external': False,
                },
            ]
        ))
        
        # append a feed module
        #self.children.append(modules.Feed(
        #    _('Latest Django News'),
        #    column=2,
        #    feed_url='http://www.djangoproject.com/rss/weblog/',
        #    limit=5
        #))
        
        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=3,
        ))


