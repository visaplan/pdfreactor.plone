"""
pdfreactor.plone.interfaces

For the IPdfReactorConversionSettings interface, see the pdfreactor.parsecfg package
"""

# PDFreactor (by RealObjects; Python integration by visaplan GmbH):
from pdfreactor.defaults import default_connection as conn

# Zope:
from zope import schema
from zope.interface import Interface

# Plone:
from plone.supermodel import model


# ------------------------ [ marker interfaces for browser views ... [
class IExporter(Interface):
    """
    For browser views to provide a PDF export of the given context
    """


class IAsynchronousExporter(Interface):
    """
    For browser views to provide an asynchronous PDF export of the given context

    This won't yield the PDF document directly but instead return some JSON
    data to access it once it is ready.
    """


class ICallbackMonitor(Interface):
    """
    For browser views to receive callback messages by asynchronous conversions.

    Might eg.g send mail to the requesting user
    or download the document from the PDFreactor service.
    """


class IGetPdfReactorConversionSettings(Interface):
    """
    Return a very basic, non-configurable config dict.
    """


class IGetPdfReactorMathjaxSettings(Interface):
    """
    Return a simple script, initializing 3 variables to configure MathJax
    """
# ------------------------ ] ... marker interfaces for browser views ]


class IPdfReactorConnectionSettings(model.Schema):
    """
    Configuration for the PDFreactor backend
    """
    service_url = schema.URI(
        title=u"URL of the PDFreactor service",
        default=conn['service_url'],
        description=(u'Adjust the address of your PDFreactor service here; '
            u'default value is %(service_url)r.'
            ) % conn)

    license_key = schema.ASCII(
        title=u"License key for the PDFreactor service",
        default=conn['license_key'],
        required=False,
        description=(u'Enter your license key here (some XML text "<license>...'
            u'</license>", containing a signature). '
            u'This is not strictly necessary, e.g. if the license is installed '
            u'on the server, or when evaluating.'
            ) % conn)

    api_key = schema.ASCIILine(
        title=u"API key for the PDFreactor service",
        default=conn['api_key'],
        required=False,
        description=(u'Not to be confused with the license key, '
        u'which is provided by RealObjects GmbH, '
        u'is the possible API key which can be defined in the service '
        u'installation. '
        u'This will be appended to the url when sending requests. '
        u'If you have a static key, you may configure it here.'
        ))
