#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3

# <bitbar.title>Date Countdown</bitbar.title>
# <bitbar.version>v1.1.1</bitbar.version>
# <bitbar.author>Sam NOh</bitbar.author>
# <bitbar.author.github>samnoh</bitbar.author.github>
# <bitbar.desc>Shows how many dates left or past for certain days</bitbar.desc>
# <bitbar.image></bitbar.image>
# <bitbar.dependencies>python3</bitbar.dependencies>

from datetime import datetime
import os
import operator


BASE_PATH  = '~/BitBar/'
FILE_PATH = BASE_PATH + '.DateCountdown.txt'
MENUBAR_SHOWN = 1
MAXIMUM_STRING = 30
DATE_FORMAT = '%d/%m/%y'
DARK_MODE = True
COLOR = {
	'future': 'white',
	'present': 'green',
	'past': 'blue',
}


def diffTime(time_future):
	duration_in_seconds = (time_future - datetime.now()).total_seconds()
	return int(divmod(duration_in_seconds, 86400)[0] + 1)


def ReadFile():
	try:
		file = open(os.path.expanduser(FILE_PATH), 'r')
	except OSError: # if no text file exits
		print('Welcome')
		print('---')
		print("Click to start | refresh=true bash='touch " + BASE_PATH + ".DateCountdown.txt && echo 25/12/18 Christmas > " + BASE_PATH + ".DateCountdown.txt'")
		print('After click, you need to refresh')
		exit() # end of program right here

	time_dict = {} 
	text = file.read().splitlines()

	for line in text:
		if len(line) == 0: # empty line
			continue

		line_arr = line.split(' ')
		time = line_arr[0]
		
		try:
			if datetime.strptime(time, DATE_FORMAT) == False: # if input is not in the date format
				raise ValueError
		except ValueError:
			continue # skip the line
	
		title = line.replace(time, '').lstrip().rstrip() # remove whitespace on the left and right side
		time_dict[title] = diffTime(datetime.strptime(time, DATE_FORMAT))  # add it to dictionary

	file.close()
	return list(sorted(time_dict.items(), key = lambda kv: kv[1])) # sort the dictionary and convert it to a list


def PrintOutput(time_list):
	for index in range(len(time_list)):
		time_diff = time_list[index][1]
		title = time_list[index][0]
		
		if time_diff == 0: # present
			print(title, 'IS TODAY! | length=', MAXIMUM_STRING, ' color=', COLOR['present'], sep=' ')
		elif time_diff > 0: # future
			print(time_diff, 'days until', title, '| length=', MAXIMUM_STRING, ' color=', COLOR['future'], sep=' ')
		else: # past
			print(abs(time_diff), 'days since', title, '| length=', MAXIMUM_STRING, ' color=', COLOR['past'], sep=' ')
				

def main():
	if not DARK_MODE:
		COLOR['future'] = 'black'

	time_list = ReadFile()
	time_past = []
	time_present = []
	time_future = []

	for item in time_list:
		time_diff = item[1]
		if time_diff == 0:
			time_present.append(item)
		elif time_diff > 0:
			time_future.append(item)
		else: 
			time_past.append(item)

	if len(time_present) > 0: # if there is present countdown
		PrintOutput(time_present[:MENUBAR_SHOWN]) 
		print('---')
		PrintOutput(time_present[MENUBAR_SHOWN:]) 
		PrintOutput(time_future)
		PrintOutput(time_past)
	elif len(time_future) > 0: # no present countdown now
		PrintOutput(time_future[:MENUBAR_SHOWN]) # only one for the future will be shown
		print('---')
		PrintOutput(time_future[MENUBAR_SHOWN:])
		PrintOutput(time_past)
	elif len(time_past) > 0:
		PrintOutput(time_past[:MENUBAR_SHOWN])
		print('---')
		PrintOutput(time_past[MENUBAR_SHOWN:])
	else: # Nothing in the list
		print('No Countdown :sob:', sep='')
		print('---')

	# Options
	print('---')
	print("Edit/Add Dates | bash='open -e ", BASE_PATH, ".DateCountdown.txt && exit'" , sep='')
	print('---')
	print('Created with :heart: by Sam | color=gray href=https://www.instagram.com/sam48855/')


if __name__ == "__main__":
    main()