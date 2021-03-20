from unittest import TestCase, main
from unittest.mock import patch

def create_penguin(PenguinID, FirstName, LastName, date, District, VaccineNumber, Medic):
	pass
	
def create_center(CenterID, District, open_HH, open_MM, close_HH, close_MM, FreeVaccines):
	pass
	
def register_penguin(PenguinID, centers = None, days = None):
	# None centers means all centers
	# None days means always
	pass
	
def change_registration_centers(PenguinID, *IDs):
	pass
	
def change_registration_times(PenguinID):
	pass

	
class Day:
	def __init__(self, day_number, start_hh = 0, start_mm = 0, end_hh = 23, end_mm = 59, remove = False):
		self.day_number = day_number
		self.start_hh = start_hh
		self.start_mm = start_mm
		self.end_hh = end_hh
		self.end_mm = end_mm
		self.remove = remove
	def __eq__(self, other):
		return self.day_number == other.day_number and self.start_hh == other.start_hh and self.start_mm == other.start_mm and self.end_hh == other.end_hh and self.end_mm == other.end_mm
	def __repr__(self):
		return "Day {} from {:02d}:{:02d} to {:02d}:{:02d}".format(self.day_number, self.start_hh, self.start_mm, self.end_hh, self.end_mm)

class Parser:
	def __init__(self):
		pass
	
	def _pop(self, string):
		if string == "":
			raise SyntaxError("string is empty")
		return string.split()[0], " ".join(string.split()[1:])
	
	def parse(self, command):
		command_branches = [
			self._parse_literal_create_penguin,
			self._parse_literal_create_center,
			self._parse_literal_register_penguin,
			self._parse_literal_change_registration_centers,
			self._parse_literal_change_registration_times,
		]
		for command_branch in command_branches:
			try:
				function, args = command_branch(command)
				return function, args 
			except SyntaxError:
				pass
		raise SyntaxError("Unknown command {}".format(command))
	
	def _parse_literal_change_registration_times(self, command):
		argument, shortened_command = self._pop(command)
		if argument == 'CHANGEREGISTRATIONTIMES':
			function, args = self._change_registration_times_parse_literal_always_or_day(shortened_command)
			return function, args 
		else:
			raise SyntaxError("Expected CHANGEREGISTRATIONTIMES, got {} instead".format(argument))
		
			
	def _change_registration_times_parse_literal_always_or_day(self, command):
		argument, shortened_command = self._pop(command)
		if argument == 'ALWAYS':
			function, args = change_registration_times, [None]
			return function, args 
		elif argument == 'DAY':
			function, args = self._change_registration_times_parse_recursive_int_day(shortened_command)
			return function, args 
		else:
			raise SyntaxError("Expected ALWAYS or DAY, got {} instead".format(argument))
			
	def _change_registration_times_parse_recursive_int_day(self, command, days = None):
		argument, shortened_command = self._pop(command)
		if days == None: days = []
		try:
			days.append(Day(int(argument)))
			function, args = self._change_registration_times_parse_int_start_hh_or_next_day_or_not(shortened_command, days)
			return function, args 
		except ValueError:
			pass
			
	def _change_registration_times_parse_int_start_hh_or_next_day_or_not(self, command, days):
		if command == "":
			return change_registration_times, [days]
		argument, shortened_command = self._pop(command)
		if argument == 'DAY':
			function, args = self._change_registration_times_parse_recursive_int_day(shortened_command, days)
			return function, args 
		elif argument == 'NOT':
			days[-1].remove = True
			function, args = self._change_registration_times_parse_int_start_hh_or_next_day_or_not(shortened_command, days)
			return function, args
		else:
			try:
				days[-1].start_hh = int(argument)
				function, args = self._change_registration_times_parse_int_start_mm(shortened_command, days)
				return function, args 
			except:
				raise SyntaxError("Expected DAY or integer, got {} instead".format(argument))
				
	def _change_registration_times_parse_int_start_mm(self, command, days):
		argument, shortened_command = self._pop(command)
		try:
			days[-1].start_mm = int(argument)
			function, args = self._change_registration_times_parse_int_end_hh(shortened_command, days)
			return function, args 
		except:
			raise SyntaxError("Expected integer, got {} instead".format(argument))
			
	def _change_registration_times_parse_int_end_hh(self, command, days):
		argument, shortened_command = self._pop(command)
		try:
			days[-1].end_hh = int(argument)
			function, args = self._change_registration_times_parse_int_end_mm(shortened_command, days)
			return function, args 
		except:
			raise SyntaxError("Expected integer, got {} instead".format(argument))
			
	def _change_registration_times_parse_int_end_mm(self, command, days):
		argument, shortened_command = self._pop(command)
		try:
			days[-1].end_mm = int(argument)
			function, args = self._change_registration_times_parse_int_start_hh_or_next_day_or_not(shortened_command, days)
			return function, args 
		except:
			raise SyntaxError("Expected integer, got {} instead".format(argument))
	
	def _parse_literal_change_registration_centers(self, command):
		argument, shortened_command = self._pop(command)
		if argument == 'CHANGEREGISTRATIONCENTERS':
			function, args = change_registration_centers, [int(i) for i in shortened_command.split()]
			return function, args
		else:
			raise SyntaxError("Expected REGISTERPENGUIN, got {} instead".format(argument))
			
	def _parse_literal_register_penguin(self, command):
		argument, shortened_command = self._pop(command)
		if argument == 'REGISTERPENGUIN':
			function, args = self._register_penguin_parse_literal_all_or_centers(shortened_command)
			return function, args 
		else:
			raise SyntaxError("Expected REGISTERPENGUIN, got {} instead".format(argument))
			
	def _register_penguin_parse_literal_all_or_centers(self, command):
		argument, shortened_command = self._pop(command)
		if argument == 'ALL':
			function, args = self._register_penguin_parse_literal_always_or_day(shortened_command)
			args.insert(0,None)
			return function, args 
		elif argument == 'CENTERS':
			function, args = self._register_penguin_parse_recursive_int_center(shortened_command)
			return function, args 
		else:
			raise SyntaxError("Expected ALL or CENTERS, got {} instead".format(argument))
	
	def _register_penguin_parse_recursive_int_center(self, command, centers = None):
		argument, shortened_command = self._pop(command)
		if centers == None: centers = []
		try:
			centers.append(int(argument))
			function, args = self._register_penguin_parse_recursive_int_center(shortened_command, centers)
			return function, args 
		except ValueError:
			function, args = self._register_penguin_parse_literal_always_or_day(command)
			args.insert(0, centers)
			return function, args 
		
			
	def _register_penguin_parse_literal_always_or_day(self, command):
		argument, shortened_command = self._pop(command)
		if argument == 'ALWAYS':
			function, args = register_penguin, [None]
			return function, args 
		elif argument == 'DAY':
			function, args = self._register_penguin_parse_recursive_int_day(shortened_command)
			return function, args 
		else:
			raise SyntaxError("Expected ALWAYS or DAY, got {} instead".format(argument))
			
	def _register_penguin_parse_recursive_int_day(self, command, days = None):
		argument, shortened_command = self._pop(command)
		if days == None: days = []
		try:
			days.append(Day(int(argument)))
			function, args = self._register_penguin_parse_int_start_hh_or_next_day(shortened_command, days)
			return function, args 
		except ValueError:
			pass
			
	def _register_penguin_parse_int_start_hh_or_next_day(self, command, days):
		if command == "":
			return register_penguin, [days]
		argument, shortened_command = self._pop(command)
		if argument == 'DAY':
			function, args = self._register_penguin_parse_recursive_int_day(shortened_command, days)
			return function, args 
		else:
			try:
				days[-1].start_hh = int(argument)
				function, args = self._register_penguin_parse_int_start_mm(shortened_command, days)
				return function, args 
			except:
				raise SyntaxError("Expected DAY or integer, got {} instead".format(argument))
				
	def _register_penguin_parse_int_start_mm(self, command, days):
		argument, shortened_command = self._pop(command)
		try:
			days[-1].start_mm = int(argument)
			function, args = self._register_penguin_parse_int_end_hh(shortened_command, days)
			return function, args 
		except:
			raise SyntaxError("Expected integer, got {} instead".format(argument))
			
	def _register_penguin_parse_int_end_hh(self, command, days):
		argument, shortened_command = self._pop(command)
		try:
			days[-1].end_hh = int(argument)
			function, args = self._register_penguin_parse_int_end_mm(shortened_command, days)
			return function, args 
		except:
			raise SyntaxError("Expected integer, got {} instead".format(argument))
			
	def _register_penguin_parse_int_end_mm(self, command, days):
		argument, shortened_command = self._pop(command)
		try:
			days[-1].end_mm = int(argument)
			function, args = self._register_penguin_parse_int_start_hh_or_next_day(shortened_command, days)
			return function, args 
		except:
			raise SyntaxError("Expected integer, got {} instead".format(argument))
	
	def _parse_literal_create_center(self, command):
		argument, shortened_command = self._pop(command)
		if argument == 'CREATECENTER':
			cpargs = shortened_command.split()
			if len(cpargs) != 7: raise SyntaxError("Incorrect number of arguments")
			try:
				function, args = create_center, [int(cpargs[0]),int(cpargs[1]),int(cpargs[2]),int(cpargs[3]),int(cpargs[4]),int(cpargs[5]),int(cpargs[6])]
				return function, args 
			except Exception:
				raise SyntaxError("Expected an integer")
		else:
			raise SyntaxError("Expected CREATECENTER, got {} instead".format(argument))

	
	def _parse_literal_create_penguin(self, command):
		argument, shortened_command = self._pop(command)
		if argument == 'CREATEPENGUIN':
			cpargs = shortened_command.split()
			if len(cpargs) != 7: raise SyntaxError("Incorrect number of arguments")
			try:
				function, args = create_penguin, [int(cpargs[0]),cpargs[1],cpargs[2],cpargs[3],int(cpargs[4]),int(cpargs[5]),int(cpargs[6])]
				return function, args 
			except Exception:
				raise SyntaxError("Expected an integer")
		else:
			raise SyntaxError("Expected CREATEPENGUIN, got {} instead".format(argument))
	
			
class TestParser(TestCase):
	def test_create_penguin_parser(self):
		parser = Parser()
	
	def test_create_penguin(self):
		'''“CREATEPENGUIN PenguinID FirstName LastName YYYY-MM-DD District VaccineNumber Medic” - query to add a penguin to the database, in which:

			The YYYY MM DD is converted to the desired form.
			If the penguin is older than 30 years (year = 365 days) or has a date of birth after the currentDate, nothing will change in the database.
			The ranking priority is calculated according to the following criteria:
			Penguins with a larger VaccineNumber take precedence.
			If the value of the parameter medic = 1 (penguin is medic) then it takes precedence over all non-medic penguins.
			Penguins older than oldAge have higher priority than younger penguins.
			Each priority level is assigned a number from 1 to N where N is the highest priority (N = VaccinationLimit * 2 (medic / nonmedic) * 2 (old / not old)).'''
		parser = Parser()
		function, args = parser.parse("CREATEPENGUIN 0 John Smith 1997-07-20 3 5 0")
		self.assertEqual(function, create_penguin)
		self.assertEqual(args, [0, 'John', 'Smith', '1997-07-20', 3, 5, 0])
		
		self.assertRaises(SyntaxError, parser.parse, "CREATEPENGUIN b John Smith 1997-07-20 3 5 0")
		self.assertRaises(SyntaxError, parser.parse, "CREATEPENGUIN 0 John Smith 1997-07-20 y 5 0")
		self.assertRaises(SyntaxError, parser.parse, "CREATEPENGUIN 0 John Smith 1997-07-20 3 x 0")
		self.assertRaises(SyntaxError, parser.parse, "CREATEPENGUIN 0 John Smith 1997-07-20 3 5 c")
		self.assertRaises(SyntaxError, parser.parse, "CREATEPENGUIN 0 John Smith 1997-07-20 3 5 0 extra_stuff")
		self.assertRaises(SyntaxError, parser.parse, "CREATEPENGUI 0 John Smith 1997-07-20 3 5 0")
		self.assertRaises(SyntaxError, parser.parse, "CREATEPENGUIN 0 John Smith 1997-07-20 3 5")
		self.assertRaises(SyntaxError, parser.parse, "CREATEPENGUIN 0 John Smith 1997-07-20 3")
		
	def test_create_center(self):
		'''“CREATECENTER CenterID District HH ​​MM HH MM FreeVaccines” - a new center will be added to the query. The first HH MM represents WorkFrom and the second WorkTill.'''
		parser = Parser()
		function, args = parser.parse("CREATECENTER 3 2 08 00 18 30 1")
		self.assertEqual(function, create_center)
		self.assertEqual(args, [3, 2, 8, 0, 18, 30, 1])
		
		self.assertRaises(SyntaxError, parser.parse, "CREATECENTER x 2 08 00 18 30 1")
		self.assertRaises(SyntaxError, parser.parse, "CREATECENTER 3 x 08 00 18 30 1")
		self.assertRaises(SyntaxError, parser.parse, "CREATECENTER 3 2 xx 00 18 30 1")
		self.assertRaises(SyntaxError, parser.parse, "CREATECENTER 3 2 08 xx 18 30 1")
		self.assertRaises(SyntaxError, parser.parse, "CREATECENTER 3 2 08 00 xx 30 1")
		self.assertRaises(SyntaxError, parser.parse, "CREATECENTER 3 2 08 00 18 xx 1")
		self.assertRaises(SyntaxError, parser.parse, "CREATECENTER 3 2 08 00 18 30 x")
		self.assertRaises(SyntaxError, parser.parse, "CREATECENTE 3 2 08 00 18 30 1")
		self.assertRaises(SyntaxError, parser.parse, "CREATECENTER 3 2 08 00 18 30")
		self.assertRaises(SyntaxError, parser.parse, "CREATECENTER 3 2 08 00 18")
		
	def test_register_penguin(self):
		'''“REGISTERPENGUIN PenguinID ARG1 ARG2” - a query that adds Penguin to WaitingList and sets when it is able to go vaccinated.
			If the penguin has VaccineNumber> = vaccinationsLimit, then the operation will do nothing.
			Penguin's RegistrationID is generated depending on how many in total it is registered.
			ARG1 can take several forms:
			"ALL" - all centers currently open in its District will be added to the penguin ValidCenters.
			“CENTERS ID ID ID…. ID ”- the keyword centers and behind it all the centers he is willing to go to (if there is none, then take it as“ ALL ”).
			ARG2 can also take several forms:
			"ALWAYS" - can at any time.
			“DAY DAYNUMBER” - can all day DAY (eg “DAY 0 DAY 4” - penguin has time all day Monday and Friday).
			“DAY DAYNUMBER HH MM HH MM” (eg “DAY 0 1 0 19 30 DAY 1 DAY 4 16 0 20 0” - the penguin can on Monday from 1AM to 7:30 PM, all Tuesday and Friday from 4PM to 8PM).
			In CENTERS arguments, centers will not be repeated but may not exist. In DAY arguments, days will not be repeated.
		'''
		parser = Parser()
		function, args = parser.parse("REGISTERPENGUIN ALL ALWAYS")
		self.assertEqual(function, register_penguin)
		self.assertEqual(args, [None, None])
		
		function, args = parser.parse("REGISTERPENGUIN CENTERS 0 1 2 ALWAYS")
		self.assertEqual(function, register_penguin)
		self.assertEqual(args, [[0,1,2], None])
		
		function, args = parser.parse("REGISTERPENGUIN ALL DAY 0 DAY 1 DAY 2")
		self.assertEqual(function, register_penguin)
		self.assertEqual(args, [None, [Day(0),Day(1),Day(2)]])
		
		function, args = parser.parse("REGISTERPENGUIN ALL DAY 0 08 00 13 45 DAY 1 DAY 2 10 30 11 15")
		self.assertEqual(function, register_penguin)
		self.assertEqual(args, [None, [Day(0,8,0,13,45),Day(1),Day(2,10,30,11,15)]])
		
		function, args = parser.parse("REGISTERPENGUIN CENTERS 4 5 6 DAY 0 08 00 13 45 DAY 1 DAY 2 10 30 11 15")
		self.assertEqual(function, register_penguin)
		self.assertEqual(args, [[4,5,6], [Day(0,8,0,13,45),Day(1),Day(2,10,30,11,15)]])
		
	def test_change_registration_centers(self):
		''' “CHANGEREGISTRATIONCENTERS PenguinID ID…. ID ”- the query changes the centers that suit the penguin.

			Unique Positive Argument ID - Adds centers with an ID among its ValidCenters.
			Unique Negative ID Argument - Removes centers with an ID from its ValidCenters.
			If the penguin should be left without a possible center, it will return the last one removed.
			As an example, penguin has registered centers in the system with ID 1 2 3. The query “CHANGEREGISTRATIONCENTERS -1 -2 -3” will do:

			Removes 1, 2 from its valid centers.
			It does not remove 3, otherwise it would have no valid Center.'''
	
		parser = Parser()
		function, args = parser.parse("CHANGEREGISTRATIONCENTERS 27 1 2 3")
		self.assertEqual(function, change_registration_centers)
		self.assertEqual(args, [27, 1,2,3])
	
	def test_change_registration_times(self):
		'''“CHANGEREGISTRATIONTIMES PenguinID ARG ARG…” - the query changes the times that suit the penguin. ARG can take several forms:

			"ALWAYS" - the penguin is always free.
			"DAY DAYNUMBER" - can all day.
			“DAY DAYNUMBER NOT” - cannot on a given day.
			“DAY DAYNUMBER HH MM HH MM” - changes the times of the day.
			Let's try to demonstrate the change of the example from REGISTERPENGUIN. Question “CHANGEREGISTRATIONTIMES 1 DAY 0 DAY 1 NOT DAY 2 2 30 20 30” penguins with ID = 1:

			Changes Monday to time from 0AM to 11:59 PM ~ 23:59.
			Removes Tuesday from the database.
			Adds free Wednesday through 2:30 AM to 8:30 PM.'''
		
		parser = Parser()
		function, args = parser.parse("CHANGEREGISTRATIONTIMES ALWAYS")
		self.assertEqual(function, change_registration_times)
		self.assertEqual(args, [None])
		
		function, args = parser.parse("CHANGEREGISTRATIONTIMES DAY 1 DAY 2 DAY 3")
		self.assertEqual(function, change_registration_times)
		self.assertEqual(args, [[Day(1),Day(2),Day(3)]])
		
		function, args = parser.parse("CHANGEREGISTRATIONTIMES DAY 1 DAY 2 NOT DAY 3 10 30 18 25")
		self.assertEqual(function, change_registration_times)
		self.assertEqual(args, [[Day(1),Day(2,remove=True),Day(3,10,30,18,25)]])
	
if __name__ == "__main__":
	main()