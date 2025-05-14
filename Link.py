import Router

class Link:
    """
    A class representing a link between two routers.
    Must be initiated with both routers, which are considered as final.
    """
    def __init__(self, router1:'Router.Router', router2:'Router.Router', cost=None, length=None, transmission_speed=None, propagation_speed=None):
        self.router2_ = router2
        self.router1_ = router1
        self.transmissionSpeed_ = transmission_speed #in bps //in contrast with the bandwidth which is the maximal (potential) transmissionSpeed, the transmission speed refers to the actual usage of the capacity depending on current factors(congestion...)
        self.length_ = length #in m
        self.cost_ = cost
        self.propagationSpeed_ = propagation_speed # in m/s


    def compute_delay(self, packet):
        propagation_delay = self.propagation_delay
        transmission_delay = (len(packet)*8)/self.transmissionSpeed_
        #ignore processing and queueing delays
        return propagation_delay + transmission_delay

    def get_neighbor(self, asking_router: 'Router.Router'):
        if asking_router == self.router1_:
            return self.router2_
        else:
            return self.router1_

    def __str__(self):
        res = "\t\t{\n"
        res+=f"\t\t\t\"propagation_speed\": {str(self.propagation_speed)},\n"
        res+=f"\t\t\t\"transmission_speed\": {str(self.transmission_speed)},\n"
        res+=f"\t\t\t\"distance\": {str(self.length)},\n"
        res+=f"\t\t\t\"cost\": {str(self.cost)},\n"
        res+=f"\t\t\t\"endpoints\": [{str(self.router1)}, {str(self.router2)}]\n"
        res+="\t\t}"
        return res

    def __repr__(self):
        res =f"endpoints \" : [{str(self.router1)}, {str(self.router2)}]\n"
        return res

    def propagate(self,source :'Router.Router', data: 'Router.DistantVectorTable'):
        #print(f"Propagating from {source.id} to {self.get_neighbor(source).id}")
        #print(data)
        dst = self.get_neighbor(source)
        #delay = self.computeDelay(data)
        #time.sleep(delay) #Simulate the delay todo : replace time.sleep() logic !
        dst.receive(data)

    @property
    def propagation_delay(self):
        return self.length / self.propagationSpeed_

    @property
    def cost(self):
        return self.cost_

    @cost.setter
    def cost(self, new_cost):
        self.router1_.update(self.router2_,self.cost_,new_cost)
        self.router2_.update(self.router1_,self.cost_,new_cost)
        self.cost_ = new_cost
        #todo add to the log !

    @property
    def length(self):
        return self.length_
    @length.setter
    def length(self, value):
        self.length_ = value

    @property
    def transmission_speed(self):
        return self.transmissionSpeed_
    @transmission_speed.setter
    def transmission_speed(self, value):
        self.transmissionSpeed_ = value

    @property
    def router1(self):
        return self.router1_

    @property
    def router2(self):
        return self.router2_

    @property
    def propagation_speed(self):
        return self.propagationSpeed_
    @propagation_speed.setter
    def propagation_speed(self, value):
        self.propagationSpeed_ = value



