import json
import networkx as nx


def load_graph(file_name):
    G = nx.DiGraph()
    url_pair_list = json.load(open(file_name))
    for pair in url_pair_list:
        G.add_edge(pair["url_to"], pair["url_from"])

    return G


def count_in_out(nodes_list):
    i = 0
    for _ in nodes_list:
        i += 1
    return i

def save_in_out_pair(G, text_file):
    text_file.write("G node " + str(G.number_of_nodes()) + "\n")
    text_file.write("in out :" + "\n")
    node_in_out_list = []
    for node in G:
        in_out_pair = [count_in_out(G.in_edges(node)),
                       count_in_out(G.out_edges(node))]
        node_in_out_list.append(in_out_pair)

    text_file.write(str(min(node_in_out_list)))
    text_file.write(str(max(node_in_out_list)))
    write_list_to_file(text_file, node_in_out_list)

def write_list_to_file(file, mlist):
    for item in mlist:
        file.write("%s\n" % item)

def save_shortest_path(G, text_file):
    for node1 in G:
        for node2 in G:
            path_list = []
            try:
                shortest_path = nx.all_shortest_paths(G, node1, node2)
                print([p for p in shortest_path])
            except nx.NetworkXNoPath:
                print str(node1) + str(node2) + 'No path'
            # for path in nx.all_shortest_paths(G, node1, node2):
            #     pass
            text_file.write("\n"+str(node2) + str(node2) +":")
            write_list_to_file(text_file, path_list)

            # try:
            #     for path in nx.all_shortest_paths(G, node1, node2):
            #         path_list.append(path)
            #     text_file.write("%s : %s\n" % node1, node2)
            #     write_list_to_file(text_file, path_list)
            # except:
            #     text_file.write(str(node2) + str(node2) + " none\n")

    pass


if __name__ == "__main__":
    # G = load_graph('ubbcluj.json')
    G = load_graph('simple.json')
    text_file = open("shortest_path.txt", "w")

    save_shortest_path(G, text_file)

    pass