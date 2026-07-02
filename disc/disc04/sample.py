def square_elements(l):

    return [x*x for row in l for x in row]


def vowel_remover(l):
    return [x for word in l for x in word if x not in ['a','e','i','o','u','y']]


def neg_index(l):
    return [(i, j, l[i][j])for i in range(len(l)) for j in range(len(l[i])) if l[i][j] < 0]
