import sys
import os
import re
import getopt

def usage(code = 0):
	print('''
    usage: csv-to-markdown.py [-hv] [-i --input input_file] [-s --samename | -o
		   --output output_file] [-d --delimeter delimeter] [-f --format format_file]
 		   [--help]
    
    -h --help : Show usage statement
    -v --verbose : Show verbose information at runtime
    -s --same_name : Use input file name with file ending "md"    

    -i --input input_file : use given file for input
    -o --output output_file : use given file for output
    -d --delimeter delimeter : use the given delimeter
    -f --format format_file : use the given file for formatting
	''')
	sys.exit(code)

def error_handler(code, line_num, err):
	sys.stderr.write("Line " + str(line_num) + ": " + err + "\n")
	sys.exit(code) 

def command_line_parse():
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

	return output_loc, same_name, input_loc, verbose

def output_name(output_loc = '-', input_loc = '-'):
	# Create destination file if same as input and output not specified
	if output_loc == '-' and input_loc != '-':
		base_name = os.path.basename(input_loc)
		output_loc = os.path.split(input_loc)[0]+os.path.splitext(base_name)[0] + '.csv'
	elif output_loc != '-':
		sys.stderr.write("Only -s or -o can be used at one time\n")
		usage(3)
	elif input_loc == '-':
		sys.stderr.write("Input file must be specified for -s\n")
		usage(5)

def read_from_file(input_loc):
	if input_loc == '-':
		r = sys.stdin
	else:
		r = open(input_loc, 'r')

	data = []
	# Get information
	for line in r:
		items = line.strip().split('|')
		for index, item in enumerate(items):
			items[index] = item.strip()
		items = remove_empty(items)
		data.append(items)

	if r is not sys.stdin:
		r.close()

	return data

def remove_empty(items):

	items.reverse()
	
	for index, item in enumerate(items):
		if item != '':
			items = items[index:]
			break
		else:
			continue

	items.reverse()

	for index, item in enumerate(items):
		if item != '':
			items = items[index:]
			break
		else:
			continue

	return items

def parse_and_format(data):
	rows = []
	formatting = {'bold': set(), 'italics': set(), 'code': set()}
	# Parse information
	row_index = 0
	max_length = 0
	for row in data:
		items = []
		no_add = False
		for col_index, item in enumerate(row):
			match = re.search('^-*-$', item)
			if match == None:
				item = item.strip()
				match = re.search('^([\*_`]).*([\*_`])$', item)
				while match != None:
					item = item.strip(match.group(1))
					style = ''
					if match.group(1) == '*':
						style = 'bold'
					elif match.group(1) == '_':
						style = 'italics'
					elif match.group(1) == '`':
						style = 'code'

					if style != '':
						formatting[style].add((row_index, col_index))
					match = re.search('^([\*_`]).*([\*_`])$', item)
				items.append(item) # append data to item array
			else:
				no_add = True

		# items = remove_empty(items)

		if not len(items):
			continue
		else:
			rows.append(items) # add row of info to rows array

		if len(items) > max_length:
			max_length = len(items)

		if not no_add:
			row_index += 1

	return rows, formatting, max_length

def print_data(output_loc, rows):
	# Put table into destination file
	if output_loc and output_loc!='-':
		w = open(output_loc, 'w')
	else:
		w = sys.stdout

	# Print out 
	for row in rows:

		for item in row:
			w.write(item + ',')
		
		w.write('\n')

	if w is not sys.stdout:
		w.close()

def make_format_file(formatting, rows, max_length):

	style_row_keywords = {'bold': {}, 'italics': {}, 'code': {}}
	style_col_keywords = {'bold': {}, 'italics': {}, 'code': {}}

	w = open('format_file.txt', 'w+')

	for key in style_row_keywords:
		for index, row in enumerate(rows):
			style_row_keywords[key][index] = {'all'}
		for i in range(0, max_length):
			style_col_keywords[key][i] = {'all'}

	for key in style_row_keywords:
		for row in range(0, len(rows)):
			for col in range(0, len(rows[row])):
				if (row, col) in formatting[key]:
					continue
				else:
					style_col_keywords[key][col] = set()
					style_row_keywords[key][row] = set()

		for row in range(0, len(rows)):
			if 'all' not in style_row_keywords[key][row]:
				if (row, 0) in formatting[key]:
					style_row_keywords[key][row].add('start')
				if (row, len(rows[row]) - 1) in formatting[key]:
					style_row_keywords[key][row].add('end')
		for col in range(0, max_length):
			if 'all' not in style_col_keywords[key][col]:
				if (0, col) in formatting[key] and 'all' not in style_row_keywords[key][0]:
					style_col_keywords[key][col].add('title')
				if (len(rows)-1, col) in formatting[key] and 'all' not in style_row_keywords[key][len(rows)-1]:
					style_col_keywords[key][col].add('bottom')
	
		for row in range(1, len(rows) - 1):
			for col in range(1, len(rows[row]) - 1):
				if 'all' not in style_row_keywords[key][row]:
					if (row, col) in formatting[key] and len(style_col_keywords[key][col]) == 0:
						style_row_keywords[key][row].add('col ' + str(col))

		for index, value in style_row_keywords[key].items():
			for item in value:
				w.write(key + ' row ' + str(index) + ' ' + item + '\n')

		for index, value in style_col_keywords[key].items():
			for item in value:
				w.write(key + ' col ' + str(index) + ' ' + item + '\n')



	
def main():
	output_loc, same_name, input_loc, verbose = command_line_parse()

	if same_name:
		output_loc = output_name(output_loc, input_loc)

	data = read_from_file(input_loc)

	rows, formatting, max_length = parse_and_format(data)

	print_data(output_loc, rows)

	make_format_file(formatting, rows, max_length)

if __name__ == '__main__':
	main()