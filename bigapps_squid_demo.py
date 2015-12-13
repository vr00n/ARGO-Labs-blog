import picamera
import os
import time
from PIL import Image, ImageDraw, ImageFont
import datetime as dt
import matplotlib
# This is to limit matplotlib's functionality to display its plotting popup window
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# for the Accelerometer
from adxl345 import ADXL345
import subprocess

adxl345 = ADXL345()
reading_x =[]
reading_y =[]
reading_z =[]
now_ti = []
​
# This function reads from the Pi's accelerometer and plots the readings to a matplotlib graph. The plot is then saved as an image
def getAccel():
	axes = adxl345.getAxes(True)
	now_ti.append(dt.datetime.now())
	reading_x.append(axes['x'])
	reading_y.append(axes['y'])
	reading_z.append(axes['z'])
	plt.plot(now_ti,reading_x,color='r')
	plt.plot(now_ti,reading_y,color='b')
	plt.plot(now_ti,reading_z,color='g')
	plt.gcf().autofmt_xdate()
	plt.savefig('overlay.png', transparent=True)
# This is to superimpose ARGO's logo to the image. You will need to install Imagemagick to use the composite command
	args=['composite -geometry +220+160 ARGO_LOGO_white_BK.png overlay.png overlay.png']
# This is to run linux / unix commands from within a python script. Including shell=True ensures that you can run this as local user instead of root.This is a linux thing 
	subprocess.call(args,shell=True)
	
​
def main():
    # prep picamera
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.rotation   = 180
        camera.crop       = (0.0, 0.0, 1.0, 1.0)
​
        # display preview
        camera.start_preview()
​
        # continuously updates the overlayed layer and display stats
        overlay_renderer = None
        while True:
          getAccel()	
		      img = Image.open("overlay.png")
          pad = Image.new('RGB', (((img.size[0] + 31) // 32) * 32,((img.size[1] + 15) // 16) * 16,))	
		      pad.paste(img, (0, 0)
          if overlay_renderer:
            # This line updates the overlay
				    overlay_renderer.update(pad.tobytes())
		      else:
		        # This line generates the overlay
            overlay_renderer = camera.add_overlay(pad.tobytes(),layer=3,size=img.size,alpha=75);
​
if __name__ == '__main__':
    import sys
    try:
        main()
    except:
        print 'Unexpected error : ', sys.exc_info()[0], sys.exc_info()[1]
