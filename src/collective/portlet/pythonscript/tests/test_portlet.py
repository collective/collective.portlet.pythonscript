from plone.portlets.interfaces import IPortletType, IPortletAssignment,\
    IPortletDataProvider, IPortletManager, IPortletRenderer
from zope.component import getUtility, getMultiAdapter
from plone.testing import z2
from plone.app.portlets.storage import PortletAssignmentMapping

from collective.portlet.pythonscript.tests.base import TestBase
from collective.portlet.pythonscript.browser.portlet import PythonScriptPortletAssignment,\
    PythonScriptPortletEditForm, PythonScriptPortletRenderer
from collective.portlet.pythonscript.content.interface import IPythonScriptManager

class TestPortlet(TestBase):
    """Test script portlet."""
    
    PORTLET_NAME = 'collective.portlet.PythonScript'
    
    def setUp(self):
        """Login as manager."""
        super(TestPortlet, self).setUp()
        z2.login(self.app['acl_users'], 'admin')
        self.addPythonScript('first', u'First', 'return []')
        self.addPythonScript('second', u'Second', 'return []')
        self.addPythonScript('third', u'Third', 'return []')
        manager = IPythonScriptManager(self.portal)
        manager.rescanScripts()
        manager.enableScript('/plone/second')
        manager.enableScript('/plone/third')
    
    def tearDown(self):
        """Logout."""
        super(TestPortlet, self).tearDown()
        z2.logout()

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name=self.PORTLET_NAME)
        self.assertEquals(portlet.addview, self.PORTLET_NAME)

    def testInterfaces(self):
        portlet = PythonScriptPortletAssignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portlet = getUtility(IPortletType, name=self.PORTLET_NAME)
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={
            'portlet_title': 'My Portlet',
            'script_name': '/plone/third',
            'limit_results': None
        })

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], PythonScriptPortletAssignment))

    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.portal.REQUEST

        mapping['foo'] = PythonScriptPortletAssignment(portlet_title=u"My Portlet", script_name="/plone/third", limit_results=None)
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, PythonScriptPortletEditForm))

    def testRenderer(self):
        context = self.portal
        request = self.portal.REQUEST
        view = self.portal.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = PythonScriptPortletAssignment(portlet_title=u"My Portlet", script_name="/plone/third", limit_results=None)

        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, PythonScriptPortletRenderer))

        self.failUnless(renderer.available,
            "Renderer should be available by default.")
