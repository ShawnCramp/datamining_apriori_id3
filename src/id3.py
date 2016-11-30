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
ATTR_OPTIONS = {}

""" ---------------------------------------------------------
Class Declarations -------------------------------------- """


class Table:
    """
    Table of Data Rows used for each Node Instance of the ID3 Tree
    """
    def __init__(self, attributes, rows):
        self.attributes = attributes
        self.rows = rows

    def __len__(self):
        return len(self.rows)


class Node:
    def __init__(self, name, depth, table):

        # Attribute Result Associated with the Node
        self.name = name

        # Table Associated with the Node
        self.table = table

        # Node Depth
        self.depth = depth

        # Leaf Children Below the Node
        # This will be of length 1 of it is a result
        self.class_entropy = None
        self._calculate_class_entropy()
        self.children = None

        # Find Children
        self.find_children()

    def find_children(self):
        """
        Find all Children to this Node
        :return:
        """
        # class_entropy = self.entropy('class')
        highest_gain = 0
        expand = ''
        for attr in self.table.attributes:
            if attr != 'class':
                gain = self.entropy(attr)
                if gain > highest_gain:
                    expand = attr

        print(expand)

    def breakout_check(self):
        """
        Determine if the Node points to only one answer.  If so, it is a breakout Node
        and will have a Result instead of Leaf Nodes
        """

    def _calculate_class_entropy(self):
        """
        Calculate Global Class Entropy Level
        :return:
        """
        options = ATTR_OPTIONS['class']
        option_counter = {}
        for op in options:
            counter = 0
            for row in self.table.rows:
                if row[-1] == op:
                    counter += 1

            option_counter[op] = counter

        entropy = 0
        for op, value in option_counter.items():
            entropy -= (value / len(self.table)) * math.log2(value / len(self.table))

        self.class_entropy = entropy
        return

    def entropy(self, attr):
        """
        Calculate Global Class Entropy Level
        :return:
        """

        # Get number of instances in the dataset
        data_count = len(self.table)
        options = ATTR_OPTIONS[attr]  # Options for the Attribute header
        position = self.table.attributes.index(attr)

        # Steps for Entropy
        # Get Number of times each attribute appears
        attribute_counter = {}
        for op in options:
            counter = 0
            for row in self.table.rows:
                if row[position] == str(op):
                    counter += 1

            attribute_counter[op] = counter

        # Get Number of times each class options shows up for each attribute option
        class_options = ATTR_OPTIONS['class']
        op_class_counter = {}
        for op in options:
            class_counter = {}
            for co in class_options:
                counter = 0
                for row in self.table.rows:
                    if row[position] == str(op) and row[-1] == co:
                        counter += 1
                class_counter[co] = counter
            op_class_counter[op] = class_counter

        # Calc Class Appearance over Attribute total appearance entropy
        # print(op_class_counter)
        entropy = 0
        for key1, op in op_class_counter.items():

            temp = 0
            # print(op)
            for key2, sel in op.items():
                # print(sel)
                # print(attribute_counter[key1])
                if sel != 0:
                    div = float(sel) / attribute_counter[key1]
                    temp -= div * math.log(div, 2)

            entropy += (float(attribute_counter[key1]) / len(self.table)) * temp

        print('{} Entropy: {}'.format(attr, entropy))
        gain = self.class_entropy - entropy
        print('{} Gain: {}'.format(attr, gain))

        # Multiply Attribute Appearance by Entropy above
        # for key, op in op_class_counter.items():
        #     gain = None

        return gain

    class Meta:
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


def interpret_options(optionsfile):
    # Open File Handle and Read Lines
    lines = open(optionsfile).readlines()
    attributes = []

    # Loop through all dataset options to get attributes and classes
    for i, line in enumerate(lines):
        # Find Name of the Attribute or Class
        col = line.find(':')
        attr_name = line[:col].strip()
        attributes.append(attr_name)
        ATTR_OPTIONS[attr_name] = line[col+1:].strip().replace(' ', '').split(',')

    return attributes


def interpret_dataset(datafile):
    # Open File Handle and Read Lines
    datalines = open(datafile).readlines()
    values = []

    # Get Dataset Attribute Count (Subtract 1 since the resulting class is not an attribute)
    attr_count = len(ATTR_OPTIONS)
    print('Number of Attributes: %d' % attr_count)

    # Loop through all entries in the data set
    for line in datalines:

        # If line does not contain missing information then keep the line
        if line.find("?") == -1:

            # Strip CRs and Split data into an array at append it to the global array
            instance = line.strip().replace(' ', '').split(',')
            if len(instance) == attr_count:
                values.append(instance)
            else:
                sys.exit('All Data Instances must be the same length')

    return values


def main():
    # Init ID3 Dataset and Populate it from the DataSet File
    attributes = interpret_options(optionsfile='datasets/k_attributes.txt')
    values = interpret_dataset(datafile='datasets/k_dataset.txt')
    table = Table(attributes=attributes, rows=values)
    tree = Node(name='Root', depth=0, table=table)


if __name__ == '__main__':
    main()
