from vocabulary import dico, genre
from DiscreteSolver import DiscreteSolver

n_lines = 2
word_types = ["Adjectif", "Verbe", "Nom commun"]

domain = {}
for word_type in word_types:
    domain_for_type = {(line, word_type): dico[word_type] for line in range(n_lines)}
    domain = {**domain, **domain_for_type}


def adjective_noun_gender_constraint(word1, word2):
    if word1 not in genre or word2 not in genre:
        # one of the word is neutral
        return True
    return genre[word1] == genre[word2]


def word_difference_constraint(word1, word2):
    return word1 != word2


def adjective_same_last_letter_constraint(word1, word2):
    return word1[-1] == word2[-1]


def create_solver_with_constraints():
    return DiscreteSolver(domain)\
        .add_constraint((0, "Adjectif"), (0, "Nom commun"), adjective_noun_gender_constraint)\
        .add_constraint((1, "Adjectif"), (1, "Nom commun"), adjective_noun_gender_constraint)\
        \
        .add_constraint((0, "Verbe"), (1, "Verbe"), word_difference_constraint)\
        .add_constraint((0, "Nom commun"), (1, "Nom commun"), word_difference_constraint)\
        .add_constraint((0, "Adjectif"), (1, "Adjectif"), word_difference_constraint)\
        \
        .add_constraint((0, "Adjectif"), (1, "Adjectif"), adjective_same_last_letter_constraint)


def display_solution(solution):
    print("%s %s %s," % (solution[(0, "Verbe")], solution[(0, "Nom commun")], solution[(0, "Adjectif")]))
    print("%s %s %s." % (solution[(1, "Verbe")], solution[(1, "Nom commun")], solution[(1, "Adjectif")]))
    print('---')


for i in range(5):
    solver = create_solver_with_constraints()
    display_solution(solver.solve(variable_selection='random'))
