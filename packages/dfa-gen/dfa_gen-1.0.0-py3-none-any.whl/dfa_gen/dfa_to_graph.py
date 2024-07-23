import pandas as pd

### DFA to tsv -----------------------------------------------------------------
def read_dfa_contents(dfa_contents):
    nodes = dfa_contents.strip().split('%')

    node_map = {}

    for node in nodes:
        lines = node.strip().split('\n')
        node_id = None
        node_info = {}
        for line in lines:
            if line.startswith("node:"):
                node_id = line.split(":")[1].strip()
            elif line != "":
                key, value = line.split(':')
                value_list = value.strip().split(';')
                if 'R' in key:
                    direction = 'right'
                else:
                    direction = 'left'
                node_info[key.strip()] = {
                    "direction": direction,
                    "next_node": value_list[2],
                    "base": value_list[0],
                    "weight": round(float(value_list[1]), 2),
                }
        if node_id:
            node_map[node_id] = node_info
    
    return node_map

def node_map_to_tsv(aa_seq, utr_trimmed, node_map, file_path):
    node_data = []
    utr_start_pos = (len(aa_seq) - len(utr_trimmed) // 3) * 3

    for node_id, info in node_map.items():
        node_id_first = int(node_id.split(",")[0].strip('('))
        node_id_second = int(node_id.split(",")[1].strip(')'))

        if node_id_first // 3 == len(aa_seq):
            node_name = 'X'
        else:
            node_name = aa_seq[node_id_first // 3]

        for key, details in info.items():
            utr = node_id_first >= utr_start_pos
            user_utr = 'N'

            if node_id_first == utr_start_pos and details["direction"] == 'left':
                utr = False
            if utr:
                utr_index = node_id_first - utr_start_pos
                if utr_index <= len(utr_trimmed):
                    if details["direction"] == 'right':
                        user_utr = utr_trimmed[utr_index]
                    else:
                        user_utr = utr_trimmed[utr_index - 1]

            node_data.append({
                "node_id": node_id,
                "node_aa": f"{node_name}{node_id_first // 3}_{node_id_first % 3}_{node_id_second}",
                "utr": utr,
                "user_utr": user_utr,
                "direction": details["direction"],
                "next_node": details["next_node"],
                "base": details["base"],
                "weight": details["weight"],
            })


    df = pd.DataFrame(node_data)
    df.to_csv(file_path, sep='\t', index=False)

### ----------------------------------------------------------------------------
### graphviz -------------------------------------------------------------------
def generate_graphviz_code(df):
    node_default = {
        "shape": "circle",
        "style": "filled",
        "color": "gainsboro"
    }
    
    graph_code = ["digraph G {\n    rankdir=LR"]
    
    for node_id in df['node_id'].unique():
        node_color = node_default["color"]
        node_aa = df[df['node_id'] == node_id]['node_aa'].values[0]
        node_utr = df[df['node_id'] == node_id]['utr'].values[0]

        if int(node_id.split(',')[0][1:]) % 3 == 0:
            node_color = "aquamarine3"
            if node_utr == True:
                node_color = "cornflowerblue"
        if '*' in node_aa and "_0_" in node_aa:
            node_color = "darksalmon"

        graph_code.append(f'    "{node_id}" [label="{node_id}\\n{node_aa}", shape={node_default["shape"]}, style={node_default["style"]}, color={node_color}];')

    last_node_id = df['node_id'].unique()[-1]
    graph_code.append(f'    "{last_node_id}" [color=darkgoldenrod1];\n')
    
    for _, row in df[df['direction'] == 'right'].iterrows():
        edge_label = f'{row["base"]}:{row["weight"]}'

        if row["utr"] and row["user_utr"] != row["base"]:
            graph_code.append(f'    "{row["node_id"]}" -> "{row["next_node"]}" [label="{edge_label}", color=gray];')
        else:
            graph_code.append(f'    "{row["node_id"]}" -> "{row["next_node"]}" [label="{edge_label}"];')

    graph_code.append("}")
    
    return "\n".join(graph_code)

### ----------------------------------------------------------------------------