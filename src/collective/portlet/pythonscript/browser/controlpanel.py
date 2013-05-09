# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.controlpanel.form import ControlPanelForm
from zope.formlib.form import action, FormFields
from zope.interface import Interface, implements

class IPythonScriptControlPanel(Interface):
    """Form interface."""

class IPythonScriptControlPanelFields(Interface):
    """Fields of the form."""

class PythonScriptControlPanel(ControlPanelForm):
    """
    Form for managing Python Scripts TTW.
    """
    implements(IPythonScriptControlPanel)

    label = u'Manage Python Scripts for use in portlets.'
    description = u'Here you can add and manage Python Scripts that later-on can be choosen to render a Script Portlet.'
    id = u'manage-pythonscript'
    form_name = u''
    form_fields = FormFields(IPythonScriptControlPanelFields)
