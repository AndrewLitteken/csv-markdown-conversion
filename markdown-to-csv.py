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
		data.append(items)

	if r is not sys.stdin:
		r.close()

	return data

def parse_and_format(data):
	rows = []
	# Parse information
	for row in data:
		items = []
		
		for item in row:
			match = re.search('^-*-$', item)
			if match == None:
				item = item.strip()
				match = re.search('^([\*_`]).*([\*_`])$', item)
				while match != None:
					item = item.strip(match.group(1))
					match = re.search('^([\*_`]).*([\*_`])$', item)
				items.append(item) # append data to item array

		if not items:
			continue
		else:
			print(items)
			rows.append(items) # add row of info to rows array

	return rows

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

def main():
	output_loc, same_name, input_loc, verbose = command_line_parse()

	if same_name:
		output_loc = output_name(output_loc, input_loc)

	data = read_from_file(input_loc)

	rows = parse_and_format(data)

	print_data(output_loc, rows)

if __name__ == '__main__':
	main()