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

# Contains all Domain Options for Attributes
ATTR_OPTIONS = {}

# Contains Ranges of Continuous Attributes by Dataset Column number.  This won't work after first iteration of table
CONTINUOUS_RANGES = {}

# Contains whether an Attribute is Continuous or Categorical
ATTR_TYPE = {}

# Current Graphviz NODE ID
ID = 1

# Global Declaration of Graphviz Node
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
        """
        Node Object Declaration
        :param name:
            The Attribute Name the Node will evaluate
        :param parent:
            The Parent Attribute to this Node
        :param depth:
            The depth level of the Node into the Tree
        :param table:
            The Table Object associated with this Node
        """
        print('\nNEW NODE {}'.format(name))

        # Attribute Result Associated with the Node
        self.name = name
        self.parent = parent

        # Graph Stuff
        global ID
        self.graph_id = str(ID)
        TREE.node(str(ID), label=str(name))
        if name != 'Root':
            TREE.edge(parent.graph_id, str(ID), label='')
        ID += 1

        # Table Associated with the Node
        self.table = table

        # Node Depth
        self.depth = depth

        # Dictionary of Gain attached to each Attribute
        self.gain = {}

        # Leaf Children Below the Node
        # This will be of length 1 if it is a result
        self.class_entropy = None
        self.children = []

        # Find Children
        self._find_children()

        # This is just for printing to the console
        child_str = ''
        for x in self.children:
            try:
                child_str += str(x.name) + ', '
            except Exception:
                child_str += x + ', '
        print('Node: {} - Parent: {} - Children: {}'.format(self.name, self.parent, child_str))

    def __str__(self):
        return 'Node: {}'.format(self.name)

    def _get_new_table(self, attr, option):
        """
        Get New Table associated with the passed Attribute and Option
        :param attr:
        :param option:
        :return:
        """

        if ATTR_TYPE[attr] == 'continuous':
            continuous = True
            current = copy.deepcopy(self.table.rows)
        else:
            continuous = False
            current = copy.deepcopy(self.table.rows)

        print('Getting New Table')
        attributes = copy.deepcopy(self.table.attributes)
        position = attributes.index(attr)
        attributes.remove(attr)
        new = []

        print('\nCurrent Option Domain being Evaluated: {}\n'.format(option))

        for row in current:
            # All I need to do is see if row[position] is in a range, instead of equal to option
            if continuous:
                current_value = int(row[position])

                if current_value in option:
                    # row.remove(str(current_value))
                    del row[position]
                    new.append(row)

            else:

                if row[position] == option:
                    row.remove(option)
                    new.append(row)

        print('New Table Length: {}'.format(len(new)))
        return Table(attributes, new)

    def _inconclusive_check(self):
        """
        Check to see if results are Inconclusive.
        I.E.  The results have no more attributes to expand on but still have different class values
        :return:
        """
        print('Inconclusive Check')
        if len(self.table.attributes) == 1 and self.table.attributes[0] == 'class':
            print('Performing Inconclusive Loop')
            last = self.table.rows[0][-1]
            for row in self.table.rows:
                current = row[-1]
                if last != current:
                    print('\nResults from Branch are Inconclusive\n')
                    return True

                last = current

        return False

    def _find_children(self):
        """
        Find all Children to this Node
        :return:
        """
        global ID
        print('Finding Children')
        if len(self.table) == 0:

            # If length of Table is 0, then there are no results by following this path
            self.children.append('No Result')
            TREE.node(str(ID), label='No Result')
            TREE.edge(str(self.graph_id), str(ID))
            ID += 1

        elif self._breakout_check():

            # If all the Class Options are the same, then we have found a result
            self.children.append(self.table.rows[0][-1])

            TREE.node(str(ID), label=self.table.rows[0][-1])
            TREE.edge(str(self.graph_id), str(ID))
            ID += 1
        elif self._inconclusive_check():

            # If Results are Inconclusive then attach inconclusive node
            self.children.append('Inconclusive')
            TREE.node(str(ID), label='Inconclusive')
            TREE.edge(str(self.graph_id), str(ID))
            ID += 1
        else:

            # Find Children of Node
            # Calculate global Class Entropy
            self._calculate_class_entropy()

            # Find Entropy of all Attributes other then the Class
            for attr in self.table.attributes:
                if attr != 'class':
                    self._entropy(attr)

            # Determine the Attribute that received the highest GAIN value
            print('Current Gain Options: {}'.format(self.gain.items()))
            print('Attribute List: {}'.format(self.table.attributes))
            print('Number or Rows in Table: {}'.format(len(self.table)))
            expand = max(self.gain.items(), key=operator.itemgetter(1))[0]
            print('Expand On: {}'.format(expand))

            # This is happening because there are no attributes to expand on, however the classes are still
            # difference.  So in the end, the tree was in conclusive.

            # Expansions is the Domain of the Attribute we are expanding
            expansions = ATTR_OPTIONS[expand]
            print('Expanding on Domain Options: {}'.format(expansions))
            for option in expansions:
                table = self._get_new_table(expand, option)
                self.children.append(Node(name=option, parent=self, depth=self.depth+1, table=table))

    def _breakout_check(self):
        """
        Determine if the Node points to only one answer.  If so, it is a breakout Node
        and will have a Result instead of Leaf Nodes
        :return:
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

    def _attr_counter(self, attr_options, position, class_options, continuous):
        """
        Get Number of times an Attribute Appears
        :param attr_options:
        :param position:
        :param class_options:
        :param continuous:
        :return:
        """
        print('Attribute Counting')

        # Dictionary containing count of Appearance of Attributes
        attribute_counter = dict.fromkeys(attr_options, 0)
        option_class_counter = {}

        """
        Create Dictionary of Dictionaries for how many times Class Options Appear
        Ex:
            If Expanding on Education, and High-School is in the Domain of Education,
            one entry in the dictionary might look like this:

            option_class_counter = {
                'High-School': {
                    '>50k': 0,
                    '<=50k: 0
                }
            }
        """
        for option in attr_options:
            class_dictionary = dict.fromkeys(class_options, 0)
            option_class_counter[option] = class_dictionary

        # If the Attribute is Continuous, then we evaluate on a Range instead of Directly
        # against the option
        if continuous:

            # Loop through all attribute options and count
            # the number of times it appears in the data set
            for row in self.table.rows:
                # print('Current Attribute: {}'.format(attr))
                try:
                    for x, r in enumerate(attr_options):
                        if int(row[position]) in r:
                            entry_range = attr_options[x]
                            break
                except Exception as e:
                    for i in self.table.rows:
                        print(i)

                # print('{} in range {}'.format(row[position], entry_range))

                attribute_counter[entry_range] += 1
                at = option_class_counter[entry_range]
                at[row[-1]] += 1

        else:

            # Loop through all attribute options and count
            # the number of times it appears in the data set
            for row in self.table.rows:
                attribute_counter[row[position]] += 1

                # While looping, we count the number of times each class option appears
                # for the current domain option as well
                at = option_class_counter[row[position]]
                at[row[-1]] += 1

        return attribute_counter, option_class_counter

    def _attr_class_counter(self, attr_options, position, class_options):
        """
        Get Number of times each Class Option appears for the passed attribute
        :param attr_options:
        :param position:
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
        :param attribute_counter:
        :param option_class_counter:
        :param data_length:
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

        print('\nEntropy Calculation Successful: {}'.format(entropy))
        return entropy

    def _entropy(self, attr):
        """
        Calculate Global Class Entropy Level
        :param attr:
        :return:
        """

        # Get number of instances in the dataset
        data_length = len(self.table)

        # Domain Options for Attribute being Evaluated
        options = ATTR_OPTIONS[attr]

        # Column Position of Attribute
        position = self.table.attributes.index(attr)

        # Find out if attribute is continuous
        continuous = False
        if ATTR_TYPE[attr] == 'continuous':
            continuous = True

        # Steps for Entropy
        # Get Number of times each attribute appears
        class_options = ATTR_OPTIONS['class']
        attribute_counter, option_class_counter = self._attr_counter(
            attr_options=options,
            position=position,
            class_options=class_options,
            continuous=continuous
        )

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

        # Calculate Domain split for Continuous Attributes
        s = int(max(value)) - int(min(value))
        r = math.ceil(s / 10)
        domain = []
        for i in range(0, 10, 1):
            print(range(min(value)+(i*r), min(value)+(i*r+r)))
            domain.append(range(min(value)+(i*r), min(value)+(i*r+r)))

        attr = attributes[key]
        median = int(statistics.median(value))
        ATTR_OPTIONS[attr] = [range(min(value), median), range(median, max(value)+1)]
        print('-------------------------------------------------\n\n')
        print('RUN PROGRAM\n---------------------------------------------')

    return values


def main():
    # Initialize ID3 Dataset and Populate it from the DataSet File
    # Start Timer for Runtime Calculation
    start = time.time()

    # Interpret Attributes and Dataset File
    # Enter File names into parameter options
    attributes = interpret_options(optionsfile='datasets/k_attributes.txt')
    values = interpret_dataset(datafile='datasets/k_dataset.txt', attributes=attributes)

    # Create Table Object for Root Node using entire Dataset
    table = Table(attributes=attributes, rows=values)

    # Create Root Node
    tree = Node(name='Root', parent='Root', depth=0, table=table)
    print('\n------ RUN TIME - {} -------'.format(time.time() - start))

    # Render Graphviz Options File
    TREE.render('test-output/round-table.gv')

if __name__ == '__main__':
    main()
