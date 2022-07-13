# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

__author__ = """Tobias Herp <tobias.herp@visaplan.com>"""

# PDFreactor (by RealObjects; Python integration by visaplan GmbH):
from pdfreactor.defaults import default_connection

# Zope:
from Missing import Value as MissingValue
from Products.CMFCore.utils import getToolByName
from zope.interface import implementer

# Plone:
from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFPlone.interfaces import INonInstallable

# visaplan:
from visaplan.plone.tools.setup import step

# Local imports:
from .interfaces import IPdfReactorConnectionSettings

# Logging / Debugging:
import logging

# ------------------------------------------------------- [ data ... [
PROJECTNAME = 'pdfreactor.plone'
PROFILE_ID = PROJECTNAME + ':default'
LOGGER_LABEL = PROJECTNAME + ': setuphandlers'
# ------------------------------------------------------- ] ... data ]

logger = logging.getLogger(LOGGER_LABEL)


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            PROJECTNAME + ':uninstall',
        ]


def post_install(context):
    """Post install script"""
    logger.info('Installing '+PROJECTNAME + ' ...')

    registry = getToolByName(context, 'portal_registry')
    registry.registerInterface(IPdfReactorConnectionSettings)
    logger.info('Registered interface %r', IPdfReactorConnectionSettings)
    proxy = registry.forInterface(IPdfReactorConnectionSettings)

    logger.info('Installation complete')

    # Do something at the end of the installation of this package.


@step
def register_settings(context, logger):
    """
    Initialize the connection settings to None

    The default values might change in some future PDFreactor release; so we
    don't "freeze" the values here ourselves.  This way, if the need arises
    to update the customized settings, the admin will know where to do it.
    """
    registry = getToolByName(context, 'portal_registry')

    registry.registerInterface(IPdfReactorConnectionSettings)
    logger.info('Registered interface %r', IPdfReactorConnectionSettings)
    proxy = registry.forInterface(IPdfReactorConnectionSettings)

    early_return = 0
    late_return = 1
    if early_return:
        return
    for key in default_connection.keys():
        val = getattr(proxy, key, None)
        if val not in (None, MissingValue):
            logger.info('Found %(key)s = %(val)r', locals())
        else:
            val = None
            setattr(proxy, key, val)
            logger.info('Set %(key)s to %(val)r', locals())


@step
def load_profile(context, logger):
    """
    (re-)load the migration profile
    """
    loadMigrationProfile(context, 'profile-'+PROFILE_ID)
