from pirc522 import RFID
import os
import requests
import json
import time

rdr = RFID()
url = "http://pumpkin.international:8080/login"
headers = {'Content-Type': 'application/json'}
mac = os.popen('cat /sys/class/net/eth0/address').read().replace("\n", "")
users = {}

while True:
  os.system('python3 Display.py image loading')
  rdr.wait_for_tag()
  (error, tag_type) = rdr.request()

  if not error:
    print("Tag detected")
    (error, uid) = rdr.anticoll()

    if not error:
      print("UID: " + str(uid))
      response = requests.post(url, data = json.dumps({"rfid":str(uid), "macAddress":str(mac)}), headers = headers)

      if response.status_code == 200:
        
        if response.json().get("message") == "Login":
          os.system('python3 Display.py image success')
          os.system('python3 Display.py text Welcome ' + response.json().get("user"))
          users = {str(uid): time.time()}
        elif (response.json().get("message") == "Logout"):
          timestamp = time.time()
          if ((timestamp - users[str(uid)]) >= 30):
            os.system('python3 Display.py image success')
            os.system('python3 Display.py text Goodbye ' + response.json().get("user"))
          else:
            os.system('python3 Display.py text Wait ' + str((timestamp - users[str(uid)])) + "s")

      elif response.status_code == 403: 
        os.system('python3 Display.py image denied')
      elif response.status_code == 409:
        os.system('python3 Display.py text LoggedIn elsewhere')
      else:
        os.system('python3 Display.py image error')

# Calls GPIO cleanup
rdr.cleanup()