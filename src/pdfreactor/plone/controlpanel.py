from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from pdfreactor.plone.interfaces import IPdfReactorConnectionSettings
from plone.z3cform import layout
from z3c.form import form

class ConnectionControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IPdfReactorConnectionSettings

ConnectionControlPanelView = layout.wrap_form(ConnectionControlPanelForm, ControlPanelFormWrapper)
ConnectionControlPanelView.label = u"PDFreactor Connection settings"
