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

def relative_placements(scores, head_judge, include_head_judge=True):
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
    ## TODO: include/exclude head judge scores
    def count_placements(routine, placement):
        ''' Counts the number of times the routine recieved up to the given placement
            
        This simply iterates through the scores[routine] dictionary counting the 
        number of times a judge gave that routine a placement that is less that or 
        equal to the given placement.
        
        Parameters
        ----------
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
            if judges_placements[judge] <= placement:
                tally += 1
        return tally
                
    def sum_placements(routine, placement):
        ''' Sums the number of times the routine recieved up to the given placement
        
        This simply iterates through the scores[routine] dictionary counting the
        number of times a judge gave that routine a placement that is less that or
        equal to the given placement.
        
        Parameters
        ----------
        routine: hashable
            the routine we are testing
        
        placement: int
            the placement we are testing
        
        Returns
        -------
        int
            the sum of the placements less than or equal to the placement parameter
        
        '''
        sum = 0
        judges_placements = scores[routine]
        for judge in judges_placements:
            if judges_placements[judge] <= placement:
                sum += judges_placements[judge]
        return sum

    ## TODO: include/exclude head judge scores
    num_judges = len(scores.itervalues().next())
    majority   = (num_judges+1) / 2
    placements = {} # A dictionary to hold the placements
    reasons    = {} # A dictionary to hold the reasons for each placement
    
    ## Step 0: Initialization faze :P
    ## Fill in the placements table and the reasons table
    for place in range(1,len(scores)+1): placements[place] =[]
    for routine in scores:
        reasons[routine] = {}
        for placement in range(1,len(placements)+1):
            reasons[routine][placement] = 0

    ## Step 1: Tally/Sum Scores
    for routine in scores:
        for placement in range(1,len(placements)+1):
            ## If there is a placement in the scores dictionary for this routine
            ## that is less than of equal to the current placements, then we
            ## increment the total number of placement tallies.
            reasons[routine][placement] = {
                'tally': count_placements(routine, placement),
                'sum'  : sum_placements(routine, placement)
            }

    ## Step 2: Determine Preliminary Placements based on tallies and look for ties
    current_placement = 1  ## The current placement we are deciding
    decided_routines  = [] ## A list of routines that have already been decided
    for i in range(1, len(placements)+1):
        placements_decided = 0
        ## Grab all of the tallies from the reasons dictionary
        tallies = {routine: reasons[routine][i]['tally'] for routine in scores}
        for routine in tallies:
            if routine not in decided_routines and tallies[routine] >= majority:
                print 'Deciding routine:', routine,'with tally:', tallies[routine]
                placements[current_placement].append(routine)
                decided_routines.append(routine)
                placements_decided += 1
        current_placement += placements_decided

    ## Step 3/4: Do preliminary tie breakers, if needed. We do this by iterating over
    ## the placements dict and seeing if there are any scores that are the same.
    def ties():
        ''' A way to compute ties
            
        Return
        ------
        boolean:
            True if there are ties, False otherwise
        
        '''
        for place in placements:
            if len(placements[place]) > 1:
                return True
        return False

    ## Preliminary tie placements
#    if ties():
#        for place in placements:
#            if len(placements[place]) > 1:
#                ## We have found the ties. Now we need to find out who gets it
#                current_placement = place
#                decided_routines  = []
#                for routine in placements[place]:
#                    score =

    return reasons, placements

## TODO: this...
def pprint_placements(placements):
    ''' Pretty prints the placements
    
    Given the placements it prints them out in the manner shown in the above 
    Docstring. Each routine has a dictionary associated with it that gives you 
    information on the judge's scores, the reasoning behind the placement, and the 
    placement given to the routine.
    
    Parameters
    ----------
    placements: dictionary
        the dictionary of {rountine:{scores, reason, place}}
    
    '''
    pass

def parse_input_file(file):
    ''' Parses an input file and returns the score dictionary
    
    This method takes in a PROPERLY FORMATTED file and returns a properly formatted
    dictionary to be fed into the  `relative_placements` method. 
    
    Parameters
    ----------
    file : file
        the PROPERLY FORMATTED input file
    
    Returns
    -------
    dictionary
        the properly formatted dictionary of {routine:scores} pairs
    
    See Also
    --------
    relative_placements: the function into which you should feed this function's 
        output
    
    Examples
    --------
    Here is an interpter look at how to use this function
    
    >>> with open('myfile.txt', 'r') as thefile:
    ...     scores     = parse_input_file(thefile)
    ...     placements = relative_placements(scores)
    ...     print placements
    
    Here there should be output. Pretend there is
    
    '''
    scores = {} # a dictionary to hold the final scores
    ## First we need to gather all of the lines so we can parse them one-by-one
    lines = [line.strip().replace('\n','') for line in file.readlines()]
    first, rest = lines[0], lines[1:]
    ## Now we seperate out the judges to index them later
    judges = first.split()
    for line in rest:
        line = line.split()
        routine = line[0]
        _scores = {judges[i]: int(line[i+1]) for i in range(len(judges))}
        scores[routine] = _scores
    return scores

def parse_score_file(file):
    ''' Parses a scoring file and returns the score dictionary
    
    This method takes in a PROPERLY FORMATTED file and returns a properly formatted
    dictionary to be fed into the  `relative_placements` method.
    
    NOTE
    ----
    This does basically the same as `parse_input_file` but is more specific
    
    Parameters
    ----------
    file : file
        the PROPERLY FORMATTED input file
    
    Returns
    -------
    tuple : hashable, dictionary
        a tuple of the routine, scores
    
    
    See Also
    --------
    relative_placements: the function into which you should feed this function's
        output
    
    Examples
    --------
    Here is an interpter look at how to use this function
    
    >>> scores = {} ## A dictionary
    >>> for file in files:
    ...     routine, _scores = parse_score_file(file)
    ...     scores[routine] = _scores
    >>> placements = relative_placements(scores)
    >>> print placements
    
    Here there should be output. Pretend there is
    
    '''
    ## First we need to gather all of the lines so we can parse them one-by-one
    lines = [line.strip().replace('\n','') for line in file.readlines()]
    routine, judges = lines[0].split()[0], lines[0].split()[1:]
    _scores = lines[1].split()
    scores = {judges[i]: int(_scores[i]) for i in range(len(judges))}
    return routine, scores

def main():
    ''' Main program. Make sure to use python 2.7 or higher!!
    '''
    import pprint, argparse
    pp = pprint.PrettyPrinter(indent=4)
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--file',   nargs='?', type=argparse.FileType('r'),
                        help='use the given file as input')
    parser.add_argument('--files',  nargs='*', type=argparse.FileType('r'),
                        help='use multiple files as input')
    parser.add_argument('--scores', nargs='*', type=argparse.FileType('r'),
                        help='use multiple score files as input')
    parser.add_argument('--output', nargs='?', type=argparse.FileType('r'),
                        help='the output file for the program')
    parser.add_argument('--pprint', action='store_true',
                        help='pretty prints the output to stdout')
    args = parser.parse_args()
    scores = parse_input_file(args.file)
    reasons, placments = relative_placements(scores, 5)
    print 'Scores'
    pp.pprint(scores)
    print 'Placments'
    pp.pprint(placments)
    print 'Reasons'
    pp.pprint(reasons)

if __name__ == '__main__':
    main()
