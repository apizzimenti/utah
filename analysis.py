
import networkx as nx
import matplotlib.pyplot as plt
import json

# Import the rook and queen adjacency graphs. Make sure that
# you have your rook adjacency graph saved as `rook.json` and
# queen adjacency as `queen.json` in the same directory as
# this script.
with open("./graphs/rook.json") as rf:
    rook = json.load(rf)

with open("./graphs/queen.json") as qf:
    queen = json.load(qf)

# Read graphs into networkx graph objects.
rook = nx.readwrite.json_graph.adjacency_graph(rook)
queen = nx.readwrite.json_graph.adjacency_graph(queen)

# Draw and save images of your dual graphs.
nx.draw(rook, node_size=1)
plt.savefig("./output/rook.png")

nx.draw(queen, node_size=1)
plt.savefig("./output/queen.png")

# Report edge sizes.
additional_edges = len(queen.edges) - len(rook.edges)

# Check to see if there are any edges in the rook that aren't in the queen. Also,
# I know this is pretty inefficient, but whatever.
redges = set(rook.edges)
qedges = set(queen.edges)
bad_edges = "No."

if not redges.issubset(qedges):
    bad_edges = "Yes."

# How many zero population vtds are there?
pop_dict = nx.get_node_attributes(rook, "POP10")
pop_list = list(pop_dict.values())
pop = pop_list.count(0)

# How many boundary districts?
bnd_dict = nx.get_node_attributes(rook, "boundary_node")
bnd_list = list(bnd_dict.values())
boundary = bnd_list.count(True)

# Write to a baby text file.
with open("./output/analysis.txt", "w") as af:
    lines = [
        f"{additional_edges} additional edges in queen adjacency graph.",
        f"Are there edges in the rook graph that aren't in the queen? {bad_edges}",
        f"{pop} 0-population VTDs and {boundary} boundary VTDs."
    ]

    for line in lines:
        af.write(line + "\n")

