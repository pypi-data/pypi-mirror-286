from collections import defaultdict, namedtuple
from dfa_gen.dfa_util import get_ACGU_char
import csv

NodeType = namedtuple("NodeType", ["index", "num"])
NodeNucWType = namedtuple("NodeNucWType", ["node", "nuc", "weight"])
NodeNucNodeType = namedtuple("NodeNucNodeType", ["node1", "nuc", "node2"])

### ----------------------------------------------------------------------------
k_map_3_1 = {
    "Phe": 'F',
    "Leu": 'L',
    "Ser": 'S',
    "Tyr": 'Y',
    "STOP": '*',
    "Cys": 'C',
    "Trp": 'W',
    "Pro": 'P',
    "His": 'H',
    "Gln": 'Q',
    "Arg": 'R',
    "Ile": 'I',
    "Met": 'M',
    "Thr": 'T',
    "Asn": 'N',
    "Lys": 'K',
    "Val": 'V',
    "Asp": 'D',
    "Glu": 'E',
    "Gly": 'G',
    "Ala": 'A'
}

### (class) Codon --------------------------------------------------------------
class Codon:
    def __init__(self, path):
        self.codon_table = {}
        self.aa_table = defaultdict(list)
        self.max_aa_table = {}

        with open(path) as codon_file:
            reader = csv.DictReader(codon_file, delimiter='\t')
            for row in reader:
                codon = row['codon']
                aa = row['AA']
                fraction = float(row['freq'])
                self.codon_table[codon] = (aa, fraction)
                self.aa_table[aa].append((codon, fraction))
                self.max_aa_table[aa] = max(self.max_aa_table.get(aa, 0), fraction)

            if len(self.codon_table) != 64:
                raise ValueError("Codon frequency file needs to contain 64 codons!")

    def get_weight(self, aa_tri, codon):
        if aa_tri in k_map_3_1:
            aa = k_map_3_1[aa_tri]
            if aa in self.aa_table:
                codons = self.aa_table[aa]
                for c, weight in codons:
                    if c == codon:
                        return weight
        return 0.0

### (class) Lattice ------------------------------------------------------------
class Lattice:
    def __init__(self):
        self.nodes = defaultdict(list)
        self.left_edges = defaultdict(list)
        self.right_edges = defaultdict(list)

    def add_edge(self, n1, n2, nuc, weight=0.0):
        self.right_edges[n1].append(NodeNucWType(n2, nuc, weight))
        self.left_edges[n2].append(NodeNucWType(n1, nuc, weight))

    def add_node(self, n1):
        pos = n1.index
        self.nodes[pos].append(n1)

### (class) DFA ----------------------------------------------------------------
class DFA:
    def __init__(self):
        self.nodes = defaultdict(list)
        self.left_edges = defaultdict(list)
        self.right_edges = defaultdict(list)
        self.auxiliary_left_edges = defaultdict(lambda: defaultdict(list))
        self.auxiliary_right_edges = defaultdict(lambda: defaultdict(list))
        self.node_rightedge_weights = defaultdict(dict)

    def add_edge(self, n1, n2, nuc, weight=0.0):
        self.right_edges[n1].append(NodeNucWType(n2, nuc, weight))
        self.left_edges[n2].append(NodeNucWType(n1, nuc, weight))
        self.auxiliary_right_edges[n1][n2].append((nuc, weight))
        self.auxiliary_left_edges[n2][n1].append((nuc, weight))
        self.node_rightedge_weights[n1][nuc] = weight

    def add_node(self, n1):
        pos = n1.index
        self.nodes[pos].append(n1)

    def print(self, file=None):
        if file is None:
            import sys
            file = sys.stdout
            
        sorted_keys = sorted(self.nodes.keys())
        print("%", file=file)
        for key in sorted_keys:
            for node in self.nodes[key]:
                print(f"node:\t({node.index}, {node.num})", file=file)
                if node in self.right_edges:
                    for cnt, edge in enumerate(self.right_edges[node], 1):
                        print(f"R_{cnt}:\t{get_ACGU_char(edge.nuc)};{edge.weight};({edge.node.index}, {edge.node.num})", file=file)
                if node in self.left_edges:
                    for cnt, edge in enumerate(self.left_edges[node], 1):
                        print(f"L_{cnt}:\t{get_ACGU_char(edge.nuc)};{edge.weight};({edge.node.index}, {edge.node.num})", file=file)
                print("%", file=file)