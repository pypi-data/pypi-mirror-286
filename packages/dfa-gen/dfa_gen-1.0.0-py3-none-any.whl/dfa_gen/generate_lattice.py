from collections import defaultdict
from dfa_gen.dfa_class import NodeType, Lattice
from dfa_gen.dfa_util import get_ACGU_num
import math

### Lattice construction -------------------------------------------------------
def prepare_codon_unit_lattice(wheel_path, codon, lambda_=1.0):
    '''
    Step 1: Read initial weights
    Step 2: Update best weights
    Step 3: Read log weights
    '''
    nodes_with_best_weight = defaultdict(lambda: defaultdict(float))
    edges_with_best_weight = defaultdict(lambda: defaultdict(float))
    
    aa_graphs_with_weights = read_wheel_with_weights(wheel_path, nodes_with_best_weight, edges_with_best_weight, codon)
    update_best_weights(aa_graphs_with_weights, nodes_with_best_weight, edges_with_best_weight)
    aa_graphs_with_ln_weights = read_wheel_with_weights_log(wheel_path, nodes_with_best_weight, edges_with_best_weight, codon, lambda_)

    return aa_graphs_with_ln_weights

def read_wheel_with_weights(filename, nodes_with_best_weight, edges_with_best_weight, codon):
    aa_graphs = {}

    with open(filename) as inFile:
        for line in inFile:
            stuff = line.strip().split('\t')
            aa = stuff[0]
            graph = Lattice()
            graph.add_node(NodeType(0, 0))

            last_first = ''
            i = 0
            for option in stuff[1:]:
                option_splited = option.split(' ')
                first = option_splited[0]
                second = option_splited[1]
                thirds = option_splited[2]
                n2 = NodeType(2, i)
                graph.add_node(n2)
                if first != last_first:
                    n1 = NodeType(1, i)
                    graph.add_node(n1)
                    first_num = get_ACGU_num(first)
                    weight = 0.0
                    if NodeType(0, 0) in nodes_with_best_weight.get(aa, {}):
                        weight = edges_with_best_weight[aa][(NodeType(0, 0), first_num, n1)] / nodes_with_best_weight[aa][NodeType(0, 0)]
                    graph.add_edge(NodeType(0, 0), n1, first_num, weight)
                else:
                    n1 = NodeType(1, i-1)

                last_first = first
                second_num = get_ACGU_num(second)
                weight = 0.0

                if n1 in nodes_with_best_weight.get(aa, {}):
                    weight = edges_with_best_weight[aa][(n1, second_num, n2)] / nodes_with_best_weight[aa][n1]
                graph.add_edge(n1, n2, second_num, weight)

                for third in thirds:
                    three_nums = first + second + third
                    weight = 0.0
                    if n2 in nodes_with_best_weight.get(aa, {}):
                        weight = codon.get_weight(aa, three_nums) / nodes_with_best_weight[aa][n2]
                    else:
                        weight = codon.get_weight(aa, three_nums)
                    graph.add_edge(n2, NodeType(0, 0), get_ACGU_num(third), weight)

                i += 1
            aa_graphs[aa] = graph

    return aa_graphs

def update_best_weights(aa_graphs_with_weights, nodes_with_best_weight, edges_with_best_weight):
    for aa, graph in aa_graphs_with_weights.items():
        for node_at_2 in graph.nodes[2]:
            for node_at_3_nuc_weight in graph.right_edges[node_at_2]:
                node_at_3 = node_at_3_nuc_weight.node
                nuc = node_at_3_nuc_weight.nuc
                weight = node_at_3_nuc_weight.weight
                nodes_with_best_weight[aa][node_at_2] = max(nodes_with_best_weight[aa][node_at_2], weight)
                edges_with_best_weight[aa][(node_at_2, nuc, node_at_3)] = weight

        for node_at_1 in graph.nodes[1]:
            for node_at_2_nuc_weight in graph.right_edges[node_at_1]:
                node_at_2 = node_at_2_nuc_weight.node
                nuc = node_at_2_nuc_weight.nuc
                nodes_with_best_weight[aa][node_at_1] = max(nodes_with_best_weight[aa][node_at_1], nodes_with_best_weight[aa][node_at_2])
                edges_with_best_weight[aa][(node_at_1, nuc, node_at_2)] = nodes_with_best_weight[aa][node_at_2]

        for node_at_0 in graph.nodes[0]:
            for node_at_1_nuc_weight in graph.right_edges[node_at_0]:
                node_at_1 = node_at_1_nuc_weight.node
                nuc = node_at_1_nuc_weight.nuc
                nodes_with_best_weight[aa][node_at_0] = max(nodes_with_best_weight[aa][node_at_0], nodes_with_best_weight[aa][node_at_1])
                edges_with_best_weight[aa][(node_at_0, nuc, node_at_1)] = nodes_with_best_weight[aa][node_at_1]


def read_wheel_with_weights_log(filename, nodes_with_best_weight, edges_with_best_weight, codon, lambda_):
    aa_graphs = {}

    with open(filename) as inFile:
        for line in inFile:
            stuff = line.strip().split('\t')
            aa = stuff[0]
            graph = Lattice()
            graph.add_node(NodeType(0, 0))

            last_first = ''
            i = 0
            for option in stuff[1:]:
                option_splited = option.split(' ')
                first = option_splited[0]
                second = option_splited[1]
                thirds = option_splited[2]
                n2 = NodeType(2, i)
                graph.add_node(n2)
                if first != last_first:
                    n1 = NodeType(1, i)
                    graph.add_node(n1)
                    first_num = get_ACGU_num(first)
                    weight = 1.0
                    if NodeType(0, 0) in nodes_with_best_weight.get(aa, {}):
                        weight = lambda_ * math.log(edges_with_best_weight[aa][(NodeType(0, 0), first_num, n1)] / nodes_with_best_weight[aa][NodeType(0, 0)])
                    graph.add_edge(NodeType(0, 0), n1, first_num, weight)
                else:
                    n1 = NodeType(1, i-1)

                last_first = first
                second_num = get_ACGU_num(second)
                weight = 1.0
                if n1 in nodes_with_best_weight.get(aa, {}):
                    weight = lambda_ * math.log(edges_with_best_weight[aa][(n1, second_num, n2)] / nodes_with_best_weight[aa][n1])
                graph.add_edge(n1, n2, second_num, weight)

                for third in thirds:
                    three_nums = first + second + third
                    weight = 1.0
                    if n2 in nodes_with_best_weight.get(aa, {}):
                        weight = lambda_ * math.log(codon.get_weight(aa, three_nums) / nodes_with_best_weight[aa][n2])
                    else:
                        weight = lambda_ * math.log(codon.get_weight(aa, three_nums))
                    graph.add_edge(n2, NodeType(0, 0), get_ACGU_num(third), weight)

                i += 1
            aa_graphs[aa] = graph

    return aa_graphs

### ----------------------------------------------------------------------------