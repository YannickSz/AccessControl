from pirc522 import RFID
import os
import requests
import json
import datetime
import pigpio
import time as t
import simplejson

rdr = RFID()
urlLogin = "http://pumpkin.international:8080/login"
urlIsLoggedIn = "http://pumpkin.international:8080/isLoggedIn"
headers = {'Content-Type': 'application/json'}
mac = os.popen('cat /sys/class/net/eth0/address').read().replace("\n", "")
format = '%Y-%m-%d %H:%M:%S'
pi = pigpio.pi()

# gpio 13 left
# gpio 19 right
def wantToLogOut():
  os.system('python3 Display.py image logout')
  while True:
    if pi.read(13) == 1:
      return True
    if pi.read(19) == 1:
      return False
    t.sleep(0.01)

while True:
  os.system('python3 Display.py image loading')
  rdr.wait_for_tag()
  (error, tag_type) = rdr.request()

  if not error:
    print("Tag detected")
    (error, uid) = rdr.anticoll()

    if not error:
      print("UID: " + str(uid))
      try:
        response = requests.get(urlIsLoggedIn, data = json.dumps({"rfid":str(uid)}), headers = headers)
        response.json() 
      except requests.exceptions.ConnectionError:
        os.system('python3 Display.py text Server Offline')
        continue
      except simplejson.errors.JSONDecodeError:
        os.system('python3 Display.py image denied')
        continue
      if response.json().get("loggedIn") == True:
        time = datetime.datetime.strptime(response.json().get("lastLogin"), format)
        delta = datetime.datetime.now() - time
        seconds = int(delta.total_seconds())
        if seconds >= 30:
          if wantToLogOut() == False:
            continue
          response = requests.post(urlLogin, data = json.dumps({"rfid":str(uid), "macAddress":str(mac)}), headers = headers)
          if response.status_code == 200:
            if response.json().get("message") == "Logout":
              os.system('python3 Display.py image success')
              os.system('python3 Display.py text Goodbye ' + response.json().get("user"))
          elif response.status_code == 403: 
            os.system('python3 Display.py image denied')
          elif response.status_code == 409:
            os.system('python3 Display.py text LoggedIn elsewhere')
          else:
            os.system('python3 Display.py image error')
        else:
          os.system('python3 Display.py text Wait ' + str(30 - seconds) + 's')
      else:
        response = requests.post(urlLogin, data = json.dumps({"rfid":str(uid), "macAddress":str(mac)}), headers = headers)
        if response.status_code == 200:
          if response.json().get("message") == "Login":
            os.system('python3 Display.py image success')
            os.system('python3 Display.py text Welcome ' + response.json().get("user"))
        elif response.status_code == 403: 
          os.system('python3 Display.py image denied')
        elif response.status_code == 409:
          os.system('python3 Display.py text LoggedIn elsewhere')
        else:
          os.system('python3 Display.py image error')

# Calls GPIO cleanup
rdr.cleanup()
  