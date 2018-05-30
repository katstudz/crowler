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


def save_shortest_path(G):
    text_file = open("shortest_path.txt", "w")
    for node1 in G:
        for node2 in G:
            pre_text = "\n" + str(node2) + " " + str(node2) + ":"
            try:
                shortest_path = nx.all_shortest_paths(G, node1, node2)
                text_file.write(pre_text + str(next(shortest_path)))
            except nx.NetworkXNoPath:
                text_file.write(pre_text + 'No path')
    pass


def average_shortest_path_length(G):
    avr = 0
    for node1 in G:
        for node2 in G:
            try:
                shortest_path = nx.all_shortest_paths(G, node1, node2)
                avr += sum(1 for _ in shortest_path)
            except nx.NetworkXNoPath:
                pass
    return avr / len(G.node())


def check_diameter(G):
    try:
        print(nx.diameter(G))
    except nx.NetworkXError:
        print("infinite path length - digraph is not strongly connected")


def pagerank(G, alpha=0.85, personalization=None,
             max_iter=100, tol=1.0e-6, nstart=None, weight='weight',
             dangling=None):
    if len(G) == 0:
        return {}

    if not G.is_directed():
        D = G.to_directed()
    else:
        D = G

    # Create a copy in (right) stochastic form
    W = nx.stochastic_graph(D, weight=weight)
    N = W.number_of_nodes()

    # Choose fixed starting vector if not given
    if nstart is None:
        x = dict.fromkeys(W, 1.0 / N)
    else:
        # Normalized nstart vector
        s = float(sum(nstart.values()))
        x = dict((k, v / s) for k, v in nstart.items())

    if personalization is None:
        # Assign uniform personalization vector if not given
        p = dict.fromkeys(W, 1.0 / N)
    else:
        s = float(sum(personalization.values()))
        p = dict((k, v / s) for k, v in personalization.items())

    if dangling is None:
        # Use personalization vector if dangling vector not specified
        dangling_weights = p
    else:
        s = float(sum(dangling.values()))
        dangling_weights = dict((k, v/s) for k, v in dangling.items())
    dangling_nodes = [n for n in W if W.out_degree(n, weight=weight) == 0.0]

    # power iteration: make up to max_iter iterations
    for _ in range(max_iter):
        xlast = x
        x = dict.fromkeys(xlast.keys(), 0)
        danglesum = alpha * sum(xlast[n] for n in dangling_nodes)
        for n in x:
            # this matrix multiply looks odd because it is
            # doing a left multiply x^T=xlast^T*W
            for nbr in W[n]:
                x[nbr] += alpha * xlast[n] * W[n][nbr][weight]
            x[n] += danglesum * dangling_weights.get(n,0) + (1.0 - alpha) * p.get(n,0)
        # check convergence, l1 norm
        err = sum([abs(x[n] - xlast[n]) for n in x])
        if err < N*tol:
            return x
    raise nx.PowerIterationFailedConvergence(max_iter)

if __name__ == "__main__":
    G = load_graph('rumunia_univ.json')

    # G = load_graph('simple.json')
    # print(average_shortest_path_length(G))
    print(nx.transitivity(G))
    nx.pagerank

    pass
