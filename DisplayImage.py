from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import ST7735
import sys
import time


display = ST7735.ST7735(port=1, cs=0, dc=23, backlight=None, 
rst=16, width=128, height=160, rotation=0, invert=False, 
offset_left=0, offset_top=0 )


if sys.argv[1]=='success':
    image = Image.open("success.png")

elif sys.argv[1]=='denied':
    image = Image.open("denied.png")

elif sys.argv[1]=='loading':
    image = Image.open("loading.png")

else:
    image = Image.open("error.png")


display.display(image)
time.sleep(1)