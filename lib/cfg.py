class Grammar:
    """A class that represents the grammar of a context free grammar. It holds
    dictionary that maps each variable name to a corresponding variable object. 
    The _start_variable instance variable holds a pointer to the 
    grammar's start variable object."""

    __slots__ = {'_variable_dict', '_start_variable'}

    def __init__(self, variable_list):
        self._variable_dict = {variable.name: variable for variable in variable_list}
        self._start_variable = self._find_start()

    def _find_start(self):
        """Finds the designated start variable and saves a pointer to it."""
        return self.variable_dict['START']

    @property
    def variable_dict(self):
        """I'm the 'variable_dict' property"""
        return self._variable_dict
    @variable_dict.setter
    def variable_dict(self, variable_dict):
        self._variable_dict = variable_dict

    @property
    def start_variable(self):
        """I'm the 'start_variable' property"""
        return self._start_variable
    @start_variable.setter
    def start_variable(self, start_variable):
        self._start_variable = start_variable

class Variable:
    """A class that represents a variable inside a context free grammar.
    The variable has a name and a list of rules that contain possible 
    productions."""
    __slots__ = {'_name', '_rules'}
    def __init__(self, name):
        self._name = name
        self._rules = []

    def __str__(self):
        return 'name: {}\nrules: {}'.format(self._name, self._rules)

    @property
    def name(self):
        """I'm the 'name' property"""
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def rules(self):
        """I'm the 'rules' property"""
        return self._rules
    @rules.setter
    def rules(self, rules):
        self._rules = rules

class VariableReference:
    """This class represents the occurence of a variable in the current
    string. It holds a pointer to the current string, a start index, end index,
    and name of the variable."""
    
    __slots__ = {'_current_string', '_start_index', '_end_index', '_name'}

    def __init__(self, current_string, start_index, end_index):
        self._current_string = current_string
        self._start_index = start_index
        self._end_index = end_index
        self._name = self._current_string[start_index:end_index + 1]

    def __str__(self):
        return 'curr_str: {}\nstart: {}\nend: {}\nname: {}'.format(self._current_string,
                                                                   self._start_index,
                                                                   self._end_index,
                                                                   self._name)

    @property
    def current_string(self):
        """I'm the 'current_string' property"""
        return self._current_string
    @current_string.setter
    def current_string(self, a_string):
        self._current_string = a_string

    @property
    def start_index(self):
        """I'm the 'start_index' property"""
        return self._start_index
    @start_index.setter
    def start_index(self, index):
        self._start_index = index

    @property
    def end_index(self):
        """I'm the 'end_index' property"""
        return self._end_index
    @end_index.setter
    def end_index(self, index):
        self._end_index = index

    @property
    def name(self):
        """I'm the 'name' property"""
        return self._name
