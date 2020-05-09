from celery.decorators import task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from .models import Device, Setup, Zone, Value
from urllib.request import urlopen
import json
import os
from datetime import datetime
import subprocess
now = datetime.now()
logger = get_task_logger(__name__)
current_time = now.strftime("%H:%M")
print("Current Time =", current_time)

@periodic_task(run_every=(crontab(minute='*/1')), name="hello", ignore_result=False)
def hello():
    devicess= Setup.objects.all()

    """sends an email when feedback form is filled successfully"""
    for dev in devicess:
        times = []
        if dev.time_1 is not None:
            times.append(dev.time_1.strftime("%H:%M"))
        if dev.time_2 is not None:
            times.append(dev.time_2.strftime("%H:%M"))

        if dev.time_3 is not None:
            times.append(dev.time_3.strftime("%H:%M"))
        if dev.time_4 is not None:
            times.append(dev.time_4.strftime("%H:%M"))
        if dev.time_5 is not None:
            times.append(dev.time_5.strftime("%H:%M"))
        if dev.time_6 is not None:
            times.append(dev.time_6.strftime("%H:%M"))
        if dev.time_7 is not None:
            times.append(dev.time_7.strftime("%H:%M"))
        if dev.time_8 is not None:
            times.append(dev.time_8.strftime("%H:%M"))

        if dev.time_9 is not None:
            times.append(dev.time_9.strftime("%H:%M"))
        if dev.time_10 is not None:
            times.append(dev.time_10.strftime("%H:%M"))
        print(times)
        if (datetime.now()).strftime("%H:%M") in times:
            print("its time")
            obj_device= Device.objects.get(id=dev.pk)
            p = subprocess.Popen(['ping',obj_device.ipaddress,'-c','1',"-W","2"])
            if p.poll():
                print("no packet transmitted")
                obj_device.connected= False
                obj_device.last_seen= datetime.now()

                obj_device.save()



            else:

                cmd= "curl -i -X POST -d '{\"id\":1, \"gpio\":16,\"status\":0, \"waterduration\": 8000}\' http://" + obj_device.ipaddress+ ":800/leds"
                os.system(cmd)
                file = urlopen('http://'+obj_device.ipaddress+':800/leds')
                data = file.read()
                file.close()
                y = json.loads(data)
                print(y["waterduration"],y["id"])
                obj_device.connected= True
                obj_device.last_seen= datetime.now()

                obj_device.save()
                try:
                    obj2 = Zone.objects.get(pk=obj_device)
                    if obj2.monitoring:

                        obj3 = Value.objects.create(device_id=obj_device,last_measured_moisture=y["waterreading"] ,last_measured= datetime.now())
                        obj3.save()
                        obj2.last_measured_moisture= y["waterreading"]
                        obj2.last_measured= datetime.now()
                        if y["waterreading"] <=obj2.min_moisture:
                            print("turned on")
                            cmd= "curl -i -X PUT -d '{\"id\":1, \"gpio\":"+obj2.gpio  + ",\"status\":1, \"waterduration\": "  + str(obj2.time_period)+ "}' http://" + obj_device.ipaddress+ ":800/leds"
                            os.system(cmd)
                            obj2.last_active_moisture= y["waterreading"]
                            obj2.last_active_measured= datetime.now()
                            print("turned on")


                        else:

                            print("off")
                        obj2.save()

                        print("exists")
                    else:
                        print("monitoring not enabled")

                except Zone.DoesNotExist:
                    print("does not exist")

                print(data)
                print((datetime.now()).strftime("%H:%M"),(dev.time_1).strftime("%H:%M"))
        else:
            print("not time")

hello()
