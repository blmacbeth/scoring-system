#!/usr/bin/python2.7
''' This module is used in the Score Keeper applicationas a location for all the
functions to perform the score calculations. The main function inthis module is the
`relative_placement` method, which performs the placement for the competition. Here
is some sample input and some sample output:

>>> python scoring.py --file myfile.txt --pprint
              ||    Judge Placement     ||        Relative Placement         ||
--------------++------------------------++-----------------------------------++------
Couple Number || J1 | J2 | J3 | J4 | J5*|| 1-1 | 1-2 | 1-3 | 1-4 | 1-5 | 1-6 || Place
--------------++----+----+----+----+----++-----+-----+-----+-----+-----+-----++------
     1        ||   1|   1|   3|   2|   3||    2|    3|-----|-----|-----|---->||     1
--------------++----+----+----+----+----++-----+-----+-----+-----+-----+-----++------
     2        ||   6|   5|   4|   1|   2||    1|    2|    2| 3(7)|    4|---->||     4
--------------++----+----+----+----+----++-----+-----+-----+-----+-----+-----++------
     3        ||   2|   4|   1|   5|   5||    1|    2|    2| 3(7)|    5|---->||     3
--------------++----+----+----+----+----++-----+-----+-----+-----+-----+-----++------
     4        ||   4|   2|   5|   6|   6||    0|    1|    1|    2|-----|---->||     6
--------------++----+----+----+----+----++-----+-----+-----+-----+-----+-----++------
     5        ||   5|   6|   2|   3|   4||    0|    1|    2| 3(9)|-----|---->||     5
--------------++----+----+----+----+----++-----+-----+-----+-----+-----+-----++------
     6        ||   3|   3|   6|   4|   1||    1|    1|    3|-----|-----|---->||     2


`--file myfile.txt` says that you are feeding it a file with the following format

               <judge0> <judge1> ... <judgeN>
    <routine0> <score0> <score1> ... <scoreN>
    <routine1> <score0> <score1> ... <scoreN>
    .                            .
    .                             .
    .                              .
    <routineN> <score0> <score1> ... <scoreN>

Another option is to have `--files myfile1.txt myfile2.txt ...`. This will allow you
to input more that file in the same format as above.

A final way to input scores is by multiple files containing a single routine and its
scores `--scores myfile.txt0 myfile.txt1 ...`. The files should look like this

              <judge0> <judge1> ... <judgeN>
    <routine> <score0> <score1> ... <scoreN>

The above example had the option `--pprint` which will produce output that is good
enough to print out on its own (in a monospace font). The other option will just
print out to Python's stdout stream. This can be redirected to a file in one of two
ways: a) by using the argument `--output myoutput.txt` or b) by using good old
fashioned piping `python ... > myoutput.txt`.

As a final note, please look at the 'Unraveline the Mysteries of the Relative
Placement Scoring System' pdf (hopefully in the same directory as this file) to clear
up any confusion on how the `relative_placement` method works or why I chose certain
names, etc.
'''

__author__  = 'Brooks MacBeth'
__version__ = '1.0.0'


def sum_placements(scores, routine, placement, head_judge=None):
	''' Sums the number of times the routine recieved up to the given placement

	This simply iterates through the scores[routine] dictionary counting the
	number of times a judge gave that routine a placement that is less that or
	equal to the given placement.

	Parameters
	----------
	scores: dict
	the scores over which we are counting

	routine: hashable
	the routine we are testing

	placement: int
	the placement we are testing

	head_judge: hashable, optional
	the head judge

	Returns
	-------
	int
	the sum of the placements less than or equal to the placement parameter

	'''
	sum = 0
	judges_placements = scores[routine]
	for judge in judges_placements:
		if judges_placements[judge] <= placement and not judge is head_judge:
			sum += judges_placements[judge]
	return sum

def count_placements(scores, routine, placement, head_judge=None):
	''' Counts the number of times the routine recieved up to the given placement

	This simply iterates through the scores[routine] dictionary counting the
	number of times a judge gave that routine a placement that is less that or
	equal to the given placement.

	Parameters
	----------
	scores: dict
	the scores over which we are counting

	routine: hashable
	the routine we are testing

	placement: int
	the placement we are testing

	Returns
	-------
	int
	the number of times any judge gave them a placement less than or equal
	to the placement parameter

	'''
	tally = 0
	judges_placements = scores[routine]
	for judge in judges_placements:
		if judges_placements[judge] <= placement and not judge is head_judge:
			tally += 1
	return tally


## TODO: size
def prelims(scores, head_judge, size):
	''' Returns the results of a preliminary scoring.

	Parameters
	----------
	scores: dict
	a dictionary of {routine: placements} where placements is
	another dictionary of {judge: placement" pairs

	head_judge: hashable
	the head judge in the competition

	size: int
	the number of competitors are advancing

	Returns
	-------

	dict
	a list of top placements
	'''
	num_judges = len(scores.itervalues().next())
	placements = []

	for r in scores:
		tuple = (r, scores[r], sum_placements(scores, r, 3, head_judge))
		placements.append(tuple)
	return sorted(placements, key=operator.itemgetter(2))

def competition(scores, head_judge, included=True):
	''' places routines using the relative placement method

	The basic idea behind this method is to place routines based on the relative
	placements scoring method. The way I will do this is by a step-wise process.

	Step 1: Tally scores
	We tally the total number of score up to a placement

	Step 2: Determine preliminary placements
	We count placements only to a majority and then determine the places based
	on which routines reached a majority first

	Step 3: (Conditional) Do a preliminary tie breaker
	If there are any ties in the preliminary placements then we perform a tie
	breaker based on the sum of the placements that got them to the placement

	Step 4: (Conditional) Do the final tie breaking
	If there are any remaining ties to break, then we use the head judge's scores
	to break the final ties

	Parameters
	----------
	scores: dictionary
	Scores is a dictionary of routine names or numbers or ids or objects,
	however you care to implement routines, so long as they are hashable. In
	this implementation it is favorable to have them as either strings or ints
	as those are more compact.

	head_judge: judge Object
	This is a judge object and must be hashable. It is our index into the scores
	dictionary in order to break ties later on. It is also used later in the
	pprint method

	include_head_judge: boolean, optional
	This tells the program whether we need to include the head judge in the tally
	process. This is not required, as most of the time we do include the head
	judge's scores in the tallying process

	Returns
	-------
	dictionary
	this is a dictionary containing all of the information necessary to do just
	about anything you would need to do with placements. Here are the fields
	available right now

	placements: a dictionary of {routine: placement} pairs
	reason: contains a dictionary allowing for one to see why a placement was set
	head_judge: the head judge in the score
	more to come... maybe

	'''
	num_judges   = len(scores.itervalues().next())
	num_routines = len(scores)
	majority     = (num_judges+1) / 2
	placements   = {} # A dictionary to hold the placements
	reasons      = {} # A dictionary to hold the reasons for each placement
	ties         = {} # A dictionary to hold the ties we need to process

	## Step 1: tally/sum scores
	for place in range(1,num_routines+1): placements[place] = None
	for routine in scores:
		reasons[routine] = {}
		for place in range(1,num_routines+1):
			if included:
				reasons[routine][place] = {
				'tally': count_placements(scores, routine, place),
				'sum'  : sum_placements(  scores, routine, place)
				}
			else:
				reasons[routine][place] = {
				'tally': count_placements(scores, routine, place, head_judge),
				'sum'  : sum_placements(  scores, routine, place, head_judge)
				}

	## Step 2: initial placments
	decided_placements = {}
	decided_routines   = []
	current_placement  = 1
	for place in range(1,num_routines+1):
		decided_placements[place] = {'count':0, 'routines':[]}
		for routine in scores:
			tally = reasons[routine][place]['tally']
			if tally >= majority and routine not in decided_routines:
				decided_placements[place]['count'] += 1
				decided_placements[place]['routines'].append(routine)
				decided_routines.append(routine)
		if decided_placements[place]['count'] is 1:
			placements[current_placement] = decided_placements[place]['routines'][0]
		elif decided_placements[place]['count'] > 1:
			ties[current_placement] = place
		current_placement += decided_placements[place]['count']

	## Step 3-4: proccess ties
	def place_ties(routines, place, count, i):
		if len(routines) is 0: return
		if len(routines) is 1:
			placements[place] = routines[0]
			return
		## TODO: fix this
		if count >= num_routines:
			headjudgescores = {}
			for r in routines:
				headjudgescore = scores[r][head_judge]
				headjudgescores[headjudgescore] = r
			print 'head judge', headjudgescores
			for _,routine in headjudgescores.items():
				placements[place] = routine
				place += 1
			return
		the_dict     = {r:reasons[r][count][i] for r in routines}
		new_routines = [min(the_dict, key=the_dict.get)] if i is 'sum' else [max(the_dict, key=the_dict.get)]
		for r, v in the_dict.items():
			if v is the_dict[new_routines[0]] and not r is new_routines[0]:
				new_routines.append(r)
		if len(new_routines) is 1:
			placements[place] = new_routines[0]
			routines.remove(new_routines[0])
			place_ties(routines, place+1, count, 'sum')
			return
		else:
			place_ties(new_routines[:], place, count+1, 'tally')
			for r in new_routines: routines.remove(r)
			place_ties(routines, place+len(new_routines), count, 'sum')
			return
		return

	for current_placement, place in ties.items():
		routines = decided_placements[place]['routines']
		place_ties(routines[:], current_placement, place, 'sum')

	return placements, reasons

## Alias functions to make things look nicer later on
quarter_finals = prelims
simi_finals    = prelims
finals         = competition

if __name__ == '__main__':
	import pprint, argparse
	import input_output
	
	pp = pprint.PrettyPrinter(indent=4)

	parser = argparse.ArgumentParser()
	parser.add_argument('--file',   nargs='?', type=argparse.FileType('r'),
	                    help='use the given file as input')
	parser.add_argument('--files',  nargs='*', type=argparse.FileType('r'),
	                    help='use multiple files as input')
	parser.add_argument('--scores', nargs='*', type=argparse.FileType('r'),
	                    help='use multiple score files as input')
	parser.add_argument('--output', nargs='?', type=argparse.FileType('r'),
	                    help='output file for the program')
	parser.add_argument('--pprint', action='store_true',
	                    help='pretty prints the output to stdout')
	args = parser.parse_args()
	scores = input_output.parse_input_file(args.file)
	placments, reasons = competition(scores, 5)
	print 'Scores'
	pp.pprint(scores)
	print 'Placments'
	pp.pprint(placments)
	print 'Reasons'
	pp.pprint(reasons)
