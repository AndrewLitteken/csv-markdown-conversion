import sys
import os
import getopt

def usage(code=0):
	print('''
    usage: csv-to-markdown.py [-hv] [-i --input input_file] [-s --samename | -o --output output_file] [-d --delimeter delimeter] [-f --format format_file] [--help]
    
    -h --help : Show usage statement
    -v --verbose : Show verbose information at runtime
    -s --same_name : Use input file name with file ending "md"    

    -i --input input_file : use given file for input
    -o --output output_file : use given file for output
    -d --delimeter delimeter : use the given delimeter
    -f --format format_file : use the given file for formatting
	''')
	sys.exit(code)

def format_item(item):
	return item

# Variables that shift with formatting
delim = ','
output_loc = '-'
same_name = False
input_loc = '-'
formatting = False
format_file = "-"
verbose = False

# Command line options
try:
	opts, args = getopt.getopt(sys.argv[1:], 'hsvd:i:o:f:', ["help", "verbose", "same_name", "delimeter=", "format=", "input=", "output="])
except getopt.GetoptError as err:
	print(err)
	usage(2)

#Parse Command Line
for o, a in opts:
	if o in ("-s", "--same_name"):
		same_name = True
	elif o in ("-f", "--format"):
		formatting = True
		format_file = a
	elif o in ("-i", "--input"):
		input_loc = a
	elif o in ("-o", "--output"):
		output_loc = a
	elif o in ("-v", "--verbose"):
		verbose = True
	elif o in ("-d", "--delimeter"):
		delim = a
	elif o in ("-h", "--help"):
		usage(0)
	else:
		assert False, "unhandled option"

# Create destination file if same as input and output not specified
if same_name and input_loc == '-':
	base_name = os.path.basename(input_loc)
	output_loc = os.path.split(input_loc)[0]+os.path.splitext(base_name)[0] + '.md'
else:
	sys.stderr.write("Only -s or -o can be used at one time\n")
	usage(3)
	
# Arrays for maximum characters per column and information
if input_loc == '-':
	r = sys.stdin
else:
	r = open(input_loc, 'r')

maximum = []
max_length = 0
rows = []
data = []

# Get information
for line in r:
	items = line.rstrip("\n, ").split(delim)
	data.append(items)
	if max_length < len(items):
		max_length = len(items)

if r is not sys.stdin:
	r.close()

# Parse information
for row in data:
	items = []
	
	for index, item in enumerate(row):
		if len(maximum) >= index+1: # if length of max array large enough
			if maximum[index] < len(item): # check and replace max if needed
				maximum[index] = len(item)
		else:
			maximum.append(len(item)) # add new entry if not large enough
	
		if formatting:
			item = format_item(item)	
		
		items.append(item) # append data to item array

	rows.append(items) # add row of info to rows array

# Put table into destination file
if output_loc and output_loc!='-':
	w = open(output_loc, 'w')
else:
	w = sys.stdout

for num, row in enumerate(rows):
	if num == 1:
		for maxi in maximum:
			w.write('|{:-^{width}}'.format('',width=maxi))
		w.write('|\n')	

	for index, item in enumerate(row):
		w.write('|{:^{width}}'.format(item,width=maximum[index]))
	
	if index+1 < max_length:
		for num in range(index+1,max_length):
			w.write('|{:^{width}}'.format('',width=maximum[num]))
	
	w.write('|\n')

if w is not sys.stdout:
	w.close()
