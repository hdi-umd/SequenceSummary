import json


class Rawnode:
    def __init__(self, node):
        self.nid = node.nid
        self.seqCount = node.seqCount
        self.value = node.value
        self.pattern = node.getPatternString()
        self.meanStep = node.meanStep
        self.medianStep = node.medianStep

    def json_default_dump(self) -> dict:
        return {
            "node id": self.nid,
            "event_attribute": self.value,
            "Pattern": self.pattern,
            "value": self.seqCount,
            "median_index": self.medianStep,
            "average_index": self.meanStep
        }


class Links:

    def __init__(self, node1, node2, count):
        self.source = node1
        self.target = node2
        self.count = count

    def json_default_dump(self) -> dict:
        return {
            "source": self.source,
            "target": self.target,
            "count": self.count
        }


class Graph():

    def __init__(self):
        self.links = []  # defaultdict(set)
        self.nodes = []

    # def add(self, node1, node2, count):
    #    self.links.append(Links(node1,node2, count))
        # self.links[node2].add(node1)

    def json_default_dump(self) -> dict:
        return {
            "nodes": self.nodes,
            "links": self.links

        }

    def json_serialize(self) -> None:

        json.dumps(self,  indent=4, default=Graph.json_serialize_dump)

    @staticmethod
    def json_serialize_dump(obj):

        if hasattr(obj, "json_default_dump"):

            return obj.json_default_dump()
        if isinstance(obj, set):
            return list(obj)
        return None  # obj.__dict__

    def print_graph(self):
        for node in self.nodes:
            print(node.nid)
