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
import operator
import copy
import time
import statistics
from graphviz import Digraph


""" ---------------------------------------------------------
Global Declarations ------------------------------------- """
ATTR_OPTIONS = {}
CONTINUOUS_RANGES = {}
ATTR_TYPE = {}
ID = 1
TREE = Digraph(comment='ID3 Decision Tree')

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
    def __init__(self, name, parent, depth, table):
        # print('\nNEW NODE {}'.format(name))
        # Attribute Result Associated with the Node
        self.name = name
        self.parent = parent

        # Graph Stuff
        global ID
        self.graph_id = str(ID)
        TREE.node(str(ID), label=str(name))
        if name != 'Root':
            TREE.edge(parent.graph_id, str(ID))
        ID += 1

        # Table Associated with the Node
        self.table = table

        # Node Depth
        self.depth = depth

        # Gain
        self.gain = {}

        # Leaf Children Below the Node
        # This will be of length 1 if it is a result
        self.class_entropy = None
        self.children = []

        # Find Children
        self._find_children()

        child_str = ''
        for x in self.children:
            try:
                child_str += str(x.name) + ', '
            except Exception:
                child_str += x + ', '
        # print('Node: {} - Parent: {} - Children: {}'.format(self.name, self.parent, child_str))

    def __str__(self):
        return 'Node: {}'.format(self.name)

    def _find_range_index(self, attr, value):
        """
        Find Continuous Value Range Index
        :param value:
        :return:
        """
        domain = ATTR_OPTIONS[attr]

        if value < domain[1]:
            return 0
        elif domain[1] <= value < domain[2]:
            return 1
        elif domain[2] <= value < domain[3]:
            return 2
        elif domain[3] <= value < domain[4]:
            return 3
        elif domain[4] <= value < domain[5]:
            return 4
        elif domain[5] <= value < domain[6]:
            return 5
        elif domain[6] <= value < domain[7]:
            return 6
        elif domain[7] <= value < domain[8]:
            return 7
        else:
            return 8

    def _get_new_table(self, attr, option):
        """
        Get New Table associated with the passed Attribute and Option
        :param attr:
        :param option:
        :return:
        """
        current = copy.deepcopy(self.table.rows)
        attributes = copy.deepcopy(self.table.attributes)

        position = attributes.index(attr)
        attributes.remove(attr)
        new = []

        for row in current:
            # All I need to do is see if row[position] is in a range, instead of equal to option
            if ATTR_TYPE[attr] == 'continuous':
                # print(row)
                # print('I AM {} AND MY POSITION IS {} AND MY VALUE IS {}'.format(attr, position, row[position]))
                thing = int(row[position])
                okay = ATTR_OPTIONS[attr]
                # print("option: {}".format(option))
                # print("thing: {}".format(thing))
                # print("okay: {}".format(okay))
                if len(okay) > okay.index(option):
                    upper_bound = option
                else:
                    upper_bound = okay[okay.index(option) + 1]

                if option <= thing <= upper_bound:
                    # print("Pruned")
                    # row.remove(thing)
                    row.remove(str(thing))
                    new.append(row)
                    # print(new)
                    # print()
            else:

                if row[position] == option:
                    row.remove(option)
                    new.append(row)

        return Table(attributes, new)

    def _find_children(self):
        """
        Find all Children to this Node
        :return:
        """
        global ID
        if len(self.table) == 0:
            self.children.append('Nothing')
            TREE.node(str(ID), label='No Result')
            TREE.edge(str(self.graph_id), str(ID))
            ID += 1

        elif self._breakout_check():
            self.children.append(self.table.rows[0][-1])

            TREE.node(str(ID), label=self.table.rows[0][-1])
            TREE.edge(str(self.graph_id), str(ID))
            ID += 1
        else:
            self._calculate_class_entropy()
            for attr in self.table.attributes:
                if attr != 'class':
                    self._entropy(attr)

            expand = max(self.gain.items(), key=operator.itemgetter(1))[0]
            # print('Expand On: {}'.format(expand))

            expansions = ATTR_OPTIONS[expand]
            if expansions[0] == 'continuous':
                position = self.table.attributes.index(expand)
                expansions = CONTINUOUS_RANGES[position]

            for option in expansions:
                table = self._get_new_table(expand, option)
                self.children.append(Node(name=option, parent=self, depth=self.depth+1, table=table))

    def _breakout_check(self):
        """
        Determine if the Node points to only one answer.  If so, it is a breakout Node
        and will have a Result instead of Leaf Nodes
        """
        current = self.table.rows[0][-1]
        for row in self.table.rows:
            if row[-1] != current:
                return False
        return True

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

    def _attr_counter(self, attr, attr_options, position, class_options, continuous):
        """
        Get Number of times an Attribute Appears
        :param attr:
        :attr_options:
        :return:
        """

        # Dictionary containing count of Appearance of Attributes
        attribute_counter = dict.fromkeys(attr_options, 0)
        option_class_counter = {}

        if continuous:

            for option in attr_options:
                class_dictionary = dict.fromkeys(class_options, 0)
                option_class_counter[option] = class_dictionary

            # Loop through all attribute options and count
            # the number of times it appears in the data set

            for row in self.table.rows:
                domain_position = self._find_range_index(attr, int(row[position]))
                attribute_counter[attr_options[domain_position]] += 1
                at = option_class_counter[attr_options[domain_position]]
                at[row[-1]] += 1

        else:

            for option in attr_options:
                class_dictionary = dict.fromkeys(class_options, 0)
                option_class_counter[option] = class_dictionary

            # Loop through all attribute options and count
            # the number of times it appears in the data set
            for row in self.table.rows:
                attribute_counter[row[position]] += 1

                attr = option_class_counter[row[position]]
                attr[row[-1]] += 1

        return attribute_counter, option_class_counter

    def _attr_class_counter(self, attr_options, position, class_options):
        """
        Get Number of times each Class Option appears for the passed attribute
        :param attr:
        :param class_options:
        :return:
        """
        option_class_counter = {}
        for option in attr_options:
            class_dictionary = dict.fromkeys(class_options, 0)
            option_class_counter[option] = class_dictionary

        for row in self.table.rows:
            attr = option_class_counter[row[position]]
            attr[row[-1]] += 1

        return option_class_counter

    @staticmethod
    def _attr_entropy_calculator(attribute_counter, option_class_counter, data_length):
        """
        Calculate Class Appearance over Attribute total appearance entropy
        :param attr:
        :param class_count:
        :return:
        """
        entropy = 0
        for key_one, op in option_class_counter.items():
            temp = 0
            for key2, sel in op.items():
                if sel != 0:
                    div = float(sel) / attribute_counter[key_one]
                    temp -= div * math.log2(div)

            entropy += (float(attribute_counter[key_one]) / data_length) * temp

        return entropy

    def _entropy(self, attr):
        """
        Calculate Global Class Entropy Level
        :return:
        """

        # Get number of instances in the dataset
        data_length = len(self.table)
        options = ATTR_OPTIONS[attr]  # Options for the Attribute header
        position = self.table.attributes.index(attr)

        # Find out if attribute is continuous
        continuous = False
        thing = ATTR_TYPE[attr]
        if thing == 'continuous':
            # options = CONTINUOUS_RANGES[position]
            continuous = True

        # Steps for Entropy
        # Get Number of times each attribute appears
        class_options = ATTR_OPTIONS['class']
        attribute_counter, option_class_counter = self._attr_counter(
            attr=attr,
            attr_options=options,
            position=position,
            class_options=class_options,
            continuous=continuous
        )

        # Get Number of times each class options shows up for each attribute option
        # class_options = ATTR_OPTIONS['class']
        # option_class_counter = self._attr_class_counter(
        #     attr_options=options,
        #     position=position,
        #     class_options=class_options
        # )

        # Calc Class Appearance over Attribute total appearance entropy
        # print(op_class_counter)
        entropy = self._attr_entropy_calculator(
            attribute_counter=attribute_counter,
            option_class_counter=option_class_counter,
            data_length=data_length
        )

        # Calculate Gain
        gain = self.class_entropy - entropy
        self.gain[attr] = gain

        return gain


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


def continuous_domains(set):
    """
    Calculate the Domain of the Continuous sets using the dictionary created
    when reading the dataset file.
    :param set:
        Dictionary containing all values in continuous dataset
    :return:
    """


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
        domain = line[col+1:].strip().replace(' ', '').split(',')
        ATTR_OPTIONS[attr_name] = domain
        if domain[0] == 'continuous':
            ATTR_TYPE[attr_name] = 'continuous'
        else:
            ATTR_TYPE[attr_name] = 'whatever'

    ATTR_TYPE['Root'] = 'whatever'

    return attributes


def interpret_dataset(datafile, attributes):
    # Open File Handle and Read Lines
    file = open(datafile).readlines()
    values = []

    # Get Dataset Attribute Count (Subtract 1 since the resulting class is not an attribute)
    attr_count = len(ATTR_OPTIONS)
    print('Number of Attributes: %d' % attr_count)

    # Make dictionary for continuous attributes
    continuous_dictionary = {}
    for attr, domain in ATTR_OPTIONS.items():
        if domain[0] == 'continuous':
            continuous_dictionary[attributes.index(attr)] = []

    # Loop through all entries in the data set
    for line in file:

        # If line does not contain missing information then keep the line
        if line.find("?") == -1:

            # Strip CRs and Split data into an array at append it to the global array
            instance = line.strip().replace(' ', '').split(',')
            if len(instance) == attr_count:
                values.append(instance)
                for position, domain in continuous_dictionary.items():
                    domain.append(int(instance[position]))

            else:
                sys.exit('All Data Instances must be the same length')

    for key, value in continuous_dictionary.items():
        # print(key)
        # print(value)
        # print(max(value))
        # print(min(value))
        s = int(max(value)) - int(min(value))
        r = round(s / 10)
        # print(r)
        domain = []
        for i in range(0, 9, 1):
            domain.append(min(value) + (i*r))

        domain.append(max(value))
        # print(domain)
        # print()

        CONTINUOUS_RANGES[key] = domain
        attr = attributes[key]
        ATTR_OPTIONS[attr] = domain

    return values


def main():
    # Init ID3 Dataset and Populate it from the DataSet File
    start = time.time()
    attributes = interpret_options(optionsfile='datasets/census_options.txt')
    values = interpret_dataset(datafile='datasets/census.txt', attributes=attributes)
    table = Table(attributes=attributes, rows=values)
    # print(ATTR_TYPE)
    tree = Node(name='Root', parent='Root', depth=0, table=table)
    print('\n------ RUN TIME - {} -------'.format(time.time() - start))
    TREE.render('test-output/round-table.gv')


if __name__ == '__main__':
    main()
