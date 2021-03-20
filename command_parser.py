import argparse

class CommandParser:
	def __init__(self):
		self.parser = argparse.ArgumentParser()
		subparsers = self.parser.add_subparsers(dest="Command")
		
		'''“CREATEPENGUIN PenguinID FirstName LastName Date District VaccineNumber Medic”'''
		create_penguin_parser = subparsers.add_parser('CREATEPENGUIN')
		create_penguin_parser.add_argument('PenguinID',type=int)
		create_penguin_parser.add_argument('FirstName',type=str)
		create_penguin_parser.add_argument('LastName',type=str)
		create_penguin_parser.add_argument('Date',type=str)
		create_penguin_parser.add_argument('District',type=int)
		create_penguin_parser.add_argument('VaccineNumber',type=int)
		create_penguin_parser.add_argument('Medic',type=int)
		
		'''“CREATECENTER CenterID District HH ​​MM HH MM FreeVaccines”'''
		create_center_parser = subparsers.add_parser('CREATECENTER')
		create_center_parser.add_argument('CenterID',type=int)
		create_center_parser.add_argument('District',type=int)
		create_center_parser.add_argument('StartHH',type=int)
		create_center_parser.add_argument('StartMM',type=int)
		create_center_parser.add_argument('EndHH',type=int)
		create_center_parser.add_argument('EndMM',type=int)
		create_center_parser.add_argument('FreeVaccines',type=int)
		
		'''“REGISTERPENGUIN PenguinID ARG1 ARG2”'''
		register_penguin_parser = subparsers.add_parser('REGISTERPENGUIN')
		register_penguin_parser.add_argument('PenguinID',type=int)
		
		register_penguin_center_subparser = register_penguin_parser.add_subparsers(dest='Centers')
		
		all_centers_parser = register_penguin_center_subparser.add_parser('ALL')
		all_centers_parser_register_penguin_days_subparser = all_centers_parser.add_subparsers(dest='Days')
		all_centers_parser_register_always_days_parser = all_centers_parser_register_penguin_days_subparser.add_parser('ALWAYS')
		all_centers_parser_register_select_days_parser = all_centers_parser_register_penguin_days_subparser.add_parser('DAY')
		all_centers_parser_register_select_days_parser.add_argument('Days',type=int, nargs='+')
		
		select_centers_parser = register_penguin_center_subparser.add_parser('CENTERS')
		select_centers_parser.add_argument('Centers',type=int, nargs='+')
		select_centers_parser_register_penguin_days_subparser = select_centers_parser.add_subparsers(dest='Days')
		select_centers_parser_register_always_days_parser = select_centers_parser_register_penguin_days_subparser.add_parser('ALWAYS')
		
	def parse(self, command):
		return self.parser.parse_args(command.split())
		
		
from unittest import TestCase, main
	
class TestCommandParser(TestCase):
	def test_create_command_parser(self):
		parser = CommandParser()
	
	def test_create_penguin(self):
		'''“CREATEPENGUIN PenguinID FirstName LastName YYYY-MM-DD District VaccineNumber Medic” - query to add a penguin to the database, in which:
			The YYYY MM DD is converted to the desired form.
			If the penguin is older than 30 years (year = 365 days) or has a date of birth after the currentDate, nothing will change in the database.
			The ranking priority is calculated according to the following criteria:
			Penguins with a larger VaccineNumber take precedence.
			If the value of the parameter medic = 1 (penguin is medic) then it takes precedence over all non-medic penguins.
			Penguins older than oldAge have higher priority than younger penguins.
			Each priority level is assigned a number from 1 to N where N is the highest priority (N = VaccinationLimit * 2 (medic / nonmedic) * 2 (old / not old)).'''
		parser = CommandParser()
		args = parser.parse("CREATEPENGUIN 0 John Smith 1997-07-20 3 5 0")
		self.assertEqual(args.Command, "CREATEPENGUIN")
		self.assertEqual(args.PenguinID, 0)
		self.assertEqual(args.FirstName, "John")
		self.assertEqual(args.LastName, "Smith")
		self.assertEqual(args.Date, "1997-07-20")
		self.assertEqual(args.District, 3)
		self.assertEqual(args.VaccineNumber, 5)
		self.assertEqual(args.Medic, 0)
		
	def test_create_center(self):
		'''“CREATECENTER CenterID District HH ​​MM HH MM FreeVaccines” - a new center will be added to the query. The first HH MM represents WorkFrom and the second WorkTill.'''
		parser = CommandParser()
		args = parser.parse("CREATECENTER 3 2 08 00 18 30 1")
		self.assertEqual(args.Command, "CREATECENTER")
		self.assertEqual(args.CenterID, 3)
		self.assertEqual(args.District, 2)
		self.assertEqual(args.StartHH, 8)
		self.assertEqual(args.StartMM, 0)
		self.assertEqual(args.EndHH, 18)
		self.assertEqual(args.EndMM, 30)
		self.assertEqual(args.FreeVaccines, 1)
		
	def test_register_penguin_all_always(self):
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
		parser = CommandParser()
		args = parser.parse("REGISTERPENGUIN 0 ALL ALWAYS")
		self.assertEqual(args.Command, "REGISTERPENGUIN")
		self.assertEqual(args.PenguinID, 0)
		self.assertEqual(args.Centers, "ALL")
		self.assertEqual(args.Days, "ALWAYS")
	
	def test_register_penguin_centers_always(self):
		parser = CommandParser()
		args = parser.parse("REGISTERPENGUIN 8 CENTERS 0 1 2 ALWAYS")
		self.assertEqual(args.Command, "REGISTERPENGUIN")
		self.assertEqual(args.PenguinID, 8)
		self.assertEqual(args.Centers, [0,1,2])
		self.assertEqual(args.Days, "ALWAYS")
		
	def test_register_penguin_all_days(self):
		parser = CommandParser()
		args = parser.parse("REGISTERPENGUIN 10 ALL DAY 1 2 3")
		self.assertEqual(args.Command, "REGISTERPENGUIN")
		self.assertEqual(args.PenguinID, 10)
		self.assertEqual(args.Centers, "ALL")
		self.assertEqual(args.Days, [1,2,3])
	
if __name__ == "__main__":
	main()