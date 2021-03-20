# Imports

# Define databse tables here

# This function will operate the whole database
def databaseOperator(vaccinationsLimit, currentDate, oldAge, printFile):
    # setup actual database here

    # do not change this
    while True:
        newCommand = yield
        # add your logic here
        print(newCommand) # remove in actual solution

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