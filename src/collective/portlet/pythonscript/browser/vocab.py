from zope.schema.vocabulary import SimpleVocabulary
from zope.component import getAdapters
from zope.interface import Interface
from collective.portlet.pythonscript.browser.renderer import IResultsList, IResultsRenderer

def TemplatesVocabFactory(context):
    """Produces Python Scripts vocabulary for given context."""
    terms = [
        SimpleVocabulary.createTerm(name, name, u'%s (%s)' % (name, adapter.title))
        for name, adapter in getAdapters((IResultsList([]), context.REQUEST), IResultsRenderer)
    ]
    return SimpleVocabulary(terms)
