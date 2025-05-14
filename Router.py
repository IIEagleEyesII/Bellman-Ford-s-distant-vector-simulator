import Link

class DistantVectorTable:
    def __init__(self, router: 'Router'):
        self.router = router
        self.dv = {self.router:[0,self.router]}  # Dst : (cost, nextHop)

    def add_neighbor(self,link:'Link'):
        neighbor = link.get_neighbor(self.router)
        self.dv[neighbor] = [link.cost, self.router]


    def __str__(self):
        return f"{self.router.id }: \n {str(self.dv)}"

    @property
    def size(self):
        # Build a string representation like: "1:10>2;2:20>3;3:5>1"
        payload_str = ";".join(
            f"{dest}:{cost}>{next_hop.id if next_hop else 'None'}"
            for dest, (cost, next_hop) in self.dv.items()
        )
        return len(payload_str.encode('utf-8')) # en octets

    def __len__(self):
        """Returns the length of the packet in bytes."""
        return self.size

    """def initialize(self):
        self.dv[self.router] = [0, None]
        for link in self.router.outGoingLinks:
            neighbor = link.get_neighbor(self.router)
            self.dv[neighbor] = [link.cost, neighbor]
        self.router.propagate(self)"""

    def contains(self, dst: 'Router'):
        return self.dv.__contains__(dst)

    def get_cost(self, dst: 'Router'):
        return self.dv[dst][0]

    def set(self, dst: 'Router', cost: 'int', next_hop: 'Router'):
        self.dv[dst] = [cost, next_hop]

    def items(self): #itterator
        """Yields a list of tuples (dst, cost, next_hop)."""
        for dst in self.dv.keys():
            yield dst, self.dv[dst][0], self.dv[dst][1]


class Router:
    """
    A class representing a Router
    To access its neighbors, the list
    """

    def __init__(self, identifier: 'int', out_going_links: set['Link.Link']):
        """
        :param identifier: unique identifier.
        :param out_going_links: A set of outgoing links.
        Use Link.getNeighbor() to access the neighbor at each end.
        """
        self.id_ = identifier
        self.outGoingLinks_ = set() if out_going_links is None else out_going_links  # Empty set by default
        self.distantVectorTable_ = DistantVectorTable(self)

    def __hash__(self):
        return hash(self.id_)

    def __eq__(self, other):
        return isinstance(other, Router) and self.id_ == other.id_

    @property
    def id(self):
        return self.id_

    def __str__(self):
        return str(self.id_)

    def __repr__(self):
        return f"Router({self.id_})"

    @property
    def out_going_links(self):
        return self.outGoingLinks_

    def add_link(self, link: 'Link'):
        """Adds a link to the list of outgoing links.
         Used in the dynamic construction of the network"""
        self.outGoingLinks_.add(link)
        self.distantVectorTable_.add_neighbor(link)


    @property
    def neighbors(self):
        return [link.get_neighbor(self) for link in self.out_going_links]

    def get_dv_table(self):
        return self.distantVectorTable_

    def propagate(self, data: 'DistantVectorTable'):
        for link in self.outGoingLinks_:
            link.propagate(self, data)

    def receive(self, data: 'DistantVectorTable'):
        updated = False
        neighbor = data.router  # who ever propagated his dvt
        cost_to_neighbor = self.distantVectorTable_.get_cost(neighbor)
        for (destination, cost_from_neighbor_to_destination, neighbor_s_next_hop) in data.items():
            if destination == self:  # Skip entries about ourselves
                continue
            new_estimated_cost = cost_to_neighbor + cost_from_neighbor_to_destination
            if not self.distantVectorTable_.contains(destination): # first time encountering a non-adjacent router
                self.distantVectorTable_.set(destination, new_estimated_cost, neighbor)
                updated = True
            else: #had an estimation
                current_estimated_cost = self.distantVectorTable_.get_cost(destination)
                if current_estimated_cost > new_estimated_cost:
                    self.distantVectorTable_.set(destination, new_estimated_cost, neighbor)
                    updated = True
        if updated:
            self.propagate(self.distantVectorTable_)



    def update(self,neighbor: 'Router',old_cost: 'int',new_cost: 'int'):
        """Called when a link changes its cost, updates the DistantVectorTable and propagates if any change."""
        if old_cost == new_cost:
            return
        updated = False
        for (destination, cost, next_hop) in self.distantVectorTable_.items():
            if(destination==neighbor) and next_hop == self:
                self.distantVectorTable_.set(destination, new_cost,self)
                updated = True
            elif next_hop == neighbor:
                x = new_cost - old_cost
                if x !=0 :
                    previously_estimated_cost = self.distantVectorTable_.get_cost(destination)
                    self.distantVectorTable_.set(destination,previously_estimated_cost + x ,neighbor)
                    updated = True

        if updated:
            self.propagate(self.distantVectorTable_)


    def share_dv(self):
        self.propagate(self.distantVectorTable_)
