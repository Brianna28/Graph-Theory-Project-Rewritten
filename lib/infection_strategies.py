'''
Rewrite this section only using matrices ()
'''


from abc import ABC, abstractmethod
from lib.infection_class import infection_graph
import random as rand
import networkx as nx
import logging
from math import floor


def modifier(x: float) -> int:
    """Used for the skill check infection strategy

    Args:
        x (float): The infection rate

    Returns:
        int: An integer from -5 to +5
    """    
    mods = list(range(-5,6))
    index = floor(11*x)
    if index == 11:
        index -= 1
    return mods[index]    






class infection_strat(ABC): 
    """This is an abstract base class for the infection strategies, it sets the blueprint for what the infection strategies should look like
    They should have:
        An Infection method
        A __str__ method for a string representation of the strat
        An assumptions dunction that returns the assumptions the infection strategy makes
    """     
    @abstractmethod
    def infect(infclass: infection_graph, p: float) -> None:
        pass
    
    @abstractmethod
    def __str__():
        pass
    
    @abstractmethod
    def assumptions():
        pass

class ConstantRateInfection(infection_strat):
    """This is the main infection strategy basiing off a constant rate to infect each node
    """    
    def infect(infclass: infection_graph,p: float) -> None:
        """This method infects usinga constant rate to infect each node

        Args:
            infclass (infection_graph): The graph we are using in the model
            p (float): The constant rate of infection
        """        
        to_be_infected = []
        for i in infclass.infected: #this part gets all the neighburs of each infected node ready to then attempt to infect them
            k = infclass.get_neighbors(i)
            for n in k:
                to_be_infected.append(n)
        to_be_infected = [x for x in  to_be_infected if x not in infclass.infected] #We filter out any nodes that are already infected
        for node in to_be_infected:#for each node in the   to_be_infected list the rate of infection is p and will be added  to the infected class
            r_no = rand.random() #A random float from 0 to 1
            if infclass.timesrecovered[node] > 0: #if infclass.timesrecovered[node] is greater than 0 the node is immune so we ignore it
                pass
            elif node in infclass.infected:
                pass
            elif r_no < p: #if the R-no is less than p the node becomes infected 
                infclass.infected.add(node) #it is added to the infected set
                infclass.no_of_successful_infections += 1 #we have successfully infected so we add 1 to the number of successful infections
            else: #If the node isnt infected we ignore it
                pass
            
    def __str__() -> str:
        """Returns a string representation of the strategy"""
        return 'ConstantRate'
    
    def assumptions() -> list[str]:
        """Returns a list of assumptions about the strat"""
        return ['Rate of infection is constant\n']
    
    
"""Do the other strategies later"""    
class PersonalInfection(infection_strat):
    """In this strategy everyone has a personal infection rate, so we are techinally agnostic on how he infecctionous of the virus
    """    
    def infect(infclass: infection_graph, p: float) -> None:   
        to_be_infected = []
        for i in infclass.infected: #this part gets all the neighburs of each infected node ready to then attempt to infect them
            k = infclass.get_neighbors(i)
            for n in k:
                to_be_infected.append(n)
        for node in to_be_infected:#for each node in the   to_be_infected list the rate of infection is p and will be added  to the infected class
            personal_rate = infclass.PersonalInfection.get(node)
            r_no = rand.random()
            if infclass.timesrecovered[node] > 0:
                pass
            elif node in infclass.infected:
                pass
            elif r_no < personal_rate:
                infclass.infected.add(node)
                infclass.no_of_successful_infections += 1
                logging.debug(f"{node} was infected")
            else:
                pass
            
    def __str__():
        return 'PersonalRate'
    
class SkillCheckInfection(infection_strat):
    def infect(infclass: infection_graph,p:float) -> None:
        """_summary_

        Args:
            infclass (infection_graph): _description_
            p (float): _description_
        """        
        to_be_infected = []
        for i in infclass.infected: #this part gets all the neighburs of each infected node ready to then attempt to infect them
            k = nx.all_neighbors(infclass.graph, i)
            for n in k:
                to_be_infected.append(n)
        for node in to_be_infected:#for each node in the   to_be_infected list the rate of infection is p and will be added  to the infected class
            personal_rate = infclass.PersonalInfection.get(node)

            infection_roll = rand.randint(1,20) + modifier(p) 
            resist_roll = rand.randint(1,20) + modifier(personal_rate)
            success = infection_roll>resist_roll
            
            if infclass.timesrecovered[node] > 0:
                pass
            elif node in infclass.infected:
                pass
            elif success:
                infclass.infected.add(node)
                infclass.no_of_successful_infections += 1
                logging.debug(f"{node} was infected")
            else:
                pass
            
    def __str__():
        return 'SkillCheck'
