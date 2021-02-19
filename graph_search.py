def bfs(graph, node_start):
    nodes_explored = [node_start]
    queue = [node_start]
    while len(queue) != 0:
        node_popped = queue.pop()
        if node_popped in graph:
            for child in graph[node_popped]:
                if child not in nodes_explored:
                    nodes_explored.append(child)
                    queue.insert(0, child)
    return nodes_explored


def dfs_non_recursive(graph, node_start):
    nodes_explored = [node_start]
    stack = [node_start]
    while len(stack) != 0:
        node_popped = stack.pop()
        if node_popped in graph:
            for child in graph[node_popped]:
                if child not in nodes_explored:
                    nodes_explored.append(child)
                    stack.append(child)
    return nodes_explored


def dfs_recursive(graph, node_start, nodes_explored=None):
    if nodes_explored is None:
        nodes_explored = set()
    nodes_explored.add(node_start)
    if node_start in graph:
        for child in graph[node_start]:
            if child not in nodes_explored:
                nodes_explored = dfs_recursive(graph, child, nodes_explored)
    return nodes_explored


def get_shortest_path(graph, node_start):
    node_to_path_count_dict = {node_start:0}
    queue = [node_start]
    while len(queue) != 0:
        node_popped = queue.pop()
        if node_popped in graph:
            for child in graph[node_popped]:
                if child not in node_to_path_count_dict:
                    node_to_path_count_dict[child] = node_to_path_count_dict[node_popped] + 1
                    queue.insert(0, child)
    return node_to_path_count_dict


def compute_strongly_connected_components_on_undirected_graph(graph, nodes):
    def _bfs(graph, nodes_explored, node_start):
        nodes_explored.append(node_start)
        connected_components = [node_start]
        queue = [node_start]
        while len(queue) != 0:
            node_popped = queue.pop()
            if node_popped in graph:
                for child in graph[node_popped]:
                    if child not in nodes_explored:
                        queue.append(child)
                        nodes_explored.append(child)
                        connected_components.append(child)
        return nodes_explored, connected_components

    nodes_explored = []
    connected_components = []
    for node in nodes:
        if node not in nodes_explored:
            nodes_explored, connected_component = _bfs(graph, nodes_explored, node)
            connected_components.append(connected_component)
    return connected_components


def compute_topological_sort(graph, nodes):
    nodes_label = {}
    current_label = len(nodes)
    for node in nodes:
        if node not in nodes_label:
            nodes_label[node] = None
            stack = [node]
            while len(stack) != 0:
                node_last = stack[-1]
                if node_last in graph:
                    for child in graph[node_last]:
                        if child not in nodes_label:
                            nodes_label[child] = None
                            stack.append(child)

                if node_last == stack[-1]:
                    node_last = stack.pop()
                    nodes_label[node_last] = current_label
                    current_label -= 1
    return nodes_label


def compute_topological_sort2(graph, nodes):
    def _dfs(graph, node_start):
        nonlocal nodes_label, count
        nodes_label[node_start] = None
        if node_start in graph:
            for child in graph[node_start]:
                if child not in nodes_label:
                    _dfs(graph, child)
        nodes_label[node_start] = count
        count -= 1

    nodes_label = {}
    count = len(nodes)
    for node in nodes:
        if node not in nodes_label:
            _dfs(graph, node)
    return nodes_label


def compute_strongly_connected_components_on_directed_graph(graph, nodes):
    def _get_nodes_label_order(graph, nodes):
        def _get_reversed_graph(graph):
            reversed_graph = {}
            for key, val in graph.items():
                for node in val:
                    if node in reversed_graph:
                        reversed_graph[node].append(key)
                    else:
                        reversed_graph[node] = [key]
            return reversed_graph

        def _dfs_on_reversed_graph(graph, node_start):
            nonlocal label_dict, count
            label_dict[node_start] = None
            if node_start in graph:
                for child in graph[node_start]:
                    if child not in label_dict:
                        _dfs_on_reversed_graph(graph, child)
            label_dict[node_start] = count
            count += 1

        label_dict, count = {}, 1
        reversed_graph = _get_reversed_graph(graph)
        for node in nodes:
            if node not in label_dict:
                _dfs_on_reversed_graph(reversed_graph, node)
        return label_dict

    nodes_label_order = sorted([(key, val) for key, val in _get_nodes_label_order(graph, nodes).items()], key=lambda x: x[1], reverse=True)
    nodes_explored = {}
    scc_combined = []

    def _dfs_on_original_graph(graph, node_start):
        nonlocal nodes_explored
        scc = []

        nodes_explored[node_start] = None
        scc.append(node_start)
        if node_start in graph:
            for child in graph[node_start]:
                if child not in nodes_explored:
                    scc += _dfs_on_original_graph(graph, child)
        return scc

    for node, _ in nodes_label_order:
        if node not in nodes_explored:
            scc_combined.append(_dfs_on_original_graph(graph, node))
    return scc_combined


directed_graph = {"A": ['B', 'C', 'D'],
         'B': ['E'],
         'C': ['F', 'G'],
         'D': ['H'],
         'E': ['I'],
         'F': ['J']}

undirected_graph = {
           'G': ['C'],
           'F': ['C'],
           'E': ['A', 'B', 'D'],
           'A': ['B', 'E', 'C'],
           'B': ['A', 'D', 'E'],
           'D': ['B', 'E'],
           'C': ['A', 'F', 'G']
        }

print(bfs(directed_graph, 'A'))
print(dfs_non_recursive(directed_graph, 'A'))
print(dfs_recursive(directed_graph, 'A'))
print(get_shortest_path(undirected_graph, 'A'))
print(compute_strongly_connected_components_on_undirected_graph(undirected_graph, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']))
print(compute_topological_sort2(directed_graph, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']))
print(compute_topological_sort(directed_graph, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']))
print(compute_strongly_connected_components_on_directed_graph(directed_graph, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']))