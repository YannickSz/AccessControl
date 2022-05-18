import os
from pirc522 import RFID
import requests

rdr = RFID()
url = "http://pumpkin.international:8080/login"
headers = {'Content-Type': 'application/json'}
mac = os.popen('cat /sys/class/net/eth0/address').read()
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
      response = requests.post(url, data = {'rfid':uid, 'macAddress':mac}, headers = headers)
      print(response.status_code)
      print(mac)
      print(uid)
      if response.status_code == 200:
        os.system('python3 DisplayImage.py success')

        if isLoggedIn:
          os.system('python3 Display.py Welcome Serdar')
        else:
          os.system('python3 Display.py Goodbye Serdar')
          
      else: 
        os.system('python3 DisplayImage.py denied')


# Calls GPIO cleanup
rdr.cleanup()