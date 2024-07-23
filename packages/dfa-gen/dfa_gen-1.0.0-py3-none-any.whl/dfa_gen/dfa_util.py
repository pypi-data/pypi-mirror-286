### utils ----------------------------------------------------------------------
def convert_aa_to_triple(aa_seq):
    aa_to_triple = {
        'F': "Phe", 'L': "Leu", 'S': "Ser", 'Y': "Tyr", 
        'C': "Cys", 'W': "Trp", 'P': "Pro", 'H': "His", 
        'Q': "Gln", 'R': "Arg", 'I': "Ile", 'M': "Met",
        'T': "Thr", 'N': "Asn", 'K': "Lys", 'V': "Val", 
        'D': "Asp", 'E': "Glu", 'G': "Gly", 'A': "Ala", 
        '*': "STOP",
    }
    return ' '.join([aa_to_triple[aa] for aa in aa_seq])

def utr_to_aa(utr_seq, codon_table):
    codon_to_aa = dict(zip(codon_table['codon'], codon_table['AA']))
    utr_aa = ""

    for i in range(0, len(utr_seq), 3):
        codon = utr_seq[i:i+3]
        aa = codon_to_aa[codon]
        utr_aa += aa

    return utr_aa

def get_ACGU_char(x):
    return 'A' if x == 1 else 'C' if x == 2 else 'G' if x == 3 else 'U' if x == 4 else 'X'

def get_ACGU_num(x):
    return 1 if x == 'A' else 2 if x == 'C' else 3 if x == 'G' else 4 if x == 'U' else 0