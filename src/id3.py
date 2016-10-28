""" ---------------------------------------------------------
Author: Shawn Cramp
ID: 111007290
Author: Omar Farah
ID:
Author: Nick Hare
ID:
Description: CP465 Final Assignment
Date: October, 28th, 2016
-------------------------------------------------------------
Assignment Task:
The objective of this project is to implement two Data Mining
algorithms and test your implementations with various reasonably
large datasets. The term reasonably large is to be interpreted
as anywhere from a few hundreds to a few thousands instances (tuples).

You need to implement two Data Mining algorithms seen in class:
1. the ID3 algorithm, based on entropy/information gain, to build decision trees;
2. the Apriori algorithm for mining association rules;

-------------------------------------------------------------
Import Declarations ------------------------------------- """


""" ---------------------------------------------------------
Global Declarations ------------------------------------- """


""" ---------------------------------------------------------
Class Declarations -------------------------------------- """


class ID3:
    """
    DataSet class for containing the information from the imported
    dataset
    """
    def __init__(self, filename):
        self.filename = filename
        self._values = []

    def populate(self):
        """
        Read Dataset File and store information into self._values
        :return:
        """
        # Open File Handle and Read Lines
        datalines = open(self.filename).readlines()

        # Loop through all entries in the data set
        for line in datalines:

            # If line does not contain missing information then keep the line
            if line.find("?") == -1:

                # Split data into an array at append it to the global array
                dataelement = line.strip().split(",")
                self._values.append(dataelement)


""" ---------------------------------------------------------
Function Declarations ----------------------------------- """


""" ---------------------------------------------------------
Console Execution Functions ---------------------------------
All functions below are used for execution of the program and
are no involved in the logical process.
The Main function will be called upon code execution and the
user will be presented with a list of options on how to
proceed and view the code output he/she would like to view.
-------------------------------------------------------------
--------------------------------------------------------- """


def main():

    # Init ID3 Dataset and Populate it from the DataSet File
    dataset = ID3(filename='datasets/small_census.txt')
    dataset.populate()


if __name__ == '__main__':
    main()
