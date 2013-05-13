from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFPlone import PloneMessageFactory as _
from zope import schema
from zope.formlib import form
from zope.interface import implements
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IPythonScriptPortlet(IPortletDataProvider):
    """Schema of Python Script portlet."""

    script_name = schema.Choice(
        title=_(u"Python Script"),
        description=_(u"Python Script used to generate list of results"),
        required=True,
        source='python-scripts'
    )

class PythonScriptPortletAssignment(base.Assignment):
    """Assignment of Python Script portlet."""
    implements(IPythonScriptPortlet)
    
    def __init__(self, script_name=None):
        self.script_name = script_name
    
    @property
    def title(self):
        return _(u"Python Script ${script_name}", mapping={'script_name': self.script_name})

class PythonScriptPortletAddForm(base.AddForm):
    """Python Script portlet add form."""
    
    form_fields = form.Fields(IPythonScriptPortlet)

    label = _(u"Add Python Script Portlet")
    description = _(u"This portlet displays list of catalog objects returned by assigned Python Script")

    def create(self, data):
        return PythonScriptPortletAssignment(
            script_name=data['script_name']
        )

class PythonScriptPortletEditForm(base.EditForm):
    """Python Script portlet edit form."""
    
    form_fields = form.Fields(IPythonScriptPortlet)

    label = _(u"Edit Python Script Portlet")
    description = _(u"This portlet displays list of catalog objects returned by assigned Python Script")

class PythonScriptPortletRenderer(base.Renderer):
    """Python Script portlet renderer."""
    
    template = ViewPageTemplateFile('portlet.pt')
    
    def render(self):
        """Render portlet."""
        return self.template()