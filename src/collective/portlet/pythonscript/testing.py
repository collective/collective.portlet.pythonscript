from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import collective.portlet.pythonscript


COLLECTIVE_PORTLET_PYTHONSCRIPT = PloneWithPackageLayer(
    zcml_package=collective.portlet.pythonscript,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.portlet.pythonscript:testing',
    name="COLLECTIVE_PORTLET_PYTHONSCRIPT")

COLLECTIVE_PORTLET_PYTHONSCRIPT_INTEGRATION = IntegrationTesting(
    bases=(COLLECTIVE_PORTLET_PYTHONSCRIPT, ),
    name="COLLECTIVE_PORTLET_PYTHONSCRIPT_INTEGRATION")

COLLECTIVE_PORTLET_PYTHONSCRIPT_FUNCTIONAL = FunctionalTesting(
    bases=(COLLECTIVE_PORTLET_PYTHONSCRIPT, ),
    name="COLLECTIVE_PORTLET_PYTHONSCRIPT_FUNCTIONAL")
