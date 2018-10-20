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


def DiffTime(time_future):
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
	
		title = line.replace(time, '').lstrip().rstrip() + '&' + time # remove whitespace on the left and right side
		time_dict[title] = DiffTime(datetime.strptime(time, DATE_FORMAT))  # add it to dictionary

	file.close()
	return list(sorted(time_dict.items(), key = lambda kv: kv[1])) # sort the dictionary and convert it to a list


def PrintDates(time_list):
	for index in range(len(time_list)):
		time_diff = time_list[index][1]
		title = time_list[index][0]
		
		if time_diff == 0: # present
			print(title.split('&')[0], 'IS TODAY! | length=', MAXIMUM_STRING, 'color=', COLOR['present'], sep=' ')
		elif time_diff > 0: # future
			print(time_diff, 'days until', title.split('&')[0], '| length=', MAXIMUM_STRING, sep=' ')
			#print(time_diff, 'days until', title, '| length=', MAXIMUM_STRING, 'color=', COLOR['future'], sep=' ')
		else: # past
			print(abs(time_diff), 'days since', title.split('&')[0], '| length=', MAXIMUM_STRING, 'color=', COLOR['past'], sep=' ')


def PrintOptions(): # Options
	print('---')
	print("Edit/Add Dates | bash='open -e " + FILE_PATH + " && exit'")
	print('---')
	print("Update Plugin | bash='cd " + GIT_PATH + " && git reset --hard && git pull'")
	print('Created with :heart: by Sam (1.3) | href=https://github.com/samnoh/DateCountdown')


def PrintWelcome(): # New Users
	print('Welcome!')
	print('---')
	print("Click to start | bash='touch " + FILE_PATH + " && echo 25/12/18 Christmas > " + BASE_PATH + ".DateCountdown.txt'")
	print('After click above, you need to refresh')
	exit() # end of program right here


def PrintNoList():
	print('No Countdown :sob:')
	PrintOptions()
	exit()


def Main():	
	time_list = ReadFile()

	if time_list == 0:
		PrintWelcome()

	if len(time_list) == 0:
		PrintNoList()

	global MENUBAR_SHOWN
	if MENUBAR_SHOWN > len(time_list):
		MENUBAR_SHOWN = len(time_list)
	elif MENUBAR_SHOWN < 1:
		MENUBAR_SHOWN = 1

	time_past = []
	for item in time_list:
		if item[1] < 0:
			time_past.append(item)
			time_list.remove(item)

	time_past.reverse()
	time_list += time_past

	PrintDates(time_list[:MENUBAR_SHOWN])
	print('---')
	PrintDates(time_list[MENUBAR_SHOWN:])
	PrintOptions()


if __name__ == "__main__":
    Main()