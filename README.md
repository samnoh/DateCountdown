# DateCountdown
BitBar Plugin Script | Date Countdown on your menubar

## Requirements
1. BitBar app
2. Python 3

## How to install
1. Go to https://getbitbar.com and install.
2. Download this plugin in your BitBar default plugin folder
3. Refresh BitBar
4. Enjoy :smile:

## How to use

### Time Format
The time format is '%d/%m/%y', e.g. 01/12/18.
If you want to change the time format, simply change DATE_FORMAT variable in the source code.
For example, DATE_FORMAT = '%y/%m/%d' or '%m/%d/%y'.

### Color
If your Mac is not in dark mode, then simply cahnge DARK_MODE variable, that is, DARK_MODE = False

You can change colors for future, present and past countdowns as well

The default colors are the followings: 
* Future: White/Black
* Present: Green
* Past: Blue


### Add/Edit Dates
Should be written in this format, 

For example,

25/12/18 Christmas

Otherwise it skips unformatted lines.
