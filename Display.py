from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import ST7735
import sys
import time


display = ST7735.ST7735(port=1, cs=0, dc=23, backlight=None, rst=16, width=128, height=160, rotation=0, invert=False, offset_left=0, offset_top=0 )

if sys.argv[1] == 'image':
    
    if sys.argv[2]=='success':
        image = Image.open("images/success.png")
    elif sys.argv[2]=='denied':
        image = Image.open("images/denied.png")
    elif sys.argv[2]=='loading':
        image = Image.open("images/loading.png")
    else:
        image = Image.open("images/error.png")
    display.display(image)

elif sys.argv[1] == 'text':
    image = Image.new('RGB', (display.width, display.height))
    draw = ImageDraw.Draw(image)
    
    draw.text((4, 30), sys.argv[2],
    font=ImageFont.truetype("codec.ttf", 25), fill=(255, 255, 255))

    draw.text((4, 90), sys.argv[3]+'!',
    font=ImageFont.truetype("codec.ttf", 25), fill=(255, 255, 255))
    display.display(image)

time.sleep(2)