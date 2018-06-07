import numpy as np
import cv2
import sys

# Given a file path for a points file, return a list of rectangle corners
# No significant performance benefit to using numpy arrays here, so simplicity was preferred
def read_points(file_path):
	file = open(file_path, "r")
	data = []
	for line in file:
		parsed_line = line.strip().split(",")
		data.append([int(x) for x in parsed_line])
	file.close()
	return data
	

if __name__ == "__main__":

	# Check if all proper input arguments exist
	if len(sys.argv) != 3:
		print("Improper number of input arguments")
		print("USAGE: main.py <img> <mask points>")
		sys.exit()
		
	# Read in the image
	filename = sys.argv[1]
	img = cv2.imread(filename)
	img_marked = img.copy()

	# Parse the points file
	points = read_points(sys.argv[2])
	
	# Apply the bounding box
	# https://docs.opencv.org/trunk/dc/da5/tutorial_py_drawing_functions.html
	bounding_rect = tuple(points.pop(0))
	mask = np.zeros(img.shape[:2],np.uint8)
	bgdModel = np.zeros((1,65),np.float64)
	fgdModel = np.zeros((1,65),np.float64)
	cv2.grabCut(img, mask, (bounding_rect[0], bounding_rect[1], bounding_rect[2]-bounding_rect[0], bounding_rect[3] - bounding_rect[1]), bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

	# Apply any additional masking if specified in the input file
	if len(points) > 0:
		# Build mask matrix for all rectangles
		for point in points:
			type, x1, y1, x2, y2 = point
			mask[y1:y2, x1:x2] = type
			
		# Using the new mask with defined inner and outer rectangles, perform grabcut
		mask, bgdModel, fgdModel = cv2.grabCut(img, mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)
		
	# Apply the mask to the image
	mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
	img = img*mask[:,:,np.newaxis]

	# Mark up the image with rectangles specifying the bounding box and inner/outer rectangles
	cv2.rectangle(img_marked,(bounding_rect[0],bounding_rect[1]),(bounding_rect[2],bounding_rect[3]),(255,0,0),3)	
	for point in points:
		type, x1, y1, x2, y2 = point
		cv2.rectangle(img_marked,(x1,y1),(x2,y2),(0,255 * type, 255 * (1 - type)),3)
	
	
	# Determine output image paths
	index = filename.rfind('.')
	marked_filename = filename[:index] + '_marked' + filename[index:]
	result_filename = filename[:index] + '_result' + filename[index:]
	
	# Write output images
	cv2.imwrite(marked_filename, img_marked)
	cv2.imwrite(result_filename, img)