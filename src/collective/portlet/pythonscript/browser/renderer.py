from zope.interface import Interface, implements, Attribute
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.browser.interfaces import IBrowserView

class IResultsList(Interface):
    """Interface for list of results to render in the portlet."""

class ResultsList(list):
    """Result list implementation."""
    implements(IResultsList)

class IResultsRenderer(IBrowserView):
    """Interface for results renderer."""

    def __call__(self):
        """Render results."""

class DefaultResultsRenderer(BrowserView):
    """Default results list renderer."""

    implements(IResultsRenderer)

    template = ViewPageTemplateFile('renderer.pt')

    def __call__(self):
        """Render results."""
        return self.template()
    
class AlternativeResultsRenderer(DefaultResultsRenderer):
    """Alternative list renderer."""
    
    template = ViewPageTemplateFile('alternative.pt')
