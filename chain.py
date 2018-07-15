
import geopandas as gpd
import networkx as nx
import functools
import matplotlib.pyplot as plt
import sys

from rundmcmc.validity import (Validator, no_vanishing_districts,
                               refuse_new_splits, single_flip_contiguous, L1_reciprocal_polsby_popper)
from rundmcmc.proposals import propose_random_flip
from rundmcmc.make_graph import construct_graph, add_data_to_graph
from rundmcmc.accept import always_accept
from rundmcmc.partition import Partition
from rundmcmc.updaters import *
from rundmcmc.chain import MarkovChain
from rundmcmc.defaults import BasicChain
from rundmcmc.run import pipe_to_table
from rundmcmc.scores import efficiency_gap, mean_median, mean_thirdian


def main():
    # Get the data, set the number of steps, and denote the column header
    # containing vote data.
    datapath = "./Prorated/Prorated.shp"
    graphpath = "./graphs/utah.json"
    steps = int(sys.argv[-1])
    r_header = "R"
    d_header = "D"

    # Generate a dataframe, graph, and then combine the two.
    df = gpd.read_file(datapath)
    graph = construct_graph(graphpath)
    add_data_to_graph(df, graph, [r_header, d_header], id_col="GEOID10")

    # Get the discrict assignment and add updaters.
    assignment = dict(zip(graph.nodes(), [graph.node[x]["CD"] for x in graph.nodes()]))
    updaters = {
        **votes_updaters([r_header, d_header]),
        "population": Tally("POP10", alias="population"),
        "perimeters": perimeters,
        "exterior_boundaries": exterior_boundaries,
        "interior_boundaries": interior_boundaries,
        "boundary_nodes": boundary_nodes,
        "cut_edges": cut_edges,
        "areas": Tally("ALAND10", alias="areas"),
        "polsby_popper": polsby_popper,
        "cut_edges_by_part": cut_edges_by_part
    }
    
    # Create an initial partition and a Pennsylvania-esque chain run.
    initial_partition = Partition(graph, assignment, updaters)
    validator = Validator([refuse_new_splits, no_vanishing_districts, single_flip_contiguous])
    chain = MarkovChain(
        propose_random_flip,
        validator,
        always_accept,
        initial_partition,
        total_steps=steps)

    # Pick the scores we want to track.
    scores = {
        "Mean-Median": functools.partial(mean_median, proportion_column_name=r_header + "%"),
        "Mean-Thirdian": functools.partial(mean_thirdian, proportion_column_name=d_header + "%"),
        "Efficiency Gap": functools.partial(efficiency_gap, col1=r_header, col2=d_header),
        "L1 Reciprocal Polsby-Popper": L1_reciprocal_polsby_popper
    }

    # Set initial scores, then allow piping and plotting things.
    initial_scores = {key: score(initial_partition) for key, score in scores.items()}
    table = pipe_to_table(chain, scores)
    fig, axes = plt.subplots(2, 2)

    # Configuring where the plots go.
    quadrants = {
        "Mean-Median": (0, 0),
        "Mean-Thirdian": (0, 1),
        "Efficiency Gap": (1, 0),
        "L1 Reciprocal Polsby-Popper": (1, 1)
    }

    # Plotting things!
    for key in scores:
        quadrant = quadrants[key]
        axes[quadrant].hist(table[key], bins=50)
        axes[quadrant].set_title(key)
        axes[quadrant].axvline(x=initial_scores[key], color="r")
        
    # Show the histogram.
    plt.savefig(f"./output/histograms/{steps}.png")
    

if __name__ == "__main__":
    main()
