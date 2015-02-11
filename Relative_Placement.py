'''
              ||    Judge Placement     ||        Relative Placement         ||
--------------++------------------------++-----------------------------------++------
Couple Number || J1 | J2 | J3 | J4 | J5 || 1-1 | 1-2 | 1-3 | 1-4 | 1-5 | 1-6 || Place
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
'''

class Relative_Placements:
	def __init__(self, places, headjudge, majority, include=False):
		self.relative_placements = dict()
		self.majority_placements = dict()
		self.final_placements    = dict()
		
		self.headjudge = headjudge
		self.majority  = majority
		self.places    = places.copy() # for the ties
		self.include   = include # do we include the head judge?
		
		self.__fill_columns(self.places.copy(), 1)
		self.__cathunk(self.relative_placements.copy(), 1, 1)
	
	# fill in the relative placements
	def __fill_columns(self, places, place): 
		if len(places) == 0: return
		for routine, scores in places.items():
			num_places = self.__count(place, scores)
			if routine not in self.relative_placements:
				self.relative_placements[routine] = {place:num_places}
			else:
				self.relative_placements[routine][place] = num_places
			if num_places >= self.majority: del places[routine]
		self.__fill_columns(places, place+1)
	
	def __cathunk(self, relative_places, place, placement):
		if len(relative_places) == 0: return
		majorities = dict()
		for routine, placecounts in relative_places.items():
			if placecounts[place] >= self.majority: 
				majorities[routine] = placecounts
				del relative_places[routine]
		x = len(majorities)
		if   len(majorities) == 0: self.__cathunk(relative_places, place+1, placement)
		elif len(majorities) == 1: 
			self.final_placements[majorities.keys()[0]] = placement
			self.__cathunk(relative_places, place+1, placement+1)
		else:
			self.__ties(majorities, place, placement)
		self.__cathunk(relative_places, place+1, placement+x)
	
	# We need to deal with ties!!
	def __ties(self, ties, place, placement):
		if place > len(self.places):
			self.__chiefjudgetie(ties, placement)
			return
		if len(ties) == 0: return
		if len(ties) == 1:
			routine,_ = ties.popitem()
			self.final_placements[routine] = placement
			return
		tie = dict()
		winner    = None
		winnersum = None
		for routine,_ in ties.items():
			if winner == None:
				winner    = routine
				winnersum = self.__sum(place, self.places[routine])
				continue
			currentsum = self.__sum(place, self.places[routine])
			
			rcount = self.relative_placements[routine][place]
			if not isinstance(rcount, dict):
				self.relative_placements[routine][place] = {
					'count':rcount, 'sum':currentsum
				}
			wcount = self.relative_placements[winner][place]
			if not isinstance(wcount, dict):
				self.relative_placements[winner][place] = {
					'count':wcount, 'sum':winnersum
				}
			if currentsum < winnersum: 
				winner    = routine
				winnersum = currentsum
				tie = dict() # reset the ties
			elif currentsum == winnersum: 
				tie[winner]  = self.places[winner]
				tie[routine] = self.places[routine]
		if len(tie) > 0:
			x = len(tie)
			for routine in tie:
				del ties[routine]
			self.__down(tie, place+1, placement)
			self.__ties(ties, place, placement+x)
			return
		self.final_placements[winner] = placement
		del ties[winner]
		self.__ties(ties, place, placement+1)
	
	def __down(self, ties, place, placement):
		if place > len(self.places):
			self.__chiefjudgetie(ties, placement)
			return
		if len(ties) == 0:
			return
		if len(ties) == 1:
			routine,_ = ties.popitem()
			self.final_placements[routine] = placement
			return
		tie = dict()
		winner      = None
		winnercount = None
		for routine, scores in ties.items():
			count = self.__count(place, scores)
			self.relative_placements[routine][place] = count 
			if winner == None:
				winner      = routine
				winnercount = self.__count(place, scores)
				continue
			currentcount = self.__count(place, scores)
			if currentcount == winnercount:
				tie[winner]  = self.places[winner]
				tie[routine] = self.places[routine]
			if currentcount > winnercount:
				winner      = routine
				winnercount = currentcount
				tie = dict()
		if len(tie) == 0:
			self.final_placements[winner] = placement
			del ties[winner]
			self.__down(ties, place, placement+1)
			return
		if len(tie) > 0:
			x = len(tie)
			for routine in tie:
				del ties[routine]
			self.__down(tie, place+1, placement)
			self.__ties(ties, place, placement+x)
			return
		self.__down(ties, place+1, placement)
	
	def __chiefjudgetie(self, ties, placement):
		headjudgescores = dict()
		for routine,_ in ties.items():
			headjudgescore = self.places[routine][self.headjudge]
			headjudgescores[headjudgescore] = routine
		for _,routine in headjudgescores.items():
			self.final_placements[routine] = placement
			placement += 1
		return

	# count the number of placements
	def __count(self, place, scores):
		num_places = sum([1 if s <= place else 0 for s in scores.values()])
		if not self.include:
			num_places = 0
			for j,s in scores.items():
				if s <= place and j is not self.headjudge:
					num_places += 1
		return num_places
	
	# sum all of the scores under a placements
	def __sum(self, place, scores):
		num_places = sum([s if s <= place else 0 for s in scores.values()])
		if not self.include:
			num_places = 0
			for j,s in scores.items():
				if s <= place and j is not self.headjudge:
					num_places += s
		return num_places
		
	def __str__(self):
		rp = self.relative_placements
		fp = self.final_placements
		
		placements = len(self.places)
		
		strng = 'order,'
		for j,_ in self.places[1].items():
			strng += ' J%-2d,' % j
		
		for i in range(placements):
			strng += ' 1-%-2d,' % (i+1)
		strng += 'placement\n'
		
		for routine, scores in self.places.items():
			# print the routine and it's score
			strng += '%5s,' % routine
			for _, score in scores.items():
				strng += '%2s,' % score
			# print the routine's relative placement count
			for i in range(placements):
				count = rp[routine][i+1] if i+1 in rp[routine] else '---->'
				if isinstance(count, dict):
					count = '%s(%s)' % (count['count'], count['sum'])
				count = count if count != 0 else '-----'
				strng += '%5s,' % count
			# print the final placements
			strng += '%2s\n' % fp[routine]
		return strng

	def pprint_relative_placements(self):
		for k,v in self.relative_placements.items():
			print '%2s :' % k,
			for key,val in v.items():
				print val,
			print
		print

	def pprint_final_placements(self):
		for k,v in self.final_placements.items():
			print '%2s :' % k, v
		print
		
	def pprint(self):
		rp = self.relative_placements
		fp = self.final_placements
		
		places = self.places.copy()
		placements = len(places)
		_,judges = places.popitem()
		numjudges = len(judges)
		
		seprt  = '---------------++'
		seprt += '-'*(numjudges*6-1)+'++'
		seprt += '-'*(len(fp)*6-1)+'++'
		seprt += '----------\n'
		
		seprt2  = '---------------++'
		seprt2 += '-----+'*(numjudges)+'+'
		seprt2 += '-----+'*(len(fp))+'+'
		seprt2 += '----------\n'
		
		strng =  '               ||'
		strng += str.center('Judge Placement',   numjudges*6-1) + '||'
		strng += str.center('Relative Placement',len(fp)*6-1) + '||\n'
		strng += seprt
		strng += ' Routine Order ||'
		
		for j,_ in self.places[1].items():
			strng += '  J%-2d|' % j
		
		strng += '|'
		
		for i in range(placements):
			strng += ' 1-%-2d|' % (i+1)
		strng += '|Placements\n' + seprt2
		
		for routine, scores in self.places.items():
			# print the routine and it's score
			strng += '%13s  ||' % routine
			for _, score in scores.items():
				strng += '%3s  |' % score
			strng += '|'
			# print the routine's relative placement count
			for i in range(placements):
				count = rp[routine][i+1] if i+1 in rp[routine] else '---->'
				if isinstance(count, dict):
					count = '%s(%s)' % (count['count'], count['sum'])
				count = count if count != 0 else '-----'
				strng += '%5s|' % count
			# print the final placements
			strng += '|%5s\n' % fp[routine] + seprt2
		print strng


scores = {
	1 : {1:1, 2:1, 3:3, 4:2, 5:3},
	2 : {1:6, 2:5, 3:4, 4:1, 5:2},
	3 : {1:2, 2:4, 3:1, 4:5, 5:5},
	4 : {1:4, 2:2, 3:5, 4:6, 5:6},
	5 : {1:5, 2:6, 3:2, 4:3, 5:4},
	6 : {1:3, 2:3, 3:6, 4:4, 5:1}
}

test_chief_judge = {
	1 : {1:1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1},
	2 : {1:2, 2:3, 3:2, 4:3, 5:2, 6:3, 7:3},
	3 : {1:3, 2:2, 3:3, 4:2, 5:3, 6:2, 7:2},
	4 : {1:4, 2:4, 3:4, 4:4, 5:4, 6:4, 7:4}
}

tjScores = {
	1  : {1:2 , 2:6 , 3:6 , 4:3 , 5:6 , 6:5 },
	2  : {1:3 , 2:1 , 3:1 , 4:2 , 5:1 , 6:1 },
	3  : {1:4 , 2:5 , 3:4 , 4:11, 5:7 , 6:4 },
	4  : {1:11, 2:11, 3:7 , 4:4 , 5:8 , 6:9 },
	5  : {1:5 , 2:10, 3:11, 4:9 , 5:3 , 6:7 },
	6  : {1:6 , 2:3 , 3:3 , 4:6 , 5:5 , 6:6 },
	7  : {1:1 , 2:2 , 3:2 , 4:1 , 5:2 , 6:2 },
	8  : {1:7 , 2:8 , 3:5 , 4:5 , 5:4 , 6:3 },
	9  : {1:8 , 2:4 , 3:9 , 4:7 , 5:9 , 6:11},
	10 : {1:9 , 2:9 , 3:8 , 4:10, 5:11, 6:10},
	11 : {1:10, 2:7 , 3:10, 4:8 , 5:10, 6:8 }
}

new_scores = {
    '1': {   '1': 1, '2': 1, '3': 3, '4': 2, '5': 3},
    '2': {   '1': 6, '2': 5, '3': 4, '4': 1, '5': 2},
    '3': {   '1': 2, '2': 4, '3': 1, '4': 5, '5': 5},
    '4': {   '1': 4, '2': 2, '3': 5, '4': 6, '5': 6},
    '5': {   '1': 5, '2': 6, '3': 2, '4': 3, '5': 4},
    '6': {   '1': 3, '2': 3, '3': 6, '4': 4, '5': 1}
}

if __name__ == '__main__':
    placements = Relative_Placements(new_scores, 7, 3, False)
    print placements