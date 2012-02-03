from django.conf.urls.defaults import *
from notas.pucrs import parse_pucrs
from notas.ulbra import parse_ulbra

urlpatterns = patterns('',
    (r'^notas/ulbra/(.[^/]+)/(.[^/]+)/$', parse_ulbra),
    (r'^notas/pucrs/(.[^/]+)/(.[^/]+)/$', parse_pucrs),
)
