# import lib
import threading
import time
import queue
import sys

# define global var like adjency matrix, router table dict, receiving queue dict     
adj_matrix = {}
all_tables = {}
all_queues = {}

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
        if l=='EOF' : break
        if len(l)>=3:
            new_node(l[0], l[1], int(l[2])) 
        else: print(' ' if l!='EOF' else 'wrong topology')  
        
    return n, nodes   

n_nodes = read_txt_file('/home/sanskriti/Documents/GitHub/2001CS60_CS359/tut4/topology.txt')
n = n_nodes[0]
nodes = n_nodes[1]

# print details
print('Total routers:', n)
print('Routers:', nodes)
print('\nAdjacency Matrix:')
print(adj_matrix)

# initialize empty routing table and receiving queue for each node
for node in nodes:
    all_queues[node] = queue.Queue()
    all_tables[node] = {}
# create lock
lock = threading.Lock()

# thread for each router
class router_thread(threading.Thread):
    
    def __init__(self, node_router):
        
        threading.Thread.__init__(self)
        self.node_router = node_router
        self.iteration = 1 #iterator
        self.updation = False
        
    def run(self):
        # initialize router table
        self.init_routing_table()
        lock.acquire()
        # print initial router table
        print('\nInitial')
        print('Routing Table for:', self.node_router)
        print('\ndest\tcost\tnext_hop')
        for dest, [distance, next_hop] in all_tables[self.node_router].items():
            print(dest, distance, next_hop, sep='\t')
        lock.release()
        
        for i in range(50):
            # update routing table
            self.update_routing_table()
            lock.acquire()
            # print after updation process
            print('\nIteration:', self.iteration)
            print('Routing Table for:', self.node_router)
            print('\ndest\tcost\tnext_hop')
            for dest, [distance, next_hop] in all_tables[self.node_router].items():
                print(dest, distance, next_hop, sep='\t')
            self.iteration += 1
            # increament iterator
            lock.release()
        
            time.sleep(2)
    
    # fun to initialize router  table according to the adj_matrix      
    def init_routing_table(self):
        
        for adj_node, distance in adj_matrix[self.node_router].items():
            all_tables[self.node_router][adj_node] = [distance, adj_node]
                        
        for node in nodes:
            if node != self.node_router and node not in adj_matrix[self.node_router]:
                all_tables[self.node_router][node] = [float('inf'), None]
    
    # fun to send routing table to adjacent nodes    
    def send_routing_table(self):
    
        for adj_node in adj_matrix[self.node_router]:
            all_queues[adj_node].put((self.node_router, all_tables[self.node_router]))

    # fun to receive routing table from adjacent nodes
    def receive_routing_table(self):
        
        # wait for all adjacent nodes to sent routing tables
        while all_queues[self.node_router].qsize() < len(adj_matrix[self.node_router]):
            time.sleep(1)
        
        # check for all received routing tables
        while not all_queues[self.node_router].empty():
            
            (adj_node, received_table) = all_queues[self.node_router].get()
            
            # bellmann fords algo to update cost and next hop
            self.updation = False
            for dest, [distance, next_hop] in received_table.items():
                
                if dest != self.node_router:
                                
                    new_distance = adj_matrix[self.node_router][adj_node] + distance
                    if new_distance < all_tables[self.node_router][dest][0]:
                        all_tables[self.node_router][dest][0] = new_distance
                        all_tables[self.node_router][dest][1] = adj_node
                        self.updation = True
            lock.acquire()
            if self.updation:
                # print if get updated
                print('\n***Routing table', self.node_router, ':UPDATED***')
            lock.release()
        
    def update_routing_table(self):
        
        # send and recieve routing tables
        self.send_routing_table()
        self.receive_routing_table()
        
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
        
        
