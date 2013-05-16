from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser import BrowserView
from collective.portlet.pythonscript.content.interface import IPythonScriptManager
from Products.statusmessages.interfaces import IStatusMessage
from plone.protect import CheckAuthenticator, PostOnly

class RescanPythonScriptView(BrowserView):

    def __call__(self):
        """Rescan and redirect."""
        # Check against CSRF.
        CheckAuthenticator(self.request)
        PostOnly(self.request)

        manager = IPythonScriptManager(self.context)
        manager.rescanScripts()
        IStatusMessage(self.request).addStatusMessage(_(u'Rescanned'))
        self.request.response.redirect(self.context.absolute_url() + '/@@manage_pythonscript')