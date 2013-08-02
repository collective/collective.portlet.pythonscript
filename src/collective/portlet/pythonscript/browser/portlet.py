import logging
from time import time

from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFPlone import PloneMessageFactory as _
from zope import schema
from zope.formlib import form
from zope.interface import implements
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from collective.portlet.pythonscript.content.interface import IPythonScriptManager
from zope.component import getMultiAdapter
from collective.portlet.pythonscript.browser.renderer import IResultsRenderer

logger = logging.getLogger(__name__)

class IPythonScriptPortlet(IPortletDataProvider):
    """Schema of Python Script portlet."""

    portlet_title = schema.TextLine(
        title=_(u"Portlet title"),
        description=_(u"Title to display above portlet content"),
        required=True
    )

    script_name = schema.Choice(
        title=_(u"Python Script"),
        description=_(u"Python Script used to generate list of results"),
        required=True,
        source='python-scripts'
    )

    limit_results = schema.Int(
        title=_(u"Limit results"),
        description=_(u"How many results should be displayed (none means all)"),
        required=False,
        min=1
    )

    template_name = schema.Choice(
        title=_(u"Template"),
        description=_(u"Template to use to render list of results"),
        required=True,
        source='python-scripts-templates'
    )

class PythonScriptPortletAssignment(base.Assignment):
    """Assignment of Python Script portlet."""
    implements(IPythonScriptPortlet)

    template_name = u'default'

    def __init__(self, portlet_title=u"", script_name=None, limit_results=None, template_name=None):
        self.portlet_title = portlet_title
        self.script_name = script_name
        self.limit_results = limit_results
        self.template_name = template_name

    @property
    def title(self):
        return _(u"Python Script ${portlet_title}", mapping={'portlet_title': self.portlet_title})

class PythonScriptPortletAddForm(base.AddForm):
    """Python Script portlet add form."""

    form_fields = form.Fields(IPythonScriptPortlet)

    label = _(u"Add Python Script Portlet")
    description = _(u"This portlet displays list of catalog objects returned by assigned Python Script")

    def create(self, data):
        """Create portlet assignment."""
        return PythonScriptPortletAssignment(
            portlet_title=data['portlet_title'],
            script_name=data['script_name'],
            limit_results=data['limit_results'],
            template_name=data['template_name']
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

    @property
    def portlet_title(self):
        """Returns portlet title."""
        return self.data.portlet_title

    @property
    def available(self):
        return len(self.items)

    def run_script(self, script):
        """Execute Python Script."""
        # Change the context of the script to point to current portlet context.
        bound_script = script.__of__(self.context)
        # Execute the script.
        results = bound_script()
        return results

    def wrap_results(self, results):
        """Wrap results into form that is renderable for the portlet."""
        # For now no need to format.
        return results
    
    def renderResults(self):
        """Return rendered list of results."""
        name = self.data.template_name
        renderer = getMultiAdapter((self.context, self.request), IResultsRenderer, name=name)
        return renderer(self.items, **self.props)

    _items = None
    _props = None

    @property
    def items(self):
        """Cached list of results."""
        if self._items is None:
            self._items, self._props = self.getItemsAndProps()
        return self._items

    @property
    def props(self):
        """Cached properties."""
        return self._props

    def getItemsAndProps(self):
        """Depending on what is returned by the python script,
        returns a list of results to be rendered inside portlet or
        a dict that contains the iterable value under the 'results' key
        and other properties to be rendered in the portlet.
        """
        portal_url = getToolByName(self.context, 'portal_url')
        portal = portal_url.getPortalObject()
        manager = IPythonScriptManager(portal)
        script_name = self.data.script_name
        try:
            info = manager.getInfo(script_name)
        except KeyError:
            logger.exception(u'Could not find script %r' % script_name)
            return [], {}
        if not info.enabled:
            logger.warning(u'Script %r is not enabled' % script_name)
            return [], {}
        script = manager.getScript(script_name)
        before = time()
        try:
            results = self.run_script(script)
        except Exception:
            logger.exception(u'Error while running script %r' % script_name)
            return [], {}
        else:
            timing = time() - before
            logger.info(u'Script %r executed successfully in %.3f sec' % (script_name, timing))
            if info.timing:
                info.addTiming(timing)

            if isinstance(results, dict):
                if not results.has_key('results'):
                    raise ValueError
                props = results
                results = props.pop('results')
            else:
                props = {}

            limit = self.data.limit_results
            if limit:
                results = results[:limit]
            results = self.wrap_results(results)
            return results, props

