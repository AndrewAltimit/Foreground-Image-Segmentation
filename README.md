# Overview
Foreground image segmentation using Python and OpenCV. See the uploaded PDF for implementation details and experimental results. Examples used in the paper can be found in the examples directory with their corresponding source images and mask definitions.

## Prerequisites
* Python 3.* https://www.python.org/download/
* Numpy
* OpenCV 3.*

## Usage

***Defining the Mask***

The mask file should consist of rectangle definitions in the form: top left x, top left y, bottom right x, bottom right y. The first line defines the bounding box and all other lines define known foreground and background areas. These definitions should be proceeded with a 0 (background) or a 1 (foreground).

***Example Mask***

	36,76,831,785
	0,42,76,345,261
	
Area of interest (all else is background): (36,76) (831,785)

Additional Background: (42,76) (345,261)


***Performing a Cut***

	main.py <source image> <mask file>

