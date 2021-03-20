# Imports

# Define databse tables here

# This function will operate the whole database

def create_penguin(args):
	PenguinID = 	int(args[1])
	FirstName = 	args[2]
	LastName = 		args[3]
	Date = 			args[4]
	District = 		int(args[5])
	VaccineNumber = int(args[6])
	Medic = 		int(args[7])

def create_center(args):
	CenterID = 		int(args[1])
	District = 		int(args[2])
	StartHH = 		int(args[3])
	StartMM = 		int(args[4])
	EndHH = 		int(args[5])
	EndMM = 		int(args[6])
	FreeVaccines =	int(args[7])

'''======================================='''
''' SUPPORT FUNCTIONS FOR REGISTERPENGUIN '''
def register_penguin_parse_centers(args):
	if args[0] == "ALL": return "ALL", args[1:]
	pointer = 1
	centers = []
	while args[pointer] not in ["ALWAYS","DAY"]:
		centers.append(args[pointer])
		pointer += 1
	return centers, args[pointer:]

def register_penguin_parse_days(args):
	if args[0] == "ALWAYS": return "ALWAYS"
	pointer = 1
	days = []
	day = []
	while pointer < len(args):
		if args[pointer] == "DAY":
			days.append(day)
			day = []
		else:
			day.append(int(args[pointer]))
		pointer += 1
	return days
''' SUPPORT FUNCTIONS FOR REGISTERPENGUIN '''
'''======================================='''

def register_penguin(args):
	PenguinID = int(args[1])
	Centers, args = register_penguin_parse_centers(args[2:])
	Days = register_penguin_parse_days(args) #formatted as [[1],[0,8,0,13,45]]
	
def change_registration_center(args):
	PenguinID = int(args[1])
	IDs = [int(id) for id in args[2:]]

'''==============================================='''
''' SUPPORT FUNCTIONS FOR CHANGEREGISTRATIONTIMES '''
def change_registration_times_parse_days(args):
	if args[0] == "ALWAYS": return "ALWAYS"
	pointer = 1
	days = []
	day = []
	while pointer < len(args):
		if args[pointer] == "DAY":
			days.append(day)
			day = []
		else:
			if args[pointer] == "NOT": day.append("NOT")
			else: day.append(int(args[pointer]))
		pointer += 1
	return days
''' SUPPORT FUNCTIONS FOR CHANGEREGISTRATIONTIMES '''
'''==============================================='''

def change_registration_times(args):
	PenguinID = int(args[1])
	Days = change_registration_times_parse_days(args[2:]) #formatted as [[0, "NOT"],[1],[0,8,0,13,45]]

def print_registered(args):
	N = int(args[1])

def print_free_centers(args):
	District = int(args[1])

'''======================================='''
''' SUPPORT FUNCTIONS FOR PRINTVALIDTIMES '''
def print_valid_times_parse_times(args):
	pointer = 0
	times = []
	time = []
	state = "discover"
	while True:
		#print(state)
		if state == "discover":
			time.append(args[pointer])
			if args[pointer] == "ID": state = "get_id"
			if args[pointer] == "DAY": state = "get_day"
			pointer += 1
		elif state == "get_id":
			time.append(int(args[pointer]))
			pointer += 1
			if pointer+2 < len(args) and args[pointer] == "DAY" and args[pointer+2] in ["DAY","ID"]: 
				pointer += 1
				state = "get_day_after_id"
			elif len(args) - pointer == 2 and args[pointer] == "DAY": 
				pointer += 1
				state = "get_day_after_id"
			else: state = "add_time"
		elif state == "get_day":
			time.append(int(args[pointer]))
			pointer += 1
			if pointer >= len(args) : state = "add_time"
			elif pointer < len(args) and args[pointer] in ["DAY","ID"]: state = "add_time"
			else: state = "get_time_after_day"
		elif state == "get_day_after_id":
			time.append(int(args[pointer]))
			pointer += 1
			state = "add_time"
		elif state == "get_time_after_day":
			time.append(int(args[pointer+0]))
			time.append(int(args[pointer+1]))
			time.append(int(args[pointer+2]))
			time.append(int(args[pointer+3]))
			pointer += 4
			state = "add_time"
		elif state == "add_time":
			times.append(time)
			time = []
			if pointer >= len(args): return times
			state = "discover"
			
	return times
''' SUPPORT FUNCTIONS FOR PRINTVALIDTIMES '''
'''======================================='''

def print_valid_times(args):
	'''
	Format:
	PenguinID 		- ["ID", 0]
	PenguinID Day 	- ["ID", 0,1]
	Day				- ["DAY", 0]
	Daytime			- ["DAY", 0,8,0,13,45]
	'''
	Times = print_valid_times_parse_times(args[1:])

def find_appointments(args):
	'''
	Format:
	PenguinID 		- ["ID", 0]
	Date 			- ["DATE", '1995','01','01']
	Center			- ["CENTER", 1]
	Center Date		- ["CENTERDATE", 0,'1995','01','01']
	'''
	queries = []
	pointer = 1
	while pointer < len(args):
		if args[pointer] == "ID":
			PenguinID = int(args[pointer+1])
			pointer += 2
			queries.append(["ID", PenguinID])
		elif args[pointer] == "DATE":
			Date = [args[pointer+1], args[pointer+2], args[pointer+3]]
			pointer += 4
			queries.append(["DATE", Date])
		elif args[pointer] == "CENTER":
			CenterID = int(args[pointer+1])
			pointer += 2
			queries.append(["CENTER", CenterID])
		elif args[pointer] == "CENTERDATE":
			CenterID = int(args[pointer+1])
			Date = [args[pointer+2], args[pointer+3], args[pointer+4]]
			pointer += 5
			queries.append(["CENTERDATE", CenterID, Date])

def find_logged_vaccinations(args):
	'''
	Format:
	PenguinID 		- ["ID", 0]
	Date 			- ["DATE", '1995','01','01']
	Center			- ["CENTER", 1]
	Center Date		- ["CENTERDATE", 0,'1995','01','01']
	Level			- ["LEVEL", 1]
	'''
	queries = []
	pointer = 1
	while pointer < len(args):
		if args[pointer] == "ID":
			PenguinID = int(args[pointer+1])
			pointer += 2
			queries.append(["ID", PenguinID])
		elif args[pointer] == "DATE":
			Date = [args[pointer+1], args[pointer+2], args[pointer+3]]
			pointer += 4
			queries.append(["DATE", Date])
		elif args[pointer] == "CENTER":
			CenterID = int(args[pointer+1])
			pointer += 2
			queries.append(["CENTER", CenterID])
		elif args[pointer] == "CENTERDATE":
			CenterID = int(args[pointer+1])
			Date = [args[pointer+2], args[pointer+3], args[pointer+4]]
			pointer += 5
			queries.append(["CENTERDATE", CenterID, Date])
		elif args[pointer] == "LEVEL":
			VaccinationNumber = int(args[pointer+1])
			pointer += 2
			queries.append(["LEVEL", VaccinationNumber])

def give_statistic(args):
	#no arguments
	pass

def databaseOperator(vaccinationsLimit, currentDate, oldAge, printFile):
    # setup actual database here
	functions = {
		  'CREATEPENGUIN': create_penguin,
		  'CREATECENTER': create_center,
		  'REGISTERPENGUIN': register_penguin,
		  'CHANGEREGISTRATIONCENTERS': change_registration_center,
		  'CHANGEREGISTRATIONTIMES': change_registration_times,
		  'PRINTREGISTERED': print_registered,
		  'PRINTFREECENTERS': print_free_centers,
		  'PRINTVALIDTIMES':print_valid_times,
		  'FINDAPPOINTMENTS': find_appointments,
		  'FINDLOGGEDVACCINATIONS': find_logged_vaccinations,
		  'GIVESTATISTICS': give_statistic,
	}
	
    # do not change this
    while True:
        newCommand = yield
        args = newCommand.split()
		result = functions[args[0]](args)

"""------------------------------------------------------
         Basic python coprogram.
1. First call inicializes the coprogram.
2. Next, executes commands until yield.
3. Send, sends intpus into the coprogram.
   Inputs are saved in newCommand.
4. Rest of the while is executed utill yeild.
Remove excess prints or comments and write your solution.
---------------------------------------------------------"""
database = databaseOperator(3, date(2021,2,5), 18, "testfile.txt")
next(database)
database.send("Test input 1")
database.send("Test input 2")