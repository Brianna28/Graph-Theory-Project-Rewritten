import networkx as nx
import numpy as np
from betterdiameter import betterdiameter
import logging
import random as rand
from math import floor
from average_shortest_path import average_shortest_path_length
from clustering_coefficent import average_clustering_coefficient

"""
    TODO: Add clustering Coefficent (/)
    TODO: Add Aveerage Shortest Path Length (/)

"""


class infection_graph:
    """The infect graph class is the object that we will be using for a majority of the programs run time, it creates an object that holds data about the on goign infection"""

    def __init__(
        self,
        network: np.ndarray,
        initial_infected: int,
        intial_immune: int,
        enable_vis: bool,
    ):
        """__init__() is run when the object is first created, here we intialise all the values ou program will require

        Args:
            network (nx.Graph): This is the network the infection will be ran on
            initial_infected (int): This determines how many people will be infected on day 0 of the infection
            intial_immune (int): This determines how many people will be natrually immune to the infection from day 0
        """
        self.graph = network  # This is the network the infection is running on
        self.no_nodes = self.graph.shape[0]  # the total number of nodes in the network
        self.vertices = [
            x for x in range(self.no_nodes)
        ]  # this is a list of all the vertices in the network
        self.edges = np.sum(self.graph) // 2  # the number of edges in the network
        self.degrees = dict(
            zip(self.vertices, [i.sum() for i in self.graph])
        )  # returns a dictionary with the nodes as keys and their degree as value
        histo_maker = lambda lst: {item: lst.count(item) for item in lst}
        self.histogram = histo_maker(
            [i.sum() for i in self.graph]
        )  # Creates a dictionary where the degree is the key and the frequency of that degree is the value
        self.highestdegree = list(self.histogram)[
            -1
        ]  # Gives the last element of the histogram to give the highest degree
        self.average_degree = (
            sum([key * val for key, val in self.histogram.items()]) / self.no_nodes
        )  # we take all the values from the histogram dictionary, multiply the frequency by the degree then take the mean of that
        self.diameter = betterdiameter(self.graph)  # See betterdiameter documentation
        self.clustering = average_clustering_coefficient(
            self.graph
        )  # returns the average clustering coeffcient by calculating the local clustering coefficent for each node

        self.average_path_length = average_shortest_path_length(
            self.graph
        )  # This calulates the average shortest path length for the graph, if the graph is discconncted this will raise and exception
        if enable_vis:
            self.colours = self.colour()
            self.nxgraph = nx.from_numpy_array(self.graph)
            self.pos = nx.spring_layout(self.nxgraph)
        ########################################################################
        self.no_of_intitial_infected = initial_infected
        self.no_of_intitial_immune = intial_immune
        self.infected = (
            set()
        )  # We store each infected node here. We intialize self.infected as a set as in python a set can only have unique values so if node 3 was added twice then only one would be saved
        zeros = [0] * self.no_nodes  # a list of 0s for each node in the graph
        self.daysinfected = dict(
            zip(self.vertices, zeros)
        )  # A dictionary mapping each node to how long they have been infected
        self.timesrecovered = dict(
            zip(self.vertices, zeros)
        )  # A dictionary mapping each node to the number of times they recoverd (Currenly if the times recoverd is greater than 0 then the node is immune)
        self.no_of_successful_infections = (
            self.no_of_intitial_infected
        )  # the number of times the infection has infected another node
        #######################################################################
        for _ in range(
            intial_immune
        ):  # adds immune people equal to init_immune parameter
            self.init_immune()
        for _ in range(initial_infected):
            self.inital_infection()  # Picks a vertex at random to start the infection
        self.PersonalInfection = (
            self.PersonalInfectionRates()
        )  # Creates a personal infection rate for each node (only used for the PersonalInfection and SkillCheck infection strategies)

    #    ########################################################################
    def colour(self) -> dict:
        """Here we colour the nodes on whether theyre a hub or a super hub, here hubs are defined as node with a degree greater than the median degree,
        super hubs are defined as nodes with the highest degrees in the graph

        Returns:
            dict: Conatins each node and its corresponding colour
        """
        colours = dict()
        hubsize = floor(len(self.histogram) / 2)  # The median degree of the graph
        hub = list(self.histogram)[hubsize]  # uses the median to grab the hub nodes
        for key, val in self.degrees.items():
            if (
                val == self.highestdegree
            ):  # if the node is a super hub its coloured yellow
                colours.update({key: "red"})
            elif (
                hub < val < self.highestdegree
            ):  # if the node has degree is greater thena hub and less than the highest degree then its coloured green
                colours.update({key: "green"})
            else:
                colours.update({key: "blue"})
        return colours

    def get_neighbors(self, node: int) -> list[int]:
        logging.info(self.vertices)
        current_node_index = self.vertices.index(node)
        neighbors = np.nonzero(self.graph[current_node_index])[0]
        neighbors = [self.vertices[x] for x in neighbors]
        return neighbors

    def remove_node(self, node: int) -> None:
        location_for_rem = self.vertices.index(node)
        self.graph = np.delete(self.graph, (location_for_rem), axis=0)
        self.graph = np.delete(self.graph, (location_for_rem), axis=1)
        self.vertices.pop(location_for_rem)

    def init_immune(self) -> None:
        """Makes nodes immune from day 0"""
        r_number = np.random.randint(
            0, self.no_nodes
        )  # Pick a random integer between 0 and self.no nodes
        node = self.vertices[
            r_number
        ]  # using that random integer it selects the node from the graph
        if (
            self.timesrecovered[node] > 0
        ):  # if the node is already immune it runs the function gain to pick a different node
            self.init_immune()
        self.timesrecovered[
            node
        ] += 1  # Adds 1 to the timesrecoverd dictionary to make the node immune

    def inital_infection(self) -> None:
        """Infects the intial nodes at day 0"""
        r_number = np.random.randint(0, self.no_nodes)
        if (
            self.timesrecovered[r_number] > 0
        ):  # If the node is already immune it cant infect the node
            self.inital_infection()
        if (
            self.vertices[r_number] in self.infected
        ):  # if the node is already infected it selects another node
            self.inital_infection()
        self.infected.add(self.vertices[r_number])  # adds the node to self.infcected

    def stats(self) -> dict[str, float]:
        """This function gives information about the garphs structure

        Returns:
            dict: Contains the highest degree, diameter, average path length, avergae clustering, and the average degree
        """
        return {
            "highest_degree": self.highestdegree,
            "Diameter": self.diameter,
            "average_path_length": self.average_path_length,
            "average_clustering": self.clustering,
            "average_degree": self.average_degree,
        }

    def inf_stats(self) -> dict[str, int]:
        """This function returns information about the infection

        Returns:
            dict: Contains the number of intial infected, intial immune and the number of successful infections
        """
        return {
            "intital_number_of_infected": self.no_of_intitial_infected,
            "intital_number_of_immune": self.no_of_intitial_immune,
            "Successful_infections": self.no_of_successful_infections,
        }

    def die_or_recover(self, node, r: float) -> None:
        """This function handles nodes either dying or recovering depending on our model parameters
        They recover with probability r and die with probability 1-r

        Args:
            node (node): The node that is going to recover or die
            r (float): The recovery rate as set by the model
        """
        r_no = rand.random()  # chooses a random float from 0 to 1
        if r_no < r:
            """if the node recovers, it is removed from the infected set, has its time spent infected set to 0 and has its times recovered increased to 1 (making the node immune)"""
            self.infected.discard(node)
            self.daysinfected.update({node: 0})
            self.timesrecovered[node] += 1
            logging.debug(f"{node} has recovered")
        else:
            """however if it fails the node is killed, being removed from the infected set, removed from the graph, has its time infected
            put to 0 and is removed from the colours list to make sure the plot later doesnt attempt to colour a node
            that doesnt exist"""
            self.infected.discard(node)
            self.remove_node(node)
            self.daysinfected.update({node: 0})
            logging.debug(f"{node} has died")

    def PersonalInfectionRates(self) -> dict[int, float]:
        """Creates all the personal infection rates for the nodes

        Returns:
            dict: Contains each node and its personal infection rate pulled from a uniform  distribution
        """
        samples = [rand.random() for _ in range(self.no_nodes)]
        personal_infections = dict(zip(self.vertices, samples))
        return personal_infections

    def update_picture(self):
        self.colours = {
            i: self.colours.get(i) for i in self.colours if i in self.vertices
        }
        self.nxgraph = nx.from_numpy_array(self.graph)
        self.pos = nx.spring_layout(
            self.nxgraph
        )  # This sets a standard layout for when we output images of the graph


if __name__ == "__main__":
    h = 0
