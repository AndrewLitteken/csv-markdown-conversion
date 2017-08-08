import sys
import os
import csv

delim = ','
same_name = True

cl_input = sys.argv[1]

if sys.arc > 2:
	same_name = False
	new_name

if cl == '-h':
	print ('python[3] input_filename [output_filename]')
else:
	filename = cl_input

maximum = []
rows = []

data = csv.reader(open(filename), delimiter=delim)

for row in data:

	items = []
	
	for index, item in enumerate(row):
		if item == '':
			continue
		if len(maximum) > index:
			if maximum[index] < len(item):
				maximum[index] = len(item)
		else:
			maximum.append(len(item))
		
		items.append(item)

	rows.append(items)

total_width = 1
for num in maximum:
	total_width += 1+num

if same_name:
	base_name = os.path.basename(filename)
	write_file = os.path.splitext(base_name)[0] + '.md'
else:
	write_file = new_name

with open(write_file, 'w+') as w: 
	for num, row in enumerate(rows):
		if num == 1:
			for maxi in maximum:
				w.write('|{:-^{width}}'.format('',width=maxi))
			w.write('|\n')	
	
		for index, item in enumerate(row):
			w.write('|{:^{width}}'.format(item,width=maximum[index]))
		w.write('|\n')
