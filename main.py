from most_important import mostImportantFormat
from important import importantFormat 
from good_to_have import goodToHaveFormat
from least_important import leastImportantFormat

from pdf2image import convert_from_path 
from PIL import Image 

import pytesseract
import os 
import cv2

def detectFormat(filename):
	try:
		# Path of the pdf 
		dir_path = os.path.join(os.path.dirname(os.path.realpath(filename)),filename)
		output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"output")

	except Exception as e:
		print("An error occurred : "+str(e))

	# Store all the pages of the PDF in a variable 
	pages = convert_from_path(dir_path, 350, fmt='jpeg', output_folder=output_path) 
	
	# Save first page
	filename = os.path.join(output_path,"page_1.jpg")
	
	# Save the image of the page in system 
	pages[0].save(filename, 'JPEG') 

	# load the saved first page
	image = cv2.imread(filename)

	# convert the image to black and white for better OCR
	ret,thresh1 = cv2.threshold(image,120,255,cv2.THRESH_BINARY)

	# pytesseract image to string to get results
	text = str(pytesseract.image_to_string(thresh1, config='--psm 6'))

	arr = text.split("\n")

	for each in arr:
		if ("Test" in each and "Name" in each) or ("TEST" in each and "NAME" in each):
			each_arr = each.split()
			if len(each_arr) == 7:
				mostImportantFormat(output_path,pages)
			elif len(each_arr) == 5:
				importantFormat(output_path,pages)
			elif len(each_arr) == 6:
				goodToHaveFormat(output_path,pages)
			else:
				leastImportantFormat(output_path,pages)
			break
	else:
		leastImportantFormat(output_path,pages)



while(True):
	filename = input("Please enter the filename with extension. E.g. - Document1.pdf\n")
	if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)),filename)):		
		if len(filename) > 0:
			detectFormat(filename.strip())
			break
		else:
			print("Please enter a filename")
	else:
		print("The file doesn't exist")
