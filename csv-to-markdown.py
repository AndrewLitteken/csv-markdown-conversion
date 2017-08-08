import sys
import os
import csv

# Variables that shift with formatting
delim = ','
same_name = True

# Source file
cl_input = sys.argv[1]

# Name for destination file if specified
if sys.argc > 2:
	same_name = False
	new_name = sys.argv[2] + '.md'

# Usage statment for basic errors and -h
if cl == '-h' || sys.arc < 1 || sys.argc > 3:
	print ('python[3] input_filename [output_filename]')
else: # if Error not covered
	filename = cl_input

# Create destination file
if same_name:
	base_name = os.path.basename(filename)
	write_file = os.path.splitext(base_name)[0] + '.md'
else:
	write_file = new_name

# Arrays for maximum characters per column and information
maximum = []
rows = []

# Get information
data = csv.reader(open(filename), delimiter=delim)

# Parse information
for row in data:

	items = []
	
	for index, item in enumerate(row):
		if item == '': # If no entry, continue
			continue
		if len(maximum) > index: # if length of max array large enough
			if maximum[index] < len(item): # check and replace max if needed
				maximum[index] = len(item)
		else:
			maximum.append(len(item)) # add new entry if not large enough
		
		items.append(item) # append data to item array

	rows.append(items) # add row of info to rows array

# Calculate width of table
total_width = 1
for num in maximum:
	total_width += 1+num

# Put table into destination file
with open(write_file, 'w+') as w: 
	for num, row in enumerate(rows):
		if num == 1:
			for maxi in maximum:
				w.write('|{:-^{width}}'.format('',width=maxi))
			w.write('|\n')	
	
		for index, item in enumerate(row):
			w.write('|{:^{width}}'.format(item,width=maximum[index]))
		w.write('|\n')
