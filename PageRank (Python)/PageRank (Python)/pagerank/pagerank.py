import numpy as np
import numpy.linalg as la
from io import StringIO

import pandas as pd
from numpy.linalg import eig

# # # MATRIX FOR STAGE I and II
# Matrix L with missing values for links from F
L = np.array([
    [0, 1 / 2, 1 / 3, 0, 0, 0],
    [1 / 3, 0, 0, 0, 1 / 2, 0],
    [1 / 3, 1 / 2, 0, 1, 0, 1 / 2],
    [1 / 3, 0, 1 / 3, 0, 1 / 2, 1 / 2],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1 / 3, 0, 0, 0]
])

# # # MATRIX FOR STAGE III
# Matrix L2 with new website G which links only to itself
L2 = np.array([
    [0, 1 / 2, 1 / 3, 0, 0, 0, 0],
    [1 / 3, 0, 0, 0, 1 / 2, 0, 0],
    [1 / 3, 1 / 2, 0, 1, 0, 1 / 3, 0],
    [1 / 3, 0, 1 / 3, 0, 1 / 2, 1 / 3, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1 / 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1 / 3, 1]
])


def power_iteration(matrix, precision=0.01):
    limit = 1
    size_n = len(matrix)
    r_prev = 100 * np.ones(size_n) / size_n

    while limit >= precision:
        r_next = matrix @ r_prev
        limit = la.norm(r_prev - r_next)
        r_prev = r_next

    # for value in r_prev:
    #     print(f"{value:.3f}")
    # print()

    return r_prev


def pagerank(link_matrix, damping_param):
    size_n = link_matrix.shape[0]
    J = np.ones((size_n, size_n))

    M = link_matrix * damping_param + (1 - damping_param) / size_n * J

    return power_iteration(M)


def print_matrix(matrix):
    # Print the matrix L row-by-row
    s = StringIO()
    np.savetxt(s, matrix, fmt="%.3f")
    print(s.getvalue())


# # # STAGE V # # #
# Getting integer n specifying how many websites are in the network;
n = int(input())
# Getting n strings separated by spaces which are the names of the websites;
webs = input().split()

# Getting n by n matrix of floats representing a link matrix for the internet;
L5 = []
for i in range(int(n)):
    L5.append(list(float(x) for x in (input().split())))

# Getting a string which is a query for the search, a name of a website to look for.
goal = input()

pg_results = pagerank(np.array(L5), damping_param=0.5)

rank = pd.Series(dict(zip(webs, pg_results)))

rank_sorted = rank.sort_index(ascending=False).sort_values(ascending=False)

if goal in rank_sorted.keys():
    # Move target row to first element of list.
    idx = [goal] + [key for key in rank_sorted.index if key != goal]
    rank_sorted = rank_sorted[idx]


i = 0
for key, v in rank_sorted.items():
    if i >= 5:
        break
    print(key, end="\n")
    i += 1




# # # # STAGE IV # # #
#
#
# n, d = (float(x) for x in input().split())
# L4 = []
# for i in range(int(n)):
#     L4.append(list(float(x) for x in (input().split())))
#
# pagerank(np.array(L4), d)


# # # # STAGE III # # #
# d = 0.5
# n = len(L2)
# J = np.ones((7, 7))
# prec = 0.01
#
# M = L2 * d + (1 - d) / n * J
#
# print_matrix(L2)
# power_iteration(L2)
# power_iteration(M, 0.01)

# # # # STAGE II # # #
#
# # Setting up initial vector r0
# r = 100 * np.ones(6) / 6
#
# # # I
# # First iteration
# r = L @ r
#
# for value in r:
#     print(f"{value:.3f}")
#
# # # II
# # Next 10 iterations
# for i in range(10):
#     r = L @ r
#
# print()
# for value in r:
#     print(f"{value:.3f}")
#
# # # III
# limit = 1
# r_prev = r
# while limit > 0.01:
#     r_next = L @ r_prev
#     limit = la.norm(r_prev - r_next)
#     r_prev = r_next
#
#
# print()
# for value in r_prev:
#     print(f"{value:.3f}")


# # # STAGE I # # #
# # Calculate eigenvectors and eigenvalues
# e_vals, e_vecs = eig(L)

# # Extract the eigenvector corresponding to the eigenvalue 1
# vec = np.transpose(e_vecs)[0].real

# # Normalize the PageRank vector
# normalized_vec = vec * (100 / sum(vec))

# # Print the matrix L row-by-row
# s = StringIO()
# np.savetxt(s, L, fmt="%.3f")
# print(s.getvalue())

# # Print the normalized PageRank vector
# for value in normalized_vec:
#     print(f"{value:.3f}")
