import json
import time
from Link import Link
from Router import Router

class NetworkSimulator:
    def __init__(self, json_path):
        self.routers = {}  # id (int) -> Router
        self.links = []  # List of Link objects
        self.events = []  # List of events, sorted by time (ms)
        self.time = 0
        self.load_from_json(json_path)

    def load_from_json(self, json_path):
        with open(json_path) as f:
            data = json.load(f)

        for link_data in data["links"]:  # Create Routers
            id1, id2 = link_data["endpoints"]
            r1 = self.routers.setdefault(id1, Router(id1, set())) # get if exists else create it
            r2 = self.routers.setdefault(id2, Router(id2, set()))

            link = Link( # Create Link
                r1, r2,
                cost=link_data["cost"],
                length=link_data["distance"],
                transmission_speed=link_data["transmission_speed"],
                propagation_speed=link_data["propagation_speed"]
            )

            r1.add_link(link)
            r2.add_link(link)
            self.links.append(link)

        # Store events sorted by trigger time
        self.events = sorted(data["events"], key=lambda e: e["time"])

    def run(self):

        for router in self.routers.values(): #Routers exchange their dvt's
            router.share_dv()



        # Step 2: Process events in chronological order
        for event in self.events:
            delay = (event["time"] / 1000) - self.time  # convert ms to seconds
            if delay > 0:
                time.sleep(delay)
            self.time = event["time"] / 1000  # advance simulation time

            if event["type"] == "cost_change":
                self.apply_cost_change(event)

    def spark(self):
        """It only takes one (any) router to share its dvt to start the whole process"""
        router = self.routers.get(1)
        router.share_dv()

    def apply_cost_change(self, event):
        id1, id2 = event["link"]
        new_cost = event["new_cost"]
        for link in self.links:
            if {link.router1.id, link.router2.id} == {id1, id2}:
                link.cost = new_cost  # This triggers updates
                break

    def get_routers(self):
        return self.routers.values()

    def get_links(self):
        return self.links