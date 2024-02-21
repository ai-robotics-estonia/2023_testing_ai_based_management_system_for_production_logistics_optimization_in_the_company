import sys, os, heapq
from .helpers import p
class PathWorker():

    def __init__(self, beacon, pw):
        try:

            self.beacon = beacon # Whos transporting
            self.pos_worker = pw # Parent entity that is part of transport system management
            self.resetsetPathData()
        except Exception as e:
            p(e)

    def resetsetPathData(self):
        self.start_points = {}
        for key, anchor in self.pos_worker.anchor_obj.items():
            # add anchors
            g = self.setGraph()
            self.start_points[anchor.id] = g
            setPath(g, g.get_vertex(anchor.id))

    def setGraph(self):
        g = Graph()
        for key, anchor in self.pos_worker.anchor_obj.items():
            g.add_vertex(anchor.id)
        # add anchor connections with time as weight
        for key, connection in self.pos_worker.anchor_connection_obj.items():
            #filter out what connections can be used by this beacon
            if self.beacon.width <= connection.width:
                connection_time = connection.distance / (self.beacon.speed / 3.6)
                g.add_edge(connection.anchor_id_start, connection.anchor_id_end, connection_time)
                if connection.direction == 'B':
                    g.add_edge(connection.anchor_id_end, connection.anchor_id_start, connection_time)
        return g

    def shortest(self, v, path):
        ''' make shortest path from v.previous'''
        if v.previous:
            path.append(v.previous.get_id())
            self.shortest(v.previous, path)
        return
    def get_connection(self, anchor_start_id, anchor_end_id):
        try:
            target = self.start_points[anchor_start_id].get_vertex(anchor_end_id)
            path = [target.get_id()]
            self.shortest(target, path)
            accessible = True
            if len(path) == 1 and anchor_start_id != anchor_end_id:
                accessible = False
            o = {
                'path': path[::-1],
                'time': target.get_distance(),
                'destination_adjacent': target.get_adjacent(),
                'accessible': accessible
            }
            return o
        except Exception as e:
            p(e)

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxsize
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def get_adjacent(self):
        return [x.id for x in self.adjacent]

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.distance == other.distance
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.distance < other.distance
        return NotImplemented

    def __hash__(self):
        return id(self)


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous




def setPath(aGraph, start):
    try:
        # Set the distance for the start node to zero
        start.set_distance(0)

        # Put tuple pair into the priority queue
        unvisited_queue = [(v.get_distance(), v) for v in aGraph]
        heapq.heapify(unvisited_queue)

        while len(unvisited_queue):
            # Pops a vertex with the smallest distance
            uv = heapq.heappop(unvisited_queue)
            current = uv[1]
            current.set_visited()
            # for next in v.adjacent:
            for next in current.adjacent:
                # if visited, skip
                if next.visited:
                    continue
                new_dist = current.get_distance() + current.get_weight(next)
                if new_dist < next.get_distance():
                    next.set_distance(new_dist)
                    next.set_previous(current)
                else:
                    pass
            # Rebuild heap
            # 1. Pop every item
            while len(unvisited_queue):
                heapq.heappop(unvisited_queue)
            # 2. Put all vertices not visited into the queue
            unvisited_queue = [(v.get_distance(), v) for v in aGraph if not v.visited]
            heapq.heapify(unvisited_queue)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(e, exc_type, fname, exc_tb.tb_lineno)


