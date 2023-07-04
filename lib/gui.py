'''
Rewrite this section only using matrices ()
'''


import networkx as nx
from math import comb
from lib.infection_strategies import ConstantRateInfection, PersonalInfection, SkillCheckInfection
import logging

try:
    import PySimpleGUI as sg
    NOGUI = False
except ImportError:
    print('PySimpleGUI is not available, please try installing PySimpleGUI')
    NOGUI = True
    sg = None




class graph_constructer:
    """_summary_
    """    
    def barabasi(init_graph: nx.Graph, no_nodes: int, edges: int) -> nx.Graph:
        """_summary_

        Args:
            init_graph (nx.Graph): _description_
            no_nodes (int): _description_
            edges (int): _description_

        Returns:
            nx.Graph: _description_
        """        
        try:
            return nx.barabasi_albert_graph(no_nodes,edges,initial_graph = init_graph)
        except nx.exception.NetworkXError:
            print(f'Number of edges must be less that number of nodes, {edges}>{no_nodes}')
            userpanel()
        
    def random_graph(no_nodes: int, Eedges: int) -> nx.Graph:
        p = Eedges/comb(no_nodes,2)
        try:
            return nx.erdos_renyi_graph(no_nodes,p)
        except nx.exception.NetworkXErrror:
            userpanel()
            
    def watts(n:int, k:int,p: float)-> nx.Graph:
        try:
            return nx.watts_strogatz_graph(n,k,p)
        except nx.exception.NetworkXErrror:
            userpanel()
        
    def scale_free(n: int,a: float,b: float,c: float) -> nx.Graph:
        try:
            nx.scale_free_graph(n,a,b,c)
        except nx.exception.NetworkXErrror:
            userpanel()

def graphchoice(m:int,choice: str) -> nx.Graph:
    """_summary_

    Args:
        m (int): _description_
        choice (str): _description_

    Returns:
        nx.Graph: _description_
    """    
    
    
    '''Here we choose which graph we will be using a barabasi transform on'''   

    if choice == 'Wheel':
        return nx.wheel_graph(m+1)
    elif choice == 'Cycle' :
        return nx.cycle_graph(m+1)
    elif choice == 'Complete':
        return nx.complete_graph(m+1)
    elif choice == 'Star':
        return nx.star_graph(m+1)
    elif choice == 'Erdos-Renyi':
        return nx.erdos_renyi_graph(m+1,0.5)

class Panel:
    """_summary_

    Returns:
        _type_: _description_
    """    
    def __init__(self):
        self.LIST_OF_INFECTION_MODELS = {'ConstantRate':ConstantRateInfection,'Personal':PersonalInfection,'SkillCheck':SkillCheckInfection}
        
    def barabasi(self) -> tuple:
        """_summary_

        Returns:
            tuple: _description_
        """        
        graph_type = 'Barabasi'
        sg.theme('Green')
        LIST_OF_GRAPHS = ('Wheel','Cycle','Complete','Star','Erdos-Renyi')
        layout = [[sg.Text('No of nodes')],
                  [sg.InputText()],
                  [sg.Text('Barabasi Edges')],
                  [sg.InputText()],
                  [sg.Text('Choice of seed graph:')],
                  [sg.Listbox(values=LIST_OF_GRAPHS,size=(15,5), key='Graph_Type', enable_events=True)],
                  [sg.Checkbox('Enable Graphs?',default = True, key= 'Enable_Vis' )],
                  [sg.Submit()],
                  [sg.Cancel()]]
        window = sg.Window('SIRD Infection Model', layout)
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                quit()
            elif 'Submit' in event:
                break      
        window.close()
        if values['Enable_Vis'] is  True:
            enable_vis = True
        else:
            enable_vis = False
        try:
            n,e= values[0],values[1]
            n,e= int(n),int(e)
        except ValueError:
            print('Please input the correct data types')
            self.barabasi()
         #n,e,p_i,p_r = input('Number of Nodes:'),input('Barabasi edges to add:'),input('Probaility of infection:'),input('Probability to Recover:')
         #enable_vis = input('Show Graphs?:')
        graph = graphchoice(e,values['Graph_Type'][0])
        user_graph = graph_constructer.barabasi(graph,n,e)
        return (user_graph,enable_vis,graph_type)

    def watts_strogatz(self) -> tuple:
        graph_type = 'Watts-Strogatz'
        sg.theme('Green')
        layout = [[sg.Text('No of nodes')],
                  [sg.InputText()],
                  [sg.Text('k:')],
                  [sg.InputText()],
                  [sg.Text('p:')],
                  [sg.InputText()],
                  [sg.Checkbox('Enable Graphs?',default = True, key= 'Enable_Vis' )],
                  [sg.Submit()],
                  [sg.Cancel()]]
        window = sg.Window('SIRD Infection Model', layout)
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                quit()
            elif 'Submit' in event:
                break      
        window.close()
        if values['Enable_Vis'] is  True:
            enable_vis = True
        else:
            enable_vis = False
        try:
            n,k,p = values[0],values[1],values[2]
            n,k,p = int(n),int(k),float(p)
        except ValueError:
            print('Please input the correct data types')
            self.watts_strogatz()

        user_graph = graph_constructer.watts(n,k,p)
        return (user_graph,enable_vis,graph_type)

    def scale_free(self):
        graph_type = 'Scale-Free'
        sg.theme('Green')
        layout = [[sg.Text('No of nodes (int)')],
                  [sg.InputText()],
                  [sg.Text('alpha (float)')],
                  [sg.InputText()],
                  [sg.Text('beta (float)')],
                  [sg.InputText()],
                  [sg.Text('gamma (float)')],
                  [sg.InputText()],
                  [sg.Checkbox('Enable Graphs?',default = True, key= 'Enable_Vis' )],
                  [sg.Submit()],
                  [sg.Cancel()]]
        window = sg.Window('SIRD Infection Model', layout)
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                quit()
            elif 'Submit' in event:
                break      
        window.close()
        if values['Enable_Vis'] is  True:
            enable_vis = True
        else:
            enable_vis = False
        try:
            n,a,b,c = values[0],values[1],values[2],values[3]
            n,a,b,c = int(n),float(a),float(b),float(c)
        except ValueError:
            print('Please input the correct data types')
            self.scale_free()
        user_graph = graph_constructer.scale_free(n,a,b,c)
        return (user_graph,enable_vis,graph_type)
    
    def erdos_renyi(self):
        graph_type = 'Erdos-Renyi'
        sg.theme('Green')
        layout = [[sg.Text('No of nodes (int)')],
                  [sg.InputText()],
                  [sg.Text('Expected No of edges')],
                  [sg.InputText()],
                  [sg.Checkbox('Enable Graphs?',default = True, key= 'Enable_Vis' )],
                  [sg.Submit()],
                  [sg.Cancel()]]
        window = sg.Window('SIRD Infection Model', layout)
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                quit()
            elif 'Submit' in event:
                break      
        window.close()
        if values['Enable_Vis'] is  True:
            enable_vis = True
        else:
            enable_vis = False
        try:
            n,e = values[0],values[1]
            n,e= int(n),float(e)
        except ValueError:
            print('Please input the correct data types')
            self.erdos_renyi()
        user_graph = graph_constructer.random_graph(n,e)
        return (user_graph,enable_vis,graph_type)
    
    def infect_panel(self):
        sg.theme('Green')
        layout = [[sg.Text('P of infection')],
                  [sg.InputText()],
                  [sg.Text('P of Recovery')],
                  [sg.InputText()],
                  [sg.Text('Number of Intial Infected')],
                  [sg.InputText()],
                  [sg.Text('Number of Intial Immune')],
                  [sg.InputText()],
                  [sg.Listbox(values=list(self.LIST_OF_INFECTION_MODELS.keys()),size=(15,5),key='Infection',enable_events=True)],
                  [sg.Submit()],
                  [sg.Cancel()]]
        window = sg.Window('SIRD Infection Model', layout)
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                quit()
            elif 'Submit' in event:
                break      
        window.close()
        try:
            p_i,p_r,init_infected,init_immune = float(values[0]),float(values[1]),int(values[2]),int(values[3])
        except ValueError:
            print('Pleaae use the coreect data types')
            self.infect_panel()
        infection_type_key = values['Infection'][0]
        infection_type = self.LIST_OF_INFECTION_MODELS[infection_type_key]
        return (p_i,p_r,init_infected,init_immune,infection_type)
    
def userpanel() -> tuple:
    """_summary_

    Returns:
        tuple: _description_
    """    
    sg.theme('Green')
    panel = Panel()
    LIST_OF_GRAPH_TYPES = {'Barabasi-Albert':panel.barabasi,'Watts-Strogats':panel.watts_strogatz,'Erdos Random':panel.erdos_renyi,'Scale Free':panel.scale_free}
    layout = [[sg.Text('Which type of graph would you like to test?')],
              [sg.Listbox(values=list(LIST_OF_GRAPH_TYPES.keys()),size=(20,10), key='-LIST-', enable_events=True)],
              [sg.Submit()],
              [sg.Cancel()]
              ]
    window = sg.Window('SIRD Infection Model', layout)
    while True:

            event, values = window.read()
            logging.debug(event)
            if event in (sg.WIN_CLOSED, 'Exit'):
                quit()
            elif 'Submit' in event:
                break
    window.close()
    try:
        graph_type = values['-LIST-'][0]
    except IndexError:
        userpanel()
    
    graph_params = LIST_OF_GRAPH_TYPES[graph_type]()
    infect_params = panel.infect_panel()
    #(p_i,p_r,init_infected,init_immune,infection_type)
    #(user_graph,enable_vis,graph_type)
    #(graph: nx.Graph,p_i: float, p_r: float,intial_infected: int = 1,intial_immune: int = 0,enable_vis: bool = False,infection_type: infection_strat = ConstantRateInfection,graph_type: str = 'Not Defined')
    parameters = (graph_params[0],infect_params[0],infect_params[1],infect_params[2],infect_params[3],graph_params[1],infect_params[4],graph_params[2])
    return parameters
    
def output_window(results):
    infect_info, orginstats = results
    infect_info = list(infect_info.items())
    orginstats = list(orginstats.items())
    layout_origin = [[x[0],x[1]] for x in orginstats]
    lay_origin = [[sg.Text(f'{x[0]}:{x[1]}')] for x in layout_origin]
    layout_infect = [[x[0],x[1]] for x in infect_info]
    lay_infect = [[sg.Text(f'{x[0]}:{x[1]}')] for x in layout_infect]
    sg.theme('Green')
    layout = [lay_origin, lay_infect]
    window = sg.Window('Output', layout)
    while True:

        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            quit()
        elif 'Submit' in event:
            break
    window.close()