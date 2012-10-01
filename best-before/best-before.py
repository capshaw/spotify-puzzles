# Spotify Problem : "Best Before"
# Author: Andrew Capshaw
# Email: capshaw@rice.edu

# PROBLEM DESCRIPTION
# Given a possibly ambiguous date "A/B/C", where A,B,C are integers
# between 0 and 2999, output the earliest possible legal date between
# Jan 1, 2000 and Dec 31, 2999 (inclusive) using them as day, month
# and year (but not necessarily in that order).

import itertools
import operator

def main():

	# Get the raw input from standard-in.
	rawInput = raw_input()

	# Parse the input and find the first plausible date.
	pl = parseInput(rawInput)
	pd = findFirstPossibleDate(pl)

	# Check the validity of the date (i.e. not feb 30)
	if pd != None:
		print pd.toString()
	else:
		illegalInput(rawInput)

class aDate(object):
	''' A class that stores dates and compares itself to other dates. '''

	month = None
	year = None
	day = None

	def __init__(self, year, month, day):
		self.month = month
		self.year = year
		self.day = day

	def older(self, other):
		''' Returns the 'greater' date object. None if same day. '''

		# If one's year is greater than the other
		if self.year > other.year:
			return self
		elif self.year < other.year:
			return other

		# If one's month is greater than the other
		if self.month > other.month:
			return self
		elif self.month < other.month:
			return other

		# If one's day is greater than the other
		if self.day > other.day:
			return self
		elif self.day < other.day:
			return other

		return None

	def isValid(self):
		'''
		Returns true if the date is a valid date with regards to
		western civilization's ideas of dates. False otherwise.
		'''

		# Make sure date has enough information
		if self.month == None or self.day == None or self.year == None:
			return False

		# Ensure extreme bounds are kept
		if self.month > 12 or self.day > 31:
			return False
		if self.month < 1 or self.day < 1:
			return False

		# For months that have 30 days, ensure days !>= 31
		if self.month in [9, 4, 6, 11] and self.day > 30:
			return False

		# Make sure feburary works correctly
		if self.month == 2 and self.day > 28:
			if self.day > 29:
				return False
			if self.year % 400 == 0:
				pass
			elif self.year % 100 == 0:
				return False
			elif self.year % 4 == 0:
				pass
			else:
				return False

		return True

	def toString(self):
		''' Return a string of the date. '''

		# Zero pad the month
		if self.month < 10:
			monthAddition = "0"
		else:
			monthAddition = ""

		# Zero pad the day
		if self.day < 10:
			dayAddition = "0"
		else:
			dayAddition = ""

		return str(self.year) + "-" + monthAddition + str(self.month) + "-" + dayAddition + str(self.day)

def parseInput(rawInput):
    ''' Given the raw input A/B/C, parse the input into a useful form. '''

    # Convert to a list
    rawList = rawInput.split('/')

    # The input is not in A/B/C form
    if len(rawList) != 3:
    	illegalInput(rawInput)

    # Parse each as an int
    parsedList = []
    for number in rawList:
	    try:
	        parsedList += [int(number)]
	    except ValueError:
	    	illegalInput(rawInput)

    return parsedList

def findFirstPossibleDate(parsedList):
	''' Given a parsed list, attempt to make a date object for it. '''

	# Get all permutations of A/B/C
	dates = itertools.permutations(parsedList)
	dates = list(dates)

	# Fix the year by adding 2000, if applicable
	dates = [fixYear(x) for x in dates]

	# Sort the dates into preferable order (where earliest dates are first)
	dates.sort()

	# Remove the dates that aren't valid and transform those that are into date objects
	dates = [aDate(x[0], x[1], x[2]) for x in dates if aDate(x[0], x[1], x[2]).isValid()]

	# Remove the dates that aren't in the proper range
	dates = [x for x in dates if inProperTimeRange(x)]

	# If nothing remains, no valid answer
	if len(dates) < 1:
		return None

	# First result is most preferable
	return dates[0]

def fixYear(threeple):
	''' If the year is not preceeded by century, fix. '''

	if threeple[0] < 100:
		return (threeple[0]+2000, threeple[1], threeple[2])
	return threeple

def inProperTimeRange(date):
	''' Returns true if date is in the proper time range, false otherwise. '''

	EARLIEST_DATE = aDate(2000, 1, 1)
	LATEST_DATE = aDate(2999, 12, 31)

	if date.older(EARLIEST_DATE) == EARLIEST_DATE or date.older(LATEST_DATE) == date:
		return False

	return True

def illegalInput(rawInput):
	''' Print an illegal input error if an error occurred. '''

	print rawInput + " is illegal"
	exit()

if __name__ == "__main__":
    main()