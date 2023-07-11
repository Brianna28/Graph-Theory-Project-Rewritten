
import networkx as nx
from math import comb
from .infection_strategies import ConstantRateInfection, PersonalInfection, SkillCheckInfection
from .matrix_graph_drawer import graph_drawer
import logging
import numpy as np




class graph_constructer:
    """_summary_
    """    
    def barabasi(init_graph: np.ndarray, no_nodes: int, edges: int) -> np.ndarray:
        """_summary_

        Args:
            init_graph (np.ndarray): _description_
            no_nodes (int): _description_
            edges (int): _description_

        Returns:
            np.ndarray: _description_
        """        
        try:
            return graph_drawer.generate_barabasi_albert_graph(no_nodes,edges,init_graph)
        except Exception:
            print(f'Number of edges must be less that number of nodes, {edges}>{no_nodes}')
            userpanel()
        
    def random_graph(no_nodes: int, Eedges: int) -> np.ndarray:
        p = Eedges/comb(no_nodes,2)
        try:
            return graph_drawer.generate_random_graph(no_nodes,p)
        except Exception:
            userpanel()
            
    def watts(n:int, k:int,p: float)-> np.ndarray:
        try:
            return nx.watts_strogatz_graph(n,k,p)
        except Exception:
            userpanel()
        
    def scale_free(n: int,a: float,b: float,c: float) -> np.ndarray:
        try:
            nx.scale_free_graph(n,a,b,c)
        except Exception:
            userpanel()

def graphchoice(m:int,choice: str) -> np.ndarray:
    """_summary_

    Args:
        m (int): _description_
        choice (str): _description_

    Returns:
        np.ndarray: _description_
    """    
    
    
    '''Here we choose which graph we will be using a barabasi transform on'''   

    if choice == 'Wheel':
        return graph_drawer.generate_wheel_graph(m+1)
    elif choice == 'Cycle' :
        return graph_drawer.generate_cycle_graph(m+1)
    elif choice == 'Complete':
        return graph_drawer.generate_complete_graph(m+1)
    elif choice == 'Star':
        return graph_drawer.generate_star_graph(m+1)
    elif choice == 'Erdos-Renyi':
        return graph_drawer.generate_random_graph(m+1,0.5)


class Panel:
    def __init__(self):
        self.LIST_OF_INFECTION_MODELS = {'ConstantRate': ConstantRateInfection, 'Personal': PersonalInfection, 'SkillCheck': SkillCheckInfection}
        
    def barabasi(self) -> tuple:
        graph_choices = ['Wheel','Cycle','Complete','Star','Erdos-Renyi']
        graph_type = 'Barabasi'
        n = input('No of nodes: ')
        e = input('Barabasi Edges: ')
        choice = input('Which type of graph would you like to test? ' + ', '.join(graph_choices) + ': ')
        graph = graphchoice(int(e),choice)
        enable_vis = input('Enable Graphs? (y/n): ').lower() == 'y'
        user_graph = graph_constructer.barabasi(graph, int(n), int(e))
        return (user_graph, enable_vis, graph_type)

    def watts_strogatz(self) -> tuple:
        graph_type = 'Watts-Strogatz'
        n = input('No of nodes: ')
        k = input('k: ')
        p = input('p: ')
        enable_vis = input('Enable Graphs? (y/n): ').lower() == 'y'
        user_graph = graph_constructer.watts(int(n), int(k), float(p))
        return (user_graph, enable_vis, graph_type)

    def scale_free(self):
        graph_type = 'Scale-Free'
        n = input('No of nodes: ')
        alpha = input('alpha: ')
        beta = input('beta: ')
        gamma = input('gamma: ')
        enable_vis = input('Enable Graphs? (y/n): ').lower() == 'y'
        user_graph = graph_constructer.scale_free(int(n), float(alpha), float(beta), float(gamma))
        return (user_graph, enable_vis, graph_type)

    def erdos_renyi(self):
        graph_type = 'Erdos-Renyi'
        n = input('No of nodes: ')
        e = input('Expected No of edges: ')
        enable_vis = input('Enable Graphs? (y/n): ').lower() == 'y'
        user_graph = graph_constructer.random_graph(int(n), float(e))
        return (user_graph, enable_vis, graph_type)

    def infect_panel(self):
        p_i = input('P of infection: ')
        p_r = input('P of Recovery: ')
        init_infected = input('Number of Initial Infected: ')
        init_immune = input('Number of Initial Immune: ')
        infection_type_key = input('Choose Infection Type: ' + ', '.join(self.LIST_OF_INFECTION_MODELS.keys()) + ': ')
        infection_type = self.LIST_OF_INFECTION_MODELS.get(infection_type_key)
        return (float(p_i), float(p_r), int(init_infected), int(init_immune), infection_type)
    

def userpanel() -> tuple:
    panel = Panel()
    LIST_OF_GRAPH_TYPES = {'Barabasi-Albert': panel.barabasi, 'Watts-Strogats': panel.watts_strogatz, 'Erdos Random': panel.erdos_renyi, 'Scale Free': panel.scale_free}
    graph_type = input('Which type of graph would you like to test? ' + ', '.join(LIST_OF_GRAPH_TYPES.keys()) + ': ')
    if graph_type not in LIST_OF_GRAPH_TYPES:
        return userpanel()
    graph_params = LIST_OF_GRAPH_TYPES[graph_type]()
    infect_params = panel.infect_panel()
    parameters = (graph_params[0], infect_params[0], infect_params[1], infect_params[2], infect_params[3], graph_params[1], infect_params[4], graph_params[2])
    return parameters

def output_window(results):
    infect_info, orginstats = results
    infect_info = list(infect_info.items())
    orginstats = list(orginstats.items())

    for item in orginstats:
        print(f"{item[0]}: {item[1]}")

    for item in infect_info:
        print(f"{item[0]}: {item[1]}")
