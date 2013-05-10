import persistent
from zope.interface import Interface, implements
from zope.schema import TextLine, Text, Bool
from zope.schema.fieldproperty import FieldProperty
from zope.container import contained
from plone.app.content.interfaces import INameFromTitle

class IPythonScript(Interface):
    """Interface for Python Script objects."""
    
    title = TextLine(
        title=u"Script title",
        description=u"",
        default=u"",
        required=True
    )
    enabled = Bool(
        title=u'If script is enabled for use in portlets',
        description=u"",
        default=False,
        required=False
    )
    code = Text(
        title=u'Python code of the script',
        description=u"Code to be executed by the script. Needs to return an iterable of portal_catalog brains.""",
        default=u"",
        required=True
    ) # TODO: constraint on syntax

class PythonScript(persistent.Persistent):
    """Python Script object."""
    
    implements(IPythonScript, INameFromTitle)
    
    # Default values of attributes.
    title = FieldProperty(IPythonScript['title'])
    enabled = FieldProperty(IPythonScript['enabled'])
    code = FieldProperty(IPythonScript['code'])
