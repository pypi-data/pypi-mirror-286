"""Radicale management frontend."""

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy

from kalabash.core.extensions import KbashExtension, exts_pool
from kalabash.parameters import tools as param_tools

from . import __version__
from . import forms


class Radicale(KbashExtension):
    """Radicale extension declaration."""

    name = "kalabash_radicale"
    label = gettext_lazy("Radicale management")
    topredirection_url = reverse_lazy("kalabash_radicale:index")
    version = __version__
    url = "calendars"
    description = gettext_lazy(
        "Management frontend for Radicale, a simple calendar and contact "
        "server."
    )

    def load(self):
        """Plugin loading."""
        param_tools.registry.add(
            "global", forms.ParametersForm, "Radicale")

exts_pool.register_extension(Radicale)
