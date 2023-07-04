import cProfile
import pstats
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from sirdmodel import model
from lib.matrix_graph_drawer import generate_random_graph
def perf():
    G = generate_random_graph(2000,0.2)
    with cProfile.Profile() as pr:
                model(G,0.6,0.3)
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename='profile.prof')


if __name__ == '__main__':
    perf()