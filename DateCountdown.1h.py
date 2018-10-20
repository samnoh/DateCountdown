#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3

# <bitbar.title>Date Countdown</bitbar.title>
# <bitbar.version>v1.3</bitbar.version>
# <bitbar.author>Sam NOh</bitbar.author>
# <bitbar.author.github>samnoh</bitbar.author.github>
# <bitbar.desc>Shows how many dates left or past for certain days on your menu bar</bitbar.desc>
# <bitbar.dependencies>python3</bitbar.dependencies>

import os, subprocess
from datetime import datetime

GIT_PATH = '/'.join(os.path.realpath(__file__).split('/')[:-1]) # real path, not alias
BASE_PATH  = os.path.dirname(__file__) + '/'
FILE_PATH = BASE_PATH + '.DateCountdown.txt'
MENUBAR_SHOWN = 1
MAXIMUM_STRING = 30
DATE_FORMAT = '%d/%m/%y'
DEFAULT_THEME = { # future color is default
	'present': 'green',
	'future': 'gray',
	'past': 'blue'
}
COLOR = DEFAULT_THEME


def diffTime(time_future):
	duration_in_seconds = (time_future - datetime.now()).total_seconds()
	return int(divmod(duration_in_seconds, 86400)[0] + 1)


def ReadFile():
	try:
		file = open(os.path.expanduser(FILE_PATH), 'r')
	except OSError: # if no text file exits
		return 0

	time_dict = {} 
	for line in file.read().splitlines():
		if len(line) == 0: # empty line
			continue

		time = line.split(' ')[0]
		try:
			if datetime.strptime(time, DATE_FORMAT) == False: # if input is not in the date format
				raise ValueError
		except ValueError:
			continue # skip the line
	
		title = line.replace(time, '').lstrip().rstrip() # remove whitespace on the left and right side
		time_dict[title] = diffTime(datetime.strptime(time, DATE_FORMAT))  # add it to dictionary

	file.close()
	return list(sorted(time_dict.items(), key = lambda kv: kv[1])) # sort the dictionary and convert it to a list


def PrintDates(time_list):
	for index in range(len(time_list)):
		time_diff = time_list[index][1]
		title = time_list[index][0]
		
		if time_diff == 0: # present
			print(title, 'IS TODAY! | length=', MAXIMUM_STRING, 'color=', COLOR['present'], sep=' ')
		elif time_diff > 0: # future
			print(time_diff, 'days until', title, '| length=', MAXIMUM_STRING, 'color=', COLOR['future'], sep=' ')
		else: # past
			print(abs(time_diff), 'days since', title, '| length=', MAXIMUM_STRING, 'color=', COLOR['past'], sep=' ')


def PrintOptions(): # Options
	print('---')
	print("Edit/Add Dates | bash='open -e " + FILE_PATH + " && exit'")
	print('---')
	print("Update Plugin | bash='cd " + GIT_PATH + " && git reset --hard && git pull'")
	print('Created with :heart: by Sam | color=gray href=https://github.com/samnoh/DateCountdown')
	

def PrintWelcome(): # New Users
	print('Welcome')
	print('---')
	print("Click to start | bash='touch " + FILE_PATH + " && echo 25/12/18 Christmas > " + BASE_PATH + ".DateCountdown.txt'")
	print('After click above, you need to refresh | color= ', COLOR['future'])
	exit() # end of program right here

	
def Main():	
	time_list = ReadFile()
	if time_list == 0:
		PrintWelcome()

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
		PrintDates(time_present[:MENUBAR_SHOWN]) 
		print('---')
		PrintDates(time_present[MENUBAR_SHOWN:]) 
		PrintDates(time_future)
		PrintDates(time_past)
	elif len(time_future) > 0: # no present countdown now
		PrintDates(time_future[:MENUBAR_SHOWN]) # only one for the future will be shown
		print('---')
		PrintDates(time_future[MENUBAR_SHOWN:])
		PrintDates(time_past)
	elif len(time_past) > 0:
		PrintDates(time_past[:MENUBAR_SHOWN])
		print('---')
		PrintDates(time_past[MENUBAR_SHOWN:])
	else: # Nothing in the list
		print('No Countdown :sob:')
		print('---')

	PrintOptions()


if __name__ == "__main__":
    Main()