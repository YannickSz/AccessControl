from pirc522 import RFID
import os
import requests
import json

rdr = RFID()
url = "http://pumpkin.international:8080/login"
headers = {'Content-Type': 'application/json'}
mac = os.popen('cat /sys/class/net/eth0/address').read().replace("\n", "")
isLoggedIn = True

while True:
  os.system('python3 DisplayImage.py loading')
  rdr.wait_for_tag()
  (error, tag_type) = rdr.request()

  if not error:
    print("Tag detected")
    (error, uid) = rdr.anticoll()

    if not error:
      print("UID: " + str(uid))
      response = requests.post(url, data = json.dumps({"rfid":str(uid), "macAddress":str(mac)}), headers = headers)

      if response.status_code == 200:
        os.system('python3 DisplayImage.py success')
        if response.json().get("message") == "Login":
          os.system('python3 Display.py Welcome ' + response.json().get("user"))
        elif response.json().get("message") == "Logout":
          os.system('python3 Display.py Goodbye ' + response.json().get("user"))

      elif response.status_code == 403: 
        os.system('python3 DisplayImage.py denied')
      elif response.status_code == 409:
        os.system('python3 Display.py LoggedIn elsewhere')
      else:
        os.system('python3 DisplayImage.py error')

# Calls GPIO cleanup
rdr.cleanup()