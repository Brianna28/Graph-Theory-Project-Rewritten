import numpy as np
import networkx as nx
di= {0: 'blue', 1: 'blue', 2: 'blue', 3: 'blue', 4: 'blue', 5: 'blue', 6: 'blue', 7: 'blue', 8: 'blue', 9: 'blue', 10: 'blue', 11: 'blue', 12: 'blue', 13: 'blue', 14: 'blue', 15: 'blue', 16: 'blue', 17: 'blue', 18: 'blue', 19: 'blue', 20: 'blue', 21: 'blue', 22: 'red', 23: 'red', 24: 'blue'}
alive = [0,5,8]
doner = {}
for i in di:
    if i in alive:
        doner.update({i:di.get(i)})
print(doner)