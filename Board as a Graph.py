import networkx as nx
import matplotlib.pyplot as plt

board = nx.Graph()

board.add_edges_from([(1, 2), (2, 3)])

nx.draw(board, with_labels=True)
plt.show()
