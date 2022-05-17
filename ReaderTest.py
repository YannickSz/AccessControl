import os
from pirc522 import RFID

rdr = RFID()
mac = os.system('cat /sys/class/net/eth0/address')

while True:
  os.system('python3 DisplayImage.py loading')
  rdr.wait_for_tag()
  (error, tag_type) = rdr.request()

  if not error:
    print("Tag detected")
    (error, uid) = rdr.anticoll()

    if not error:
      print("UID: " + str(uid))

      if uid==[26, 198, 157, 26, 91]:
        os.system('python3 DisplayImage.py success')
        os.system('python3 Display.py Serdar')

      else: 
        os.system('python3 DisplayImage.py denied')


# Calls GPIO cleanup
rdr.cleanup()