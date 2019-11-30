class DiscreteSolver:
    def __init__(self, domain):
        """
        :param domain: dictionary, keys: variable names, values: list representing the variable's domain.
        """
        self.domain = domain
        self.constraints = {}
        self.affectation = {}

    def add_constraint(self, var1_name, var2_name, is_affectation_possible):
        """
        Add constraints for a couple of variables.
        :param var1_name: name of the variable 1 in the domain.
        :param var2_name: name of the variable 2 in the domain.
        :param is_affectation_possible: function(var1_affectation, var2_affectation) -> bool.
            returns True if the value passed are a possible affectation for var1 and var2, returns False otherwise.
        :return: None.
        """
        self.constraints[(var1_name, var2_name)] = is_affectation_possible
        self.constraints[(var2_name, var1_name)] = lambda var2, var1: is_affectation_possible(var1, var2)

    def _select_variable(self):
        """
        :return: the variable with the smallest domain not already affected. None if all variables are affected.
        """
        var_with_smallest_domain = None
        smallest_domain_size = float('Inf')

        for var_name, domain in self.domain.items():
            if len(domain) < smallest_domain_size and var_name not in self.affectation:
                var_with_smallest_domain = var_name
                smallest_domain_size = len(domain)

        return var_with_smallest_domain

    def _backward_compatibility_check(self, var_name, value):
        """
        :param var_name: name of the variable
        :param value: value for the variable.
        :return: True if this value for var_name is compatible with already affected variables.
        """
        for affected_var_name, affected_var_value in self.affectation.items():
            constraint_key = (var_name, affected_var_name)
            if constraint_key in self.constraints and not self.constraints[constraint_key](value, affected_var_value):
                return False
        return True

    def solve(self):
        """

        :return: dict with keys variable names and values an affectation for each variables satisfying the constraint.
        """
        var_name = self._select_variable()

        if var_name is None:
            return self.affectation

        for possible_value in self.domain[var_name]:
            if self._backward_compatibility_check(var_name, possible_value):
                self.affectation[var_name] = possible_value
                solution = self.solve()

                if solution:
                    return solution

                del self.affectation[var_name]




