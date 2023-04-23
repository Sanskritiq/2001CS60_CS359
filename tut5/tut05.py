import queue
import threading
import sys
import time

# create lock
lock = threading.Lock()

# define adjancy matrix and all routing tables variables
adj_matrix = {}
all_tables = {}

# fun to input new node in adj_matrix
def new_node(node1, node2, w):

    if node1 not in adj_matrix:
        adj_matrix[node1] = {}
    adj_matrix[node1][node2] = int(w)

    if node2 not in adj_matrix:
        adj_matrix[node2] = {}
    adj_matrix[node2][node1] = int(w)

# fun to read topology text file and extract number of routers, routers name and update adj_matrix
def read_txt_file(path):

    file = open(path, 'r')
    lines = file.readlines()
    file.close()
    n = int(lines[0].strip())
    nodes = lines[1].split()
    for l in lines[2:]:
        l = l.split()
        if l == 'EOF':
            break
        if len(l) >= 3:
            new_node(l[0], l[1], int(l[2]))
        else:
            print(' ' if l != 'EOF' else 'wrong topology')

    return n, nodes


# read no. of nodes and all nodes name from file and update adjancy matrix
n_nodes = read_txt_file(
    '/home/sanskriti/Documents/GitHub/2001CS60_CS359/tut5/topology.txt')
n = n_nodes[0]
nodes = n_nodes[1]
for node in nodes:
    all_tables[node] = {}

# fun to initialize router  table according to the adj_matrix
def init_routing_table(node_router):

    for adj_node, distance in adj_matrix[node_router].items():
        all_tables[node_router][adj_node] = [distance, adj_node]

    for node in nodes:
        if node != node_router and node not in adj_matrix[node_router]:
            all_tables[node_router][node] = [float('inf'), None]
            
for node in nodes:
    init_routing_table(node)
    # print initial router table
    print('\nInitial')
    print('Routing Table for:', node)
    print('\ndest\tcost\tnext_hop')
    for dest, [distance, next_hop] in all_tables[node].items():
        print(dest, distance, next_hop, sep='\t')
        

class router_thread(threading.Thread):

    # initialize the threads
    def __init__(self, node_router):

        threading.Thread.__init__(self)
        self.node_router = node_router

    def run(self):
        # update routing table
        self.update_routing_table()
        
        lock.acquire()
        # print if get updated
        print('\n***Routing table', self.node_router, ':UPDATED***')
        lock.release()

        # sleep for 1 second
        time.sleep(1)
        
    # fun for dikstra algorithm
    def dijkstra(self):
        
        # cost and previous node for each node
        cost = {self.node_router: 0}
        prev = {self.node_router: None}
        # nodes that are unvisited
        unvisited = set(nodes)

        # for nonvisited nodes initialize cost to inf and previous node as none
        for dest in unvisited:
            if dest == self.node_router:
                continue
            cost[dest] = float('inf')
            prev[dest] = None

        # while still unvisited nodes left
        while unvisited:
            # Find the unvisited node with least cost
            current = min(unvisited, key=lambda x: cost[x])
            unvisited.remove(current)

            # Update the cost and previous node for each adjacent node of the current node
            for adj_node in adj_matrix[current]:
                if adj_node in unvisited:
                    new_cost = cost[current] + adj_matrix[current][adj_node]
                    # update cost and previous node if shorter path exist
                    if new_cost < cost[adj_node]:
                        cost[adj_node] = new_cost
                        prev[adj_node] = current
                        
        # Return the previous nodes and costs for each destination
        return prev, cost

    def update_routing_table(self):
        prev, dist = self.dijkstra()

        lock.acquire()
        # update the shortest distance in routing table
        for current, distance in dist.items():
            if current != self.node_router:
                all_tables[self.node_router][current][0] = distance

        # update the next hop in routing table
        for dest in dist:
            if dest != self.node_router:
                next_hop = None
                current = dest
                while prev[current] != self.node_router:
                    current = prev[current]
                next_hop = current
                all_tables[self.node_router][dest][1] = next_hop
                
        # print final router table
        print('\nFinal')
        print('Routing Table for:', self.node_router)
        print('\ndest\tcost\tnext_hop')
        for dest, [distance, next_hop] in all_tables[self.node_router].items():
            print(dest, distance, next_hop, sep='\t')
                
        lock.release()


        
# initialize list for threads
threads = []
# creating thread for each router
for node in nodes:
    new_router_thread = router_thread(node)
    new_router_thread.start()
    threads.append(new_router_thread)

# join all threads
for thread in threads:
    thread.join()

