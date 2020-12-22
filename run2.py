# Import libraries 
from pdf2image import convert_from_path 
from PIL import Image 
from progress.bar import Bar



import pytesseract 
import sys 
import os 
import cv2
import shutil

def hasDecimalValueOrStar(arr):
    for val in arr:
    	if "*" in val:
    		return True
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



def endsWithANumber(row):
	return isInteger(row[-1][-1])

def endsWithUnits(row):
	return "/" in row[-1]

def endsWithPosNegNil(row):
	return "POSITIVE" in row[-1] or "NEGATIVE" in row[-1] or "NIL" in row[-1]

def endsWithADash(row):
	return "-" in row[-1]

def hasGender(row):
	for each in row:
		s = each.strip()
		if 'Male' in s or 'MALE' in s or 'Female' in s or 'FEMALE' in s:
			return True
	return False



def isValidRow(row):
	if len(row) == 0 or len(row)>15:
		return False
	if len(row) < 3:
		return endsWithANumber(row)
	if ':' in row:
		return False
	if hasDecimalValueOrStar(row):
			return endsWithUnits(row) or endsWithANumber(row) or endsWithADash(row)
	return endsWithPosNegNil(row)

#Current Directory path
cur_dir_path = os.path.dirname(os.path.realpath("GoodToHave.pdf"))


# Path of the pdf 
dir_path = os.path.join(os.path.dirname(os.path.realpath("GoodToHave.pdf")),"GoodToHave.pdf")


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
outfile = "out_text2.txt"

f = open(outfile, "a") 

#Progress Bar 
bar = Bar('Processing', max=filelimit)

start_flag = False
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
	
    
	
	for each in arr:
		if ("Name" in each and "Test" not in each) or "Age/Sex" in each:
			if i == 1:
				f.write(each+"\n")
			continue
		if "Name" in each and "Result" in each:
			start_flag = True
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
