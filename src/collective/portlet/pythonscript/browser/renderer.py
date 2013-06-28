from zope.interface import Interface, implements, Attribute
from zope.publisher.browser import BrowserView
from zope.browser.interfaces import IBrowserView
from Products.CMFPlone import PloneMessageFactory as _
try:
    from zope.app.pagetemplate import ViewPageTemplateFile
except ImportError:
    # In Plone 4.3 module name changed.
    from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

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

    def __call__(self, results):
        """Render results."""
        return self.template(results=results)

class AlternativeResultsRenderer(DefaultResultsRenderer):
    """Alternative list renderer."""
    
    title = _(u"No links template")

    template = ViewPageTemplateFile('alternative.pt')
