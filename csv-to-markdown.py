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

def error_message(code, line_num, err):
	sys.stderr.write("Line "+str(line_num)+": "+err+"\n")
	sys.exit(code) 

def format_item(item, col, row):
	if (col, row) in formats:
		style = formats[(col, row)]
		for style_type in style:
			if style_type == 'bold':
				item = '**'+item+'**'
				if len(item) > maximum[col]:
					maximum[col] = len(item)
			if style_type == 'italics':
				item = '__'+item+'__'
				if len(item) > maximum[col]:
					maximum[col] = len(item)
			if style_type == 'code':
				item = '`'+item+'`'
				if len(item) > maximum[col]:
					maximum[col] = len(item)
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
if same_name and output_loc == '-' and input_loc != '-':
	base_name = os.path.basename(input_loc)
	output_loc = os.path.split(input_loc)[0]+os.path.splitext(base_name)[0] + '.md'
elif output_loc != '-' and same_name:
	sys.stderr.write("Only -s or -o can be used at one time\n")
	usage(3)
elif same_name and input_loc == '-':
	sys.stderr.write("Input file must be specified for -s\n")
	sys.exit(5)

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

if formatting:
	f = open(format_file, 'r')
	
	special_locations = ()
	style = False
	format_options = ('bold', 'italics', 'code')
	format_locations = ('row', 'col')
	format_special_index = ('title', 'bottom', 'end', 'start')
	format_command = ('remove')
	formats = {}
	for num, line in enumerate(f):
		newline = line.strip().split()
		key=['','']
		value=set()
		for index, word in enumerate(newline):
			word = word.lower()
			error = ''
			if word in format_options:
				value.add(word)
			elif word in format_locations:
				digit=0
				if newline[index+1].isdigit():
					digit = int(newline[index+1])
					if word == 'row' and digit < len(data):
						key[1] = digit
					elif word == 'col' and digit < len(data[digit]):
						key[0] = digit
					else: 
						error = word+" out of range"
					if newline[index+2] == "all" and error == '':
						if word == 'row':
							key_index = 0
							length =  len(data[digit])
						else:
							key_index = 1
							len(data)
						for i in range(0,length):
							key[key_index] = i
							if (key[0],key[1]) in formats:
								for styles in value:
									formats[(key[0],key[1])].add(styles)
							else:
								formats[(key[0],key[1])] = value
									
					elif error != '-' and newline[index+2] not in format_locations and newline[index+2] not in format_special_index and newline[index+2] not in format_command and newline[index+2] not in format_options:
						error = newline[index+2]+" is an unsupported keyword"
			elif word in format_special_index:
				if word == 'title':
					key[1] = 0
				elif word == 'bottom':
					key[1] = len(data)-1
				elif word == 'start':
					key[0] = 0
				elif word == 'end':
					key[0] = len(data[key[1]])-1
			elif word.isdigit() or word == 'all':
				continue
			else:
				error = "Command was not found"

			if error != '':
				error_message(4, num+1, error)
			
			if key[0] != '' and key[1] != '':
				continue
		
		if (key[0],key[1]) in formats:
			for styles in value:
				formats[(key[0],key[1])].add(styles)
		else:
			formats[(key[0],key[1])] = value
	
	f.close()

# Parse information
for row_index, row in enumerate(data):
	items = []
	
	for col_index, item in enumerate(row):
		if len(maximum) >= col_index+1: # if length of max array large enough
			if maximum[col_index] < len(item): # check and replace max if needed
				maximum[col_index] = len(item)
		else:
			maximum.append(len(item)) # add new entry if not large enough
	
		if formatting:
			item = format_item(item, col_index, row_index)	
		
		items.append(item) # append data to item array

	rows.append(items) # add row of info to rows array
	
# Put table into destination file
if output_loc and output_loc!='-':
	w = open(output_loc, 'w')
else:
	w = sys.stdout

# Print out 
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
