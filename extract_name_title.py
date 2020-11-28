import json
import argparse

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('json_file')
	parser.add_argument('output')
	args = parser.parse_args()

	output = open(args.output, 'w')
	output.write("Name\ttitle\tcoding\n")

	with open(args.json_file) as f:
		for line in f:
			jline = json.loads(line)
			#print(jline['title'])
			output.write(jline['name'] + '\t' + jline['title'] + '\n')


if __name__ == '__main__':
	main()
