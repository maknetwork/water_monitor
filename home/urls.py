from django.urls import path
from . import views
from django.conf.urls import url
import socket
from urllib.request import urlopen
import xmltodict

from xml.etree.ElementTree import parse

msg = \
    'M-SEARCH * HTTP/1.1\r\n' \
    'HOST:239.255.255.250:1900\r\n' \
    'ST:upnp:rootdevice\r\n' \
    'MX:2\r\n' \
    'MAN:"ssdp:discover"\r\n' \
    '\r\n'
app_name = 'blog'
urlpatterns = [
# post views
path('', views.homepage, name='homepage'),
path('connect', views.connect, name='connect'),
path('getdevices', views.getdevices, name='getdevices'),
                url(r'^save_device/$', views.savedevice, name='save_device'),
path('list_devices', views.listdevices, name='listdevices'),
path('disconnect', views.disconnect, name='disconnect'),
path('edit_zone', views.editzone, name='edit_zone'),

path('list_zone', views.listzone, name='list_zone'),
path('delete_zone', views.deletezone, name='deletezone'),

path('create_zone', views.createzone, name='create_zone'),
                url('delete_zone', views.deletezone, name='deletezone'),

                url(r'^create_zone_get/$', views.createzoneget, name='createzoneget'),
                url(r'^edit_zone_form/$', views.editzoneform, name='edit_zone_form'),
                url(r'^edit_zone_get/$', views.editzoneget, name='edit_zone_get'),
path('save_manually', views.savemanually, name='save_manually'),

                url(r'^disconnect_device/$', views.disconnectdevice, name='disconnect_device'),
                url(r'^set_timeperiod/$', views.settimeperiod, name='set_timeperiod'),

                url(r'^save_status/$', views.savestatus, name='save_status'),

]
