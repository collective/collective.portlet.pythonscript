from zope.interface import Interface, implements, Attribute
from zope.publisher.browser import BrowserView
from zope.browser.interfaces import IBrowserView
from Products.CMFPlone import PloneMessageFactory as _
try:
    from zope.app.pagetemplate import ViewPageTemplateFile
except ImportError:
    # In Plone 4.3 module name changed.
    from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

class IResultsList(Interface):
    """Interface for list of results to render in the portlet."""

class ResultsList(list):
    """Result list implementation."""
    implements(IResultsList)

class IResultsRenderer(IBrowserView):
    """Interface for results renderer."""

    title = Attribute(u"Displayable name of the template")

    def __call__(self, results):
        """Render results."""

class DefaultResultsRenderer(BrowserView):
    """Default results list renderer."""

    title = _(u"Default template")

    implements(IResultsRenderer)

    template = ViewPageTemplateFile('renderer.pt')

    def __call__(self):
        """Render results."""
        return self.template()

class AlternativeResultsRenderer(DefaultResultsRenderer):
    """Alternative list renderer."""
    
    title = _(u"No links template")

    template = ViewPageTemplateFile('alternative.pt')
