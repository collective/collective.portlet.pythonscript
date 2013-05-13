from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from zope.schema.interfaces import IVocabulary
from zope.schema.vocabulary import SimpleVocabulary
from collective.portlet.pythonscript.content.scriptmanager import IPythonScriptManager

def getPythonScriptsVocab(context):
    """Return vocabulary of Python Scripts."""
    manager = IPythonScriptManager(context)
    terms = [SimpleVocabulary.createTerm(name, name, script.title)
             for (name, script) in manager]
    return SimpleVocabulary(terms)

def PythonScriptsVocabFactory(context):
    """Produces Python Scripts vocabulary for given context."""
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    manager = IPythonScriptManager(portal)
    terms = [SimpleVocabulary.createTerm(name, name, script.title)
             for (name, script) in manager.getScripts()]
    return SimpleVocabulary(terms)
