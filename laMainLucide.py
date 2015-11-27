from SimpleCV import Image, Display, DrawingLayer, Color, Camera
import time
import numpy as np
img = Image('stenramchiffontest.jpg')
disp = Display()
img_blurred = img.gaussianBlur((101,101))

# Make a mask
mask_size = 80
mask = Image((4*mask_size, 4*mask_size))
dl = DrawingLayer((4*mask_size, 4*mask_size))

# Draw a filled circle in the mask
dl.circle((2*mask_size,2*mask_size), mask_size, filled = True, color = Color.WHITE)
mask.addDrawingLayer(dl)
mask = mask.applyLayers()
blurred_mask = mask.gaussianBlur((101,101))
t0 = time.time()
	# Blur the mask to get progressive blur

n=3
img_ = img.gaussianBlur((n,n))
old_n = 3
isDown = False
mouseRawXOld = 0
x= 0
while not disp.isDone():
	t = time.time()
	dt = t-t0
	t0 = t
	mouseRawX = disp.mouseRawX
	if disp.mouseRawX==mouseRawXOld:
	  print x
	  x = np.amax([0, x-dt*80])
	else:
	  x = np.amin([x+np.abs(disp.mouseRawX-mouseRawXOld)/10, 30])
	mouseRawXOld = mouseRawX
	n = 2*int(x)+1
	if n!=old_n:
	  img_ = img.gaussianBlur((n,n))
	  old_n = n
	# Change the position of the mask at mouse position
	mask_in_place = Image(img.size()).blit(blurred_mask, pos=(disp.mouseRawX-2*mask_size,disp.mouseRawY-2*mask_size))
	# Paste the net image in the blurred image using alpha mask
	masked_image = img_blurred.blit(img_,  alphaMask = mask_in_place)
	masked_image.show()
	time.sleep(.01)

