from zope.interface import implements
from collective.portlet.pythonscript.content.interface import IPythonScriptPortletItem

class CatalogBrainPythonScriptPortletAdapter(object):
    """Adapter for portal catalog brains into renderable portlet items."""

    implements(IPythonScriptPortletItem)

    def __init__(self, context):
        """Context is Products.ZCatalog.interfaces.ICatalogBrain"""
        self.context = context

    @property
    def title(self):
        """Get brain title."""
        return self.context.Title

    @property
    def url(self):
        """Get brain url."""
        return self.context.getURL()