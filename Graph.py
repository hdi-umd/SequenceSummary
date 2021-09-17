""" Creates the RawNode, Links and Graph class."""

import json

from itertools import count, chain, groupby


class RawNode:
    """RawNode contains selected attributes from Node class for json conversion."""
    _ids = count(0)

    def __init__(self, node=None):
        if node:
            self.nid = node.nid
            self.seqCount = node.seqCount
            self.value = node.value
            self.pattern = node.getPatternString()
            self.meanStep = node.meanStep
            self.medianStep = node.medianStep
            self.parent = node.parent
        self.rightLinks = []
        self.leftLinks = []

    def jsonDefaultDump(self) -> dict:
        """creates the Json format output for the class RawNode."""
        return {
            "id": self.nid,
            "event_attribute": self.value,
            "Pattern": self.pattern,
            "value": self.seqCount,
            "median_index": self.medianStep,
            "average_index": self.meanStep
        }

    @staticmethod
    def jsonSerializeDump(obj):
        """static method to call jsonDefaultDump on all custom objects"""
        if hasattr(obj, "jsonDefaultDump"):
            print("default dump")
            return obj.jsonDefaultDump()

        return None  # obj.__dict__

    def printNode(self):
        """ Prints details for a node."""
        print(f'node {self.nid}, value {self.value}, Pattern {self.pattern}, \
        meanStep {self.meanStep} seqcount {self.seqCount}, right {[x.source.nid for x in self.rightLinks]}, \
        left {[x.target.nid for x in self.leftLinks]}')

    @staticmethod
    def printNodes(nodeList):
        """Print all nodes in the list."""
        for node in nodeList:
            node.printNode()

    @staticmethod
    def merge(nodeList):
        """Merge all the nodes in nodeList into a single node."""
        print(f'Nodes {nodeList}')
        node = RawNode()
        node.nid = min(x.nid for x in nodeList)
        node.value = nodeList[0].value
        node.seqCount = sum(nodes.seqCount for nodes in nodeList)
        node.pattern = "\n".join(nodes.pattern for nodes in nodeList)
        node.meanStep = sum(nodes.meanStep for nodes in nodeList)/len(nodeList)
        node.medianStep = sum(
            nodes.medianStep for nodes in nodeList)/len(nodeList)
        return node


class Links:
    """Links class contains information regarding which node is connected to which one"""

    def __init__(self, node1, node2, cnt):
        self.source = node1
        self.target = node2
        self.count = cnt

    def jsonDefaultDump(self) -> dict:
        """creates the Json format output for the class Links."""
        return {
            "source": self.source.nid,
            "target": self.target.nid,
            "count": self.count
        }


class Graph:
    """Graph class consusts of Links and Nodes."""

    def __init__(self):
        self.links = []  # defaultdict(set)
        self.nodes = []
        self.linkAdj = {}


    def jsonDefaultDump(self) -> dict:
        """creates the Json format output for the class Graph."""
        return {
            "nodes": self.nodes,
            "links": self.links

        }

    def jsonSerialize(self) -> None:
        """Default JSON serializer"""
        json.dumps(self, indent=4, default=Graph.jsonSerializeDump)

    @staticmethod
    def jsonSerializeDump(obj):
        """static method to call jsonDefaultDump on all custom objects"""
        if hasattr(obj, "jsonDefaultDump"):

            return obj.jsonDefaultDump()
        if isinstance(obj, set):
            return list(obj)
        return None  # obj.__dict__

    def printGraph(self):
        """Print the node ids."""
        for i, node in enumerate(self.nodes):
            print(f'node {node.nid}, index {i}')
        for i, link in enumerate(self.links):
            print(f'links {link.source} {link.target}, index {i}')

    def detectCycles(self):
        """Detect if two incoming nodes has same ancestor."""

        for node in self.nodes:
            if len(node.leftLinks) > 1:
                rightNodes = [lnk.source for lnk in node.leftLinks]
                parentList = []
                for candidate in rightNodes:
                    parentList.append([elem.nid for elem in candidate.parent])

                for i, first in enumerate(parentList):
                    for j, second in enumerate(parentList[i+1:]):
                        common = list(set(first) & set(second))
                        if len(common) > 1 or common[0] != 1:
                            if rightNodes[i].seqCount > rightNodes[i+1+j].seqCount:
                                node.leftLinks[i].count -= node.leftLinks[i+1+j].count
                            else:
                                node.leftLinks[i+1+j].count -= node.leftLinks[i].count

    def createLinks(self):
        """ Create links between nodes."""
        print([x.value for x in self.nodes])
        for _, conn in enumerate(self.linkAdj):
            leftNode = [x for x in self.nodes if x.nid == conn][0]
            for _, right in enumerate(self.linkAdj[conn]):
                rightNode = [x for x in self.nodes if x.nid == right][0]
                link = Links(leftNode, rightNode, self.linkAdj[conn][right])
                self.links.append(link)
                leftNode.rightLinks.append(link)
                rightNode.leftLinks.append(link)


    def bundle(self):
        """Bundle nodes."""
        RawNode.printNodes(self.nodes)
        delNodeIndices = []
        uniqueValue = list(set([x.value for x in self.nodes]))
        print(uniqueValue)

        bundleList = []
        merged = []  # list of nodes in merge
        for node in self.nodes:
            if len(node.rightLinks) > 1 or len(node.leftLinks) > 1:
                bundleList.append(node)
        print(f'bundle {[b.nid for b in bundleList]}')
        print(f'Heer {len(bundleList)}')
        while bundleList:
            currentBundle = max(bundleList, key=lambda x: x.nid)
            print(f'nid {currentBundle.nid}')
            if currentBundle.nid in merged:
                continue
            groups = []
            if len(currentBundle.leftLinks) > 1:
                lNodes = [left.source for left in currentBundle.leftLinks]
                if lNodes:
                    groups.extend(
                        self.groupMergeableNodes(lNodes, uniqueValue))
                    print(f'left links exist {groups}')
            if len(currentBundle.rightLinks) > 1:
                rNodes = [right.target for right in currentBundle.rightLinks]
                if rNodes:
                    groups.extend(
                        self.groupMergeableNodes(rNodes, uniqueValue))
                    print(f'right links exist {groups}')

            if groups:
                print(f'groups {groups}')
                for grp in groups:
                    delNodeIndices.append(self.nodes.index(n) for n in grp)
                    print(f'groyp {len(grp)}')
                    newNode = self.mergeNodes(grp, merged)
                    if len(newNode.rightLinks) > 1 or len(newNode.leftLinks) > 1:
                        bundleList.append(newNode)

            ind = bundleList.index(currentBundle)
            del bundleList[ind]
        for idx in sorted(delNodeIndices, reverse=True):
            del self.nodes[idx]

    def mergeNodes(self, nodes, isMerged):
        """ Merge the links into a single node"""
        print(f'Nodesss {nodes}')
        newNode = RawNode.merge(nodes)
        newNode.nid = self.nodes[-1].nid+1
        self.nodes.append(newNode)
        isMerged.extend(node.nid for node in nodes)
        deleteLinks = []

        rightLinkCollection = list(
            chain.from_iterable(n.rightLinks for n in nodes))
        for _, igroup in groupby(rightLinkCollection, lambda x: x.target.nid):
            target = igroup[0].target
            print(f'target {target}')
            target.leftLinks = [
                target.leftLinks for target in igroup if target.source not in isMerged]
            deleteLinks.extend(
                target.leftLinks for target in igroup if target.source in isMerged)
            link = Links(newNode, igroup[0].target,
                         sum(lnk.count for lnk in igroup))
            target.leftLinks.append(link)
            self.links.append(link)
            newNode.rightLinks.extend(target.leftLinks)

        leftLinkCollection = list(
            chain.from_iterable(n.leftLinks for n in nodes))
        for _, igroup in groupby(leftLinkCollection, lambda x: x.source.nid):
            source = igroup[0].source
            print(f'source {source}')
            source.rightLinks = [
                source.rightLinks for source in igroup if source.target not in isMerged]
            deleteLinks.extend(
                source.rightLinks for source in igroup if source.target in isMerged)
            link = Links(igroup[0].source, newNode,
                         sum(lnk.count for lnk in igroup))
            source.rightLinks.append(link)
            self.links.append(link)
            newNode.leftLinks.extend(source.rightLinks)
        deleteLinkIndices = []
        for link in deleteLinks:
            deleteLinkIndices.append(self.links.index(deleteLinks))
        deleteLinkIndices = list(set(deleteLinkIndices))
        for idx in sorted(deleteLinkIndices, reverse=True):
            del self.links[idx]

        return newNode

    def groupMergeableNodes(self, nodes, uniqueValue):
        """Group nodes and merge."""

        subGroups = []
        for val in uniqueValue:
            subGroup = []
            checkMultiple = [node for node in nodes if node.nid == val]
            if len(checkMultiple) > 1:
                for index, node in checkMultiple:
                    linkExists = []  # Check if link exists within same items of a group
                    for rightNode in checkMultiple[index+1]:
                        linkExists.append([link for link in self.links
                                           if (link.source == node and link.target == rightNode)
                                           or (link.target == node and link.source == rightNode)])
                        if linkExists:
                            break
                    if not linkExists:  # This node has no connection to own sub group
                        subGroup.append(node)
            if subGroup:
                subGroups.append(subGroup)
        return subGroups

    @staticmethod
    def assembleGraphs(graphList):
        """Create a single grapg given a list of graph"""
        newGraph = Graph()
        for graph in graphList:
            newGraph.links.extend(graph.links)
            newGraph.nodes.extend(graph.nodes)
        return newGraph
