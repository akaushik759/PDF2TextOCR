# Import libraries 
from pdf2image import convert_from_path 
from PIL import Image 
from progress.bar import Bar



import pytesseract 
import sys 
import os 
import cv2
import shutil

def hasDecimalValue(arr):
    for val in arr:
        try:
            float(val)
        except Exception as e:
            continue
        else:
            return True
    return False

def isInteger(char):
	try:
		int(char)
	except ValueError:
		return False
	else:
		return True

def startsWithANumber(row):
	return isInteger(row[0][0])

def endsWithANumber(row):
	return isInteger(row[-1][-1])


def isValidRow(row):
	if len(row) < 4:
		return False
	if ':' in row:
		return False
	if hasDecimalValue(row):
		if not startsWithANumber(row):
			return endsWithANumber(row)
	return False

#Current Directory path
cur_dir_path = os.path.dirname(os.path.realpath("MOST_IMPORTANT_FORMAT.pdf"))

# Path of the pdf 
dir_path = os.path.join(os.path.dirname(os.path.realpath("MOST_IMPORTANT_FORMAT.pdf")),"MOST_IMPORTANT_FORMAT.pdf")

output_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"output")


# Store all the pages of the PDF in a variable 
pages = convert_from_path(dir_path, 350, fmt='jpeg', output_folder=output_path) 

# Counter to store images of each page of PDF to image 
image_counter = 1

# Iterate through all the pages stored above 
for page in pages: 

	# Declaring filename for each page of PDF as JPG 
	filename = os.path.join(output_path,"page_"+str(image_counter)+".jpg")
	
	# Save the image of the page in system 
	page.save(filename, 'JPEG') 

	# Increment the counter to update filename 
	image_counter = image_counter + 1

# Variable to get count of total number of pages 
filelimit = image_counter-1

# Creating a text file to write the output 
outfile = "out_text0.txt"

f = open(outfile, "a") 

#Progress Bar 
bar = Bar('Processing', max=filelimit)

# Iterate from 1 to total number of pages 
for i in range(1, filelimit + 1): 

	filepath = os.path.join(output_path,"page_"+str(i)+".jpg")


	# load the original image
	image = cv2.imread(filepath)

	#quit()

	# convert the image to black and white for better OCR
	ret,thresh1 = cv2.threshold(image,120,255,cv2.THRESH_BINARY)

	# pytesseract image to string to get results
	text = str(pytesseract.image_to_string(thresh1, config='--psm 6'))
	arr = text.split("\n")
	
    
	start_flag = False
	for each in arr:
		if "Gender/Age" in each and i == 1:
			f.write(each+"\n")
			continue
		if "Name" in each and "Value" not in each:
			start_flag = True
			if i == 1:
				f.write(each+"\n")
			continue
		if start_flag:
			row_arr = each.split()
			if isValidRow(row_arr):
				f.write(each+"\n")
	bar.next()

#Delete all created images
shutil.rmtree(output_path) 
os.mkdir(output_path)

bar.finish()

# Close the file after writing all the text. 
f.close() 
