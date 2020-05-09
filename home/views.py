from django.shortcuts import redirect, render
import socket
from .models import Device, Setup,Zone, Value
from django.views.decorators.cache import never_cache

from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect,  JsonResponse
from urllib.request import urlopen
import xmltodict
import os
from django.contrib import messages

from xml.etree.ElementTree import parse
from collections import OrderedDict
msg = \
    'M-SEARCH * HTTP/1.1\r\n' \
    'HOST:239.255.255.250:1900\r\n' \
    'ST:upnp:rootdevice\r\n' \
    'MX:2\r\n' \
    'MAN:"ssdp:discover"\r\n' \
    '\r\n'

# Create your views here.
@never_cache
def homepage(request):
    devices = Device.objects.all()

    zones = Zone.objects.all()
    labels = []
    data = []
    queryset = Value.objects.filter()
    for city in queryset:
        labels.append(city.last_measured_moisture)
        date= str((city.last_measured).strftime("%Y/%m/%dT%H:%M:00"))
        data.append(date)
    return render(request, 'home.html', {'devices': devices , 'zones':zones, 'labels': labels,
        'data': data})

@never_cache
def connect(request):

    return render(request, 'connect.html')
@never_cache
def editzone(request):
    devices = Zone.objects.all()

    return render(request, 'edit_zone.html', {'devices': devices })

@never_cache
def listzone(request):
    devices = Zone.objects.all()
    labels = []
    data = []
    queryset = Value.objects.filter()
    for city in queryset:
        labels.append(city.last_measured_moisture)
        date= str((city.last_measured).strftime("%Y/%m/%dT%H:%M:00"))
        data.append(date)
    print(data)
    return render(request, 'list_zone.html', {'zones': devices, 'labels': labels,
        'data': data})

@never_cache
def disconnect(request):
    devices = Device.objects.all()

    return render(request, 'disconnect.html', {'devices': devices })

@never_cache
def deletezone(request):
    name = request.GET.get('zone_id')

    devices = Zone.objects.get(pk=name)
    devices.delete()
    return redirect('/list_zone')

@never_cache
def listdevices(request):
    devices = Device.objects.all()

    return render(request, 'listdevices.html', {'devices': devices })



@never_cache
def createzone(request):
    devices = Device.objects.all()

    return render(request, 'create_zone.html', {'devices': devices })


def editzoneform(request):

    zone_name= request.GET.get('device_id')
    zones = Zone.objects.get(name=zone_name)
    devices = Device.objects.all()
    print(zone_name,zones)
    html = render_to_string('edit_zone_form.html', {'devices': devices,'zone': zones })
    return HttpResponse(html)


def savestatus(request):

    names= request.GET.getlist('zone_id')
    for name in names:
        zone = Zone.objects.get(pk=name)
        zone.monitoring= True
        zone.save()

    print(names)
    return redirect('/')

@never_cache
def getdevices(request):
    device = {}

    dictionary = {}
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.settimeout(2)
    s.sendto(msg.encode(), ('239.255.255.250', 1900) )
    try:
        while True:
            data, addr = s.recvfrom(65507)

            print(addr[0])
            if "Philips" in data.decode("utf-8"):
                print("True")
                file = urlopen('http://'+addr[0]+'/description.xml')
                data = file.read()
                file.close()

                data = xmltodict.parse(data)
                device= (data["root"])["device"]
                print(((data["root"])["device"])["friendlyName"])
                try:
                    obj2 = Device.objects.get(title=((data["root"])["device"])["friendlyName"])

                except Device.DoesNotExist:
                    newdict= dict(device)
                    dictionary[addr[0]]= newdict
            else:
                print("false")
    except socket.timeout:
        pass
    html = render_to_string('ajaxupdate.html', {'device': dictionary })
    return HttpResponse(html)

@never_cache
def savemanually(request):
    try:

        ipaddress = request.POST.get('ip_address')

        file = urlopen('http://'+ipaddress+'/description.xml')
        data = file.read()
        file.close()

        data = xmltodict.parse(data)
        device= (data["root"])["device"]
        user = Device.objects.create(title=((data["root"])["device"])["friendlyName"], ipaddress=ipaddress)
        user.save()
        cmd= "curl -i -X POST -d '{\"id\":1, \"gpio\":12,\"status\":0, \"waterduration\": 8000}\' http://" + ipaddress+ ":800/leds"
        os.system(cmd)
        messages.success(request, 'Successfully connected to device.')

        return HttpResponseRedirect('/connect')


    except  Exception as e:
        messages.error(request, ' An error occured. Please try again.' + str(e))
        return HttpResponseRedirect('/connect')


@never_cache
def savedevice(request):
    try:
        name= request.GET.get('device_name')
        ipaddress = request.GET.get('ip_address')
        user = Device.objects.create(title=name, ipaddress=ipaddress)
        user.save()
        cmd= "curl -i -X POST -d '{\"id\":1, \"gpio\":12,\"status\":0, \"waterduration\": 8000}\' http://" + ipaddress+ ":800/leds"
        os.system(cmd)
        messages.success(request, 'Successfully connected to device.')

        return HttpResponseRedirect('/connect')


    except:
        messages.error(request, 'An error occured. Please try again.')
        return HttpResponseRedirect('/connect')


@never_cache
def disconnectdevice(request):
    try:
        devices= request.GET.getlist('device_id[]')
        if len(devices) == 0:
            return JsonResponse({'error':"Please select atleast a device"})
            print(devices)
        else:
            for dev in devices:
                print(dev)
                obj_device= Device.objects.get(pk=dev)
                obj_device.delete()
        return JsonResponse({'success':True})

    except Exception as e:
        return JsonResponse({'error':str(e)})



def createzoneget(request):
    if request.method == 'GET':
        try:
            devices= request.GET.get('device_id')

            zone_name= request.GET.get('zone_name')
            watering_time= request.GET.get('watering_time')
            soil_moisture= request.GET.get('soil_moisture')
            gpio_pin= request.GET.get('gpio_pin')
            obj_device= Device.objects.get(title=devices)
            zone_obj= Zone.objects.create(device_id=obj_device,name=zone_name,min_moisture=soil_moisture,
            time_period=watering_time,gpio=gpio_pin,setupcompleted=True)
            zone_obj.save()

            print(devices, zone_name, watering_time,soil_moisture, gpio_pin)
            return JsonResponse({'success':True})
        except Exception as e:
            return JsonResponse({'error':str(e)})


def editzoneget(request):
    if request.method == 'GET':
        try:
            devices= request.GET.get('device_id')

            zone_name= request.GET.get('zone_name')
            watering_time= request.GET.get('watering_time')
            soil_moisture= request.GET.get('soil_moisture')
            gpio_pin= request.GET.get('gpio_pin')
            obj_device= Device.objects.get(title=devices)
            zone_obj= Zone.objects.get(device_id=obj_device)
            zone_obj.name=zone_name
            zone_obj.min_moisture=soil_moisture
            zone_obj.time_period=watering_time
            zone_obj.gpio=gpio_pin

            zone_obj.save()

            print(devices, zone_name, watering_time,soil_moisture, gpio_pin)

            return JsonResponse({'success':True})
        except Exception as e:
            print("error afssssafffffff")
            return JsonResponse({'error':str(e)})
def settimeperiod(request):
    if request.method == 'POST':
        try:
            id = request.POST.get('device_id')
            timeperiods = request.POST.get('timeperiods')
            buttonpressed = request.POST.get('deviceselect')
            print(id, timeperiods, buttonpressed)
            cronnamer= Device.objects.get(pk=id)
            lowercase = (buttonpressed.lower()).replace(" ", "_")

            print(lowercase)

               # person just refers to the existing one
            if buttonpressed=="Time 1" :
                person, created = Setup.objects.get_or_create(device_id= Device.objects.get(pk=id))

                if created:
                    print("created")
                    person.time_1 = timeperiods
                    person.save()

                else:
                    print("no")
                    person.time_1 = timeperiods
                    person.save()
                print("startcd is s")

            elif buttonpressed=="Time 2":
                person, created = Setup.objects.get_or_create(device_id= Device.objects.get(pk=id))

                if created:
                    print("created")
                    person.time_2 = timeperiods
                    person.save()

                else:
                    print("no")
                    person.time_2 = timeperiods
                    person.save()
                print("stopcd")

            elif buttonpressed=="Time 3":
                person, created = Setup.objects.get_or_create(device_id= Device.objects.get(pk=id))

                if created:
                    print("created")
                    person.time_3 = timeperiods
                    person.save()

                else:
                    print("no")
                    person.time_3 = timeperiods
                    person.save()
                print("startcd is s")

            elif buttonpressed=="Time 4":
                person, created = Setup.objects.get_or_create(device_id= Device.objects.get(pk=id))

                if created:
                    print("created")
                    person.time_4 = timeperiods
                    person.save()

                else:
                    print("no")
                    person.time_4 = timeperiods
                    person.save()
            elif buttonpressed=="Time 5":
                person, created = Setup.objects.get_or_create(device_id= Device.objects.get(pk=id))

                if created:
                    print("created")
                    person.time_5 = timeperiods
                    person.save()

                else:
                    print("no")
                    person.time_5 = timeperiods
                    person.save()
            elif buttonpressed=="Time 6":
                person, created = Setup.objects.get_or_create(device_id= Device.objects.get(pk=id))

                if created:
                    print("created")
                    person.time_6 = timeperiods
                    person.save()

                else:
                    print("no")
                    person.time_6 = timeperiods
                    person.save()
            elif buttonpressed=="Time 7":
                person, created = Setup.objects.get_or_create(device_id= Device.objects.get(pk=id))

                if created:
                    print("created")
                    person.time_7 = timeperiods
                    person.save()

                else:
                    print("no")
                    person.time_7 = timeperiods
                    person.save()
            elif buttonpressed=="Time 8":
                person, created = Setup.objects.get_or_create(device_id= Device.objects.get(pk=id))

                if created:
                    print("created")
                    person.time_8 = timeperiods
                    person.save()

                else:
                    print("no")
                    person.time_8 = timeperiods
                    person.save()
            elif buttonpressed=="Time 9":
                person, created = Setup.objects.get_or_create(device_id= Device.objects.get(pk=id))

                if created:
                    print("created")
                    person.time_9 = timeperiods
                    person.save()

                else:
                    print("no")
                    person.time_9 = timeperiods
                    person.save()
            elif buttonpressed=="Time 10":
                person, created = Setup.objects.get_or_create(device_id= Device.objects.get(pk=id))

                if created:
                    print("created")
                    person.time_10 = timeperiods
                    person.save()

                else:
                    print("no")
                    person.time_10 = timeperiods
                    person.save()
            messages.success(request, 'Profile details updated.')

            return HttpResponseRedirect('/list_devices')


        except:
            messages.error(request, 'An error occured. PLease try again.')
            return HttpResponseRedirect('/list_devices')
