from pirc522 import RFID
import os
import requests
import json
import datetime

rdr = RFID()
urlLogin = "http://pumpkin.international:8080/login"
urlIsLoggedIn = "http://pumpkin.international:8080/isLoggedIn"
headers = {'Content-Type': 'application/json'}
mac = os.popen('cat /sys/class/net/eth0/address').read().replace("\n", "")
format = '%Y-%m-%d %H:%M:%S'

while True:
  os.system('python3 Display.py image loading')
  rdr.wait_for_tag()
  (error, tag_type) = rdr.request()

  if not error:
    print("Tag detected")
    (error, uid) = rdr.anticoll()

    if not error:
      print("UID: " + str(uid))
      response = requests.get(urlIsLoggedIn, data = json.dumps({"rfid":str(uid)}), headers = headers)
      if response.json().get("loggedIn") == False:
        response = requests.post(urlLogin, data = json.dumps({"rfid":str(uid), "macAddress":str(mac)}), headers = headers)
        if response.status_code == 200:
          if response.json().get("message") == "Login":
            os.system('python3 Display.py image success')
            os.system('python3 Display.py text Welcome ' + response.json().get("user"))


      elif response.json().get("loggedIn") == True:
        time = datetime.datetime.strptime(response.json().get("lastLogin"), format)
        delta = datetime.datetime.now() - time
        seconds = int(delta.total_seconds())
        if seconds >= 30:
          response = requests.post(urlLogin, data = json.dumps({"rfid":str(uid), "macAddress":str(mac)}), headers = headers)
          os.system('python3 Display.py image success')
          os.system('python3 Display.py text Goodbye ' + response.json().get("user"))
        else:
          os.system('python3 Display.py text Wait ' + str(30 - seconds) + 's')

      elif response.status_code == 403: 
        os.system('python3 Display.py image denied')
      elif response.status_code == 409:
        os.system('python3 Display.py text LoggedIn elsewhere')
      else:
        os.system('python3 Display.py image error')

# Calls GPIO cleanup
rdr.cleanup()