from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from zope.schema.vocabulary import SimpleVocabulary
from collective.portlet.pythonscript.content.interface import IPythonScriptManager

def PythonScriptsVocabFactory(context):
    """Produces Python Scripts vocabulary for given context."""
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    manager = IPythonScriptManager(portal)
    terms = [
        SimpleVocabulary.createTerm(name, name, script.title)
        for (name, script) in manager.getEnabledScripts()
    ]
    return SimpleVocabulary(terms)
