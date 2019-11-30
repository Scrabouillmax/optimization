class DiscreteSolver:
    def __init__(self, domain):
        """
        :param domain: dictionary, keys: variable names, values: list representing the variable's domain.
        """
        self.domain = domain
        self.constraints = {}
        self.affectation = {}
        # used to save variables domains before reducing it when running the forward compatibility check.
        # domain_cache[var_name] is a dictionary containing the copy
        # of all variables for which the domain was changed by forward check
        # after assigning var_name to a value.
        self.domain_cache = {var_name: {} for var_name in domain.keys()}

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
        :return: the variable with the smallest domain not already assigned. None if all variables are assigned.
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
        :return: True if this value for var_name is compatible with already assigned variables.
        """
        for affected_var_name, affected_var_value in self.affectation.items():
            constraint_key = (var_name, affected_var_name)
            if constraint_key in self.constraints and not self.constraints[constraint_key](value, affected_var_value):
                return False
        return True

    def _forward_compatibility_check(self, affected_var_name, affected_var_value):
        """
        Reduces the domain of all the variables not yet assigned
        to satisfy all the constraints after affected_var_name affectation.
        :param affected_var_name: name of the variable assigned before this check.
        :param affected_var_value: value of the variable assigned before this check.
        :return: False if it is not possible to find a solution after this assignment
            (i.e. one of the non-assigned variable's domain is empty), True otherwise.
        """
        for var_name, var_domain in self.domain.items():
            if var_name not in self.affectation and (affected_var_name, var_name) in self.constraints:
                new_var_domain = [
                    value
                    for value in var_domain
                    if self.constraints[(affected_var_name, var_name)](affected_var_value, value)
                ]
                if len(new_var_domain) == 0:
                    # one of the non-assigned variable is no longer possible to assign
                    return False
                if len(new_var_domain) < len(var_domain):
                    self.domain_cache[affected_var_name][var_name] = var_domain
                    self.domain[var_name] = new_var_domain

        return True

    def _perform_compatibility_check(self, compatibility_check, var_name, value):
        """
        Assigns value to var_name if possible.
        :param compatibility_check: 'forward' or 'backward'
        :param var_name: name of the variable to assign.
        :param value: value of the variable to assign.
        :return: True if the variable has been assigned, False otherwise.
        """
        if compatibility_check == 'backward':
            if self._backward_compatibility_check(var_name, value):
                self.affectation[var_name] = value
                return True
            return False

        if self._forward_compatibility_check(var_name, value):
            self.affectation[var_name] = value
            return True
        return False

    def solve(self, compatibility_check='forward'):
        """
        :param compatibility_check: 'forward' or 'backward'
        :return: dict with keys variable names and values an affectation for each variables satisfying the constraint.
        """
        var_name = self._select_variable()

        if var_name is None:
            return self.affectation

        for possible_value in self.domain[var_name]:
            if self._perform_compatibility_check(compatibility_check, var_name, possible_value):
                solution = self.solve(compatibility_check=compatibility_check)

                if solution:
                    return solution

                del self.affectation[var_name]
                for cached_domain_var_name, cached_domain_value in self.domain_cache[var_name].items():
                    self.domain[cached_domain_var_name] = cached_domain_value
                self.domain_cache[var_name] = {}

