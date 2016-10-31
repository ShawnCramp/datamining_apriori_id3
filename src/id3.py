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
        # self.attr_length = {}  # Number of Times Attribute Appears
        self.attr_position = {}  # Attribute Column position in 2d Array

        # Class Variables
        # self.class_options = []  # End Result Options

        # Dataset
        self._values = []  # Array of Data

        # Calculate Entropy
        # self.class_entropy = 0

        # Execute Populate during Initialize
        self.__options()
        self.__populate()

    def __options(self):
        """
        Private Function

        Read Imported Options File and Interperet Information
        :return:
        """
        # Open File Handle and Read Lines
        lines = open(self.options_file).readlines()

        # Loop through all dataset options to get attributes and classes
        for i, line in enumerate(lines):

            # Find Name of the Attribute or Class
            col = line.find(':')
            attr_name = line[:col].strip()

            self.attr_position[attr_name] = i - 1
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
        print('Number of Attributes: %d' % attr_count)

        # Loop through all entries in the data set
        for line in datalines:

            # If line does not contain missing information then keep the line
            if line.find("?") == -1:

                # Strip CRs and Split data into an array at append it to the global array
                instance = line.strip().replace(' ', '').split(',')
                if len(instance) == attr_count:
                    self._values.append(instance)
                else:
                    sys.exit('All Data Instances must be the same length')

    def __attr_count(self, attr, values):
        """
        Count the number of times an attr appears
        :return:
        """
        # Get Attribute Column position
        position = self.attr_position[attr]

        count = {}
        for instance in values:
            val = instance[position]
            if val not in count:
                count[val] = 1
            else:
                count[val] += 1

        return count

    def __entropy(self, attr, values):
        """
        Calculate Global Class Entropy level
        :return:
        """
        # Get number of instances in the dataset
        data_count = len(values)
        options = self.attr_options[attr]
        position = self.attr_position[attr]
        op_counter = {}

        if options[0] == 'continuous':
            op_counter = self.__attr_count(attr, self._values)
        else:
            # Loop through options
            for op in options:
                counter = 0

                # Count number of times class option appears in instance results
                for instance in values:
                    if instance[position] == op:
                        counter += 1

                # Append the count array for calculations
                op_counter[op] = counter

        print(op_counter)
        print('Data Count: %d' % data_count)

        # Calculate Entropy
        entropy = 0
        for key, value in op_counter.iteritems():
            if value != 0:
                percent = float(value) / data_count
                entropy -= percent * math.log10(percent)

        print('%s Resulting Entropy: %f\n' % (attr, entropy))
        return entropy

    def __attr_entropy(self):
        pass

    def __gain(self):
        pass

    def __reduction(self):
        pass

    def calc_entropy(self):
        """
        Calculate Entropy levels of Dataset and Create Flow Chart
        """
        gains = {}
        global_entropy = self.__entropy(attr='class', values=self._values)

        for key, value in self.attr_options.iteritems():
            if key != 'class':
                entropy = self.__entropy(attr=key, values=self._values)
                g = entropy - global_entropy
                gains[key] = g

        print(gains)


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
    dataset.calc_entropy()


if __name__ == '__main__':
    main()
