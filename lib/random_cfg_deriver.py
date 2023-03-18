import sys
import random
from . import grammar
from . import variable
from . import variable_reference

DEBUG = 0

def parse_first_rule(line):
    rule = line.rstrip()
    variable_name, production = rule.split('=')
    return variable_name, production

def parse_alt_rule(line):
    rule = line.rstrip()
    return rule[1:]

def find_references(current_string):
    variable_references = []
    begin_index = 0
    end_index = 0
    is_variable = False
    for i,c in enumerate(current_string):
        # If the character is an upper case and the variable flag is off, we've
        # hit the beginning of a new variable, so turn the variable flag on, and
        # reset the begin and end index.
        if c.isupper() and not is_variable:
            is_variable = True
            begin_index = i
            end_index = i
        # Here we increment the end index of the current variable reference
        # we are counting.
        elif c.isupper() and is_variable:
            end_index += 1
        # If the character is not an upper case alphabet character and the
        # variable flag is on, it's the end of our variable reference substring.
        # Save the reference to the list and reset the variable flag, begin, and
        # end index.
        elif is_variable:
            variable_references.append(variable_reference.VariableReference(current_string, begin_index, end_index))
            is_variable = False
            begin_index = i
            end_index = i
    # If we've enumerated through the whole string and the variable flag is on,
    # there's a variable that hasn't been added to the list, so add it.
    if is_variable:
        variable_references.append(variable_reference.VariableReference(current_string, begin_index, end_index))
    return variable_references

def derive_string(current_string, grammar):
    # While the string is not fully lower case(i.e. contains rules to be replaced
    # with productions):
    # 1. find variable references in the current string
    # 2. choose a random variable reference from the list of references
    # 3. choose a random production to expand from the corresponding variable's rules
    # 4. print logging message
    # 5. update the current string with the random production
    variable_references = []
    while not current_string.islower():
        variable_references = find_references(current_string)
        random_variable = random.choice(variable_references)
        random_production = random.choice(grammar.variable_dict[random_variable.name].rules)
        updated_string = current_string[:random_variable.start_index] + random_production + current_string[random_variable.end_index + 1:]
        if DEBUG == 1:
            print('In "{}" replacing "{}" with "{}" to obtain "{}"'.format(current_string, 
                                                                            random_variable.name,
                                                                            random_production,
                                                                            updated_string))
        current_string = updated_string
    return updated_string

def process_grammar(filename):
    input_file = open(filename,'r')
    variable_list = []
    current_variable = None
    total_rules = 0
    for line in input_file:
        if line.isspace():
            continue
        elif line[0] == '#':
            continue
        elif line[0] == '|':
            # Arrived at an alternative rule for a variable
            production = parse_alt_rule(line)
            current_variable.rules.append(production)
            total_rules += 1
        else:
            # Arrived at a new variable rule
            variable_name, production = parse_first_rule(line)
            current_variable = variable.Variable(variable_name)
            current_variable.rules.append(production)
            variable_list.append(current_variable)
            total_rules += 1
    input_file.close()

    # Instantiate our grammar with the list of variable objects
    the_grammar = grammar.Grammar(variable_list)
    start_string = the_grammar.start_variable.name

    # Seed the random generator and initialize an empty list of variable references
    random.seed()
    
    # Derive a random string from the grammar until all the variables are used
    final_string = derive_string(start_string, the_grammar)
    return final_string
