''' auxilary file for io operations
'''

__author__  = 'Brooks MacBeth'
__version__ = '1.0.0'

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
    scoring.competition: the function into which you should feed this function's
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

def print_full_placements(placements):
    '''
    '''
    pass