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
import sys
import math


""" ---------------------------------------------------------
Global Declarations ------------------------------------- """


""" ---------------------------------------------------------
Class Declarations -------------------------------------- """


class ID3:
    """
    ID3 Implementation using the initialized dataset file
    """
    def __init__(self, filename, optionsfile):

        # File Handles
        self.filename = filename
        self.options_file = optionsfile

        # Attribute Variables
        self.attr_options = {}  # Options for each Attribute

        # Class Variables
        self.class_options = []  # End Result Options

        # Dataset
        self._values = []  # Array of Data

        # Execute Populate during Initialize
        self.__options()
        self.__populate()

        # Calculate Entropy
        self.class_entropy = self.__class_entropy()

    def __options(self):
        """
        Private Function

        Read Imported Options File and Interperet Information
        :return:
        """
        # Open File Handle and Read Lines
        lines = open(self.options_file).readlines()

        # Loop through all dataset options to get attributes and classes
        for line in lines:

            # Find Name of the Attribute or Class
            col = line.find(':')
            name = line[:col].strip()

            if name == 'class':
                # Interpret Class Options
                self.class_options = line[col+1:].strip().replace(' ', '').split(',')
            else:
                # Interpret Attribute Options
                attr_name = line[:col].strip()
                self.attr_options[attr_name] = line[col+1:].strip().replace(' ', '').split(',')

    def __populate(self):
        """
        Private Function

        Read Dataset File and store information into self._values
        :return:
        """
        # Open File Handle and Read Lines
        datalines = open(self.filename).readlines()

        # Get Dataset Attribute Count (Subtract 1 since the resulting class is not an attribute)
        attr_count = len(self.attr_options)
        print(attr_count)

        # Loop through all entries in the data set
        for line in datalines:

            # If line does not contain missing information then keep the line
            if line.find("?") == -1:

                # Strip CRs and Split data into an array at append it to the global array
                instance = line.strip().replace(' ', '').split(',')
                if len(instance) - 1 == attr_count:
                    self._values.append(instance)
                else:
                    sys.exit('All Data Instances must be the same length')

    def __class_entropy(self):
        """
        Calculate Global Class Entropy level
        :return:
        """
        # Get number of instances in the dataset
        data_count = len(self._values)
        class_count = []

        # Loop through class options
        for cl in self.class_options:
            print(cl)
            counter = 0

            # Count number of times class option appears in instance results
            for instance in self._values:
                if instance[-1] == cl:
                    counter += 1

            # Append the count array for calculations
            class_count.append(counter)

        # Calculate Entropy
        entropy = 0
        for value in class_count:
            percent = float(value) / data_count
            entropy -= percent * math.log(percent)

        print('Resulting Global Entropy: %f' % entropy)
        return entropy

    def __attr_entropy(self):
        pass

    def __gain(self):
        pass

    def __reduction(self):
        pass

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
    dataset = ID3(filename='datasets/small_census.txt', optionsfile='datasets/census_options.txt')


if __name__ == '__main__':
    main()
