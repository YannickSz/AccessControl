from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import ST7735
import sys


display = ST7735.ST7735(port=1, cs=0, dc=23, backlight=None, rst=16, width=128, height=160, rotation=0, invert=False, offset_left=0, offset_top=0 )

image = Image.new('RGB', (display.width, display.height))
draw = ImageDraw.Draw(image)


#print (len(sys.argv))


if len(sys.argv) < 2:
    print ("Usage: Display.py <TEXT>")
    sys.exit()


draw.text((4, 30), sys.argv[1],
font=ImageFont.truetype("codec.ttf", 25), fill=(255, 255, 255))


draw.text((4, 90), sys.argv[2]+'!',
font=ImageFont.truetype("codec.ttf", 25), fill=(255, 255, 255))
display.display(image)