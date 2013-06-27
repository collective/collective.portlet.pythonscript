from zope.interface import Interface, implements, Attribute
from zope.publisher.browser import BrowserView
from zope.app.pagetemplate import ViewPageTemplateFile

class IResultsList(Interface):
    """Interface for list of results to render in the portlet."""

class ResultsList(list):
    """Result list implementation."""
    implements(IResultsList)

class DefaultResultsRenderer(BrowserView):
    """Default results list renderer."""

    index = ViewPageTemplateFile('renderer.pt')
