import argparse
import pandas as pd
import graphviz
import os

from dfa_gen.dfa_class import Codon, DFA, NodeType
from dfa_gen.dfa_util import get_ACGU_char, utr_to_aa, convert_aa_to_triple
from dfa_gen.generate_lattice import prepare_codon_unit_lattice
from dfa_gen.dfa_to_graph import read_dfa_contents, node_map_to_tsv, generate_graphviz_code

def get_dfa(aa_graphs, protein, utr_trimmed):
    dfa = DFA()
    newnode = NodeType(3 * len(protein), 0)
    is_utr = -1

    dfa.add_node(newnode)

    for i, aa in enumerate(protein):
        i3 = i * 3
        graph = aa_graphs[aa]

        for pos in range(3):
            for node in graph.nodes[pos]:
                num = node.num
                newnode = NodeType(i3 + pos, num)
                
                dfa.add_node(newnode)
                for edge in graph.right_edges[node]:
                    n2 = edge.node
                    nuc = edge.nuc
                    num = n2.num
                    newn2 = NodeType(i3 + pos + 1, num)
                    if is_utr == -1:
                        dfa.add_edge(newnode, newn2, nuc, round(edge.weight * 100, 3))
                    elif is_utr < len(utr_trimmed):
                        if utr_trimmed[is_utr] == get_ACGU_char(nuc):
                            dfa.add_edge(newnode, newn2, nuc, 0)
                            # dfa.add_edge(newnode, newn2, nuc, round(edge.weight * 100, 3))
                        # else:
                            # dfa.add_edge(newnode, newn2, nuc, 0)
            if is_utr > -1:
                is_utr += 1
        if aa == "STOP" and is_utr == -1:
            is_utr = 0
    return dfa

def dfa_generator(seq, utr, lambda_val=0, output="untitled"):
    FILE_PATH = str(os.path.abspath(__file__))[:-15]
    SEQ = seq
    UTR = utr
    LAMBDA_VAL = lambda_val
    
    os.makedirs(f"output", exist_ok=True)
    DFA_FILE = f"output/{output}_lam_{int(lambda_val)}"

    CODON_TABLE = f"{FILE_PATH}/data/codon_freq_table.tsv"
    CODING_WHEEL = f"{FILE_PATH}/data/coding_wheel.txt"

    codon_table = pd.read_csv(CODON_TABLE, sep='\t')
    utr_trimmed = UTR[:len(UTR) - (len(UTR) % 3)]
    utr_aa = utr_to_aa(utr_trimmed, codon_table)

    if UTR != "" and SEQ[-1] != '*':
        SEQ = SEQ + '*'
    aa_seq = SEQ + utr_aa

    codon = Codon(CODON_TABLE)
    aa_graphs_with_ln_weights = prepare_codon_unit_lattice(CODING_WHEEL, codon, lambda_=LAMBDA_VAL)
    
    aa_tri_seq = convert_aa_to_triple(aa_seq)
    protein = aa_tri_seq.split()
    dfa = get_dfa(aa_graphs_with_ln_weights, protein, utr_trimmed)

    print(f"{SEQ}")
    print(f"{utr_trimmed}")
    print(f"{aa_seq}")
    dfa.print()

    # with open(f"{DFA_FILE}.txt", 'r') as file:
    #     SEQ = file.readline().strip()
    #     UTR = file.readline().strip()
    #     dfa_input_seq = file.readline().strip()
    #     dfa_contents = file.read()

    # node_map = read_dfa_contents(dfa_contents)
    # node_map_to_tsv(dfa_input_seq, utr_trimmed, node_map, f"{DFA_FILE}.tsv")

    # df = pd.read_csv(f"{DFA_FILE}.tsv", sep='\t')
    # graphviz_code = generate_graphviz_code(df)
    # dot = graphviz.Source(graphviz_code)
    # dot.render(f'{DFA_FILE}_graph', format='png')

def main():
    parser = argparse.ArgumentParser(description="Generate DFA from sequence")
    parser.add_argument("seq", type=str, help="The amino acid sequence")
    parser.add_argument("-u", "--utr", type=str, default="", help="The 3'UTR sequence")
    parser.add_argument("-l", "--lambda_val", type=float, default=0, help="The lambda value for calculating edge weight")
    parser.add_argument("-o", "--output", type=str, default="untitled", help="The name of output files")

    args = parser.parse_args()
    dfa_generator(args.seq, args.utr, args.lambda_val, args.output)

if __name__ == "__main__":
    main()