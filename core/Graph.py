"""Creates the RawNode, Links and Graph class."""

import json

from itertools import count, chain, groupby
from statistics import mean
from core.Pattern import Pattern


class RawNode:
    """RawNode contains selected attributes from Node class for json conversion."""

    _ids = count(1)

    def __init__(self, node=None, pos=0, isCoreflow=0):
        if node:
            self.createFromNode(node, isCoreflow)
        else:
            self.nid = next(self._ids)
            self.seqCount = 0

            self.value = 0
            self.keyevts = []
            self.pattern = -1
            self.parent = []
            self.sequences = []
            self.attr = ""
            self.meanStep = -1
            self.medianStep = -1
        self.evtCount = 0
        self.pos = pos
        self.rightLinks = []
        self.leftLinks = []

    def createFromNode(self, node, coreFlow):
        """Create RawNode from Node object."""
        self.nid = node.nid
        self.seqCount = node.seqCount
        self.value = node.value
        self.keyevts = node.keyevts
        self.pattern = node.getPatternString()
        self.parent = node.parent
        self.sequences = node.sequences
        self.attr = node.attr
        if coreFlow:
            self.meanStep = node.meanStep
            self.medianStep = node.medianStep
        else:
            self.meanStep = -1
            self.medianStep = -1

    def jsonDefaultDump(self) -> dict:
        """creates the Json format output for the class RawNode."""
        return {
            "id": self.nid,
            "event_attribute": self.value,
            "pattern": "P" + str(self.pattern),
            "value": str(self.seqCount),
            "value_event": str(self.evtCount),
            "median_index": self.medianStep,
            "average_index": self.meanStep,
            "sequences": [s._id for s in self.sequences],
        }

    @staticmethod
    def jsonSerializeDump(obj):
        """static method to call jsonDefaultDump on all custom objects"""
        if hasattr(obj, "jsonDefaultDump"):
            return obj.jsonDefaultDump()

        return None  # obj.__dict__

    def printNode(self):
        """Prints details for a node."""
        print(
            f"node {self.nid}, value {self.value}, Pattern {self.pattern}, \
        meanStep {self.meanStep} seqcount {self.seqCount}, right {[x.target.nid for x in self.rightLinks]}, \
        left {[x.source.nid for x in self.leftLinks]}"
        )

    @staticmethod
    def printNodes(nodeList):
        """Print all nodes in the list."""
        for node in nodeList:
            node.printNode()

    @staticmethod
    def merge(nodeList, allNodes):
        """Merge all the nodes in nodeList into a single node."""
        node = RawNode()
        node.nid = max(x.nid for x in allNodes) + 1
        node.value = nodeList[0].value
        node.seqCount = sum(nodes.seqCount for nodes in nodeList)
        node.pattern = "\t".join(nodes.pattern for nodes in nodeList)
        node.meanStep = sum(nodes.meanStep for nodes in nodeList) / len(nodeList)
        node.medianStep = sum(nodes.medianStep for nodes in nodeList) / len(nodeList)
        return node

    def calcPositions(self, matchAll):
        """Computes cumulative mean and median positions and path lengths of
        key events for the given attribute.
        """

        if not self.keyevts or self.nid == 1:
            # rootNode
            return 0, 0

        medians, means = Pattern.getStats(
            self.keyevts[: self.pos + 1], self.sequences, self.attr, matchAll
        )

        # if not matchAll:
        #     return sum(means), sum(medians)

        return means[-1], medians[-1]

    def calcPositionsGenericNode(self, nodeList, matchAll):
        """Computes cumulative mean and median positions and path lengths of
        key events for the given attribute.
        """

        mean, median = self.calcPositions(matchAll)

        if len(self.parent) > 1:
            parentNid = self.parent[self.pos].nid
            rawParent = [x for x in nodeList if x.nid == parentNid][0]
            # As root is also in parent
            self.meanStep = mean + rawParent.meanStep
            self.medianStep = median + rawParent.medianStep
        else:
            self.meanStep = mean
            self.medianStep = median

    def calcPositionsExitNode(self, nodeList):
        """Computes cumulative mean and median positions and path lengths of
        key events for the given attribute.
        """
        median, mean = Pattern.getStatsEnd(self.keyevts, self.sequences, self.attr)
        parentNid = self.parent[-1].nid
        rawParent = [x for x in nodeList if x.nid == parentNid][0]
        self.meanStep = rawParent.meanStep + mean
        self.medianStep = rawParent.medianStep + median

        return mean

    def getEventValue(self):
        """Get How many sequences this specific event has."""
        self.evtCount = int(self.seqCount)
        if self.value != "_Start" and self.value != "_Exit":
            for seq in self.sequences:
                pos = Pattern.getPositions(
                    self.keyevts[: self.pos + 1], seq.getHashList(self.attr)
                )
                if pos[-1] == -1:
                    self.evtCount -= 1

    @staticmethod
    def resetCounter():
        """resets node counter."""
        RawNode._ids = count(1)


class Links:
    """Links class contains information regarding which node is connected to which one"""

    def __init__(self, node1, node2, cnt, LinkLen=0):
        self.source = node1
        self.target = node2
        self.count = cnt
        self.length = LinkLen

    def jsonDefaultDump(self) -> dict:
        """creates the Json format output for the class Links."""
        return {
            "source": self.source.nid,
            "target": self.target.nid,
            "count": self.count,
            "length": self.length,
        }

    def calcLinkLength(self):
        """Calculate link lengths for all links in graph."""
        means = []
        srcNode = self.source
        targetNode = self.target
        seqs = []
        for seq in targetNode.sequences:
            if seq in srcNode.sequences:
                seqs.append(seq)

        if targetNode.value == "_Exit":
            trailingSteps = [0] * len(seqs)
            for i, path in enumerate(seqs):
                pos = Pattern.getPositions(
                    targetNode.keyevts, path.getHashList(targetNode.attr)
                )
                # the difference between the last event in thesequence and the last key event

                # if no sequence, Start-> Exit
                trailingSteps[i] = len(path.events) - (pos[-1] - 1 if pos else 0)

            trailStepSum = sum(trailingSteps)

            if trailingSteps:
                mean = trailStepSum / len(trailingSteps)
            else:
                mean = 0

            self.length = mean

        else:
            _medians, means = Pattern.getStats(
                targetNode.keyevts[: targetNode.pos + 1], seqs, targetNode.attr
            )

            self.length = means[-1]


class Graph:
    """Graph class consusts of Links and Nodes."""

    def __init__(self):
        self.links = []  # defaultdict(set)
        self.nodes = []
        self.linkAdj = {}

    def jsonDefaultDump(self) -> dict:
        """creates the Json format output for the class Graph."""
        return {"nodes": self.nodes, "links": self.links}

    def jsonSerialize(self) -> None:
        """Default JSON serializer"""
        json.dumps(self, indent=4, default=Graph.jsonSerializeDump)

    def calcPositionsNode(self, matchAll=True):
        """Calculate mean and median node positions."""
        for node in self.nodes:
            if node.value == "_Exit":
                node.calcPositionsExitNode(self.nodes)
            else:
                node.calcPositionsGenericNode(self.nodes, matchAll)

    def setMaxNodePred(self, node):
        """Recursively get max predecessor."""
        candPred = [x.source for x in node.leftLinks]
        for cand in candPred:
            if cand.meanStep < 0:
                self.setMaxNodePred(cand)
        candPred = sorted(candPred, key=lambda x: x.meanStep, reverse=True)
        mean, median = node.calcPositions()
        node.meanStep = candPred[0].meanStep + mean
        node.medianStep = candPred[0].medianStep + median

    def calcPositionsNodeMaxPredecessor(self):
        """Calculate mean and median node positions based on max predecessor."""
        startNode = [x for x in self.nodes if x.nid == 1][0]
        startNode.meanStep = 0
        startNode.medianStep = 0
        for node in self.nodes:
            if node.value == "_Exit":
                node.calcPositionsExitNode(self.nodes)
            elif node.meanStep < 0:
                self.setMaxNodePred(node)

    def calcLengthsLink(self):
        """Calculate average length for links."""
        self.links = sorted(
            self.links, key=lambda x: (x.source.nid, x.target.nid, x.count)
        )
        for link in self.links:
            link.calcLinkLength()

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
            print(f"node {node.nid}, index {i}")
        for i, link in enumerate(self.links):
            print(f"links {link.source} {link.target}, index {i}")

    def detectCycles(self):
        """Detect if two incoming nodes has same ancestor."""
        for node in self.nodes:
            if len(node.leftLinks) > 1:
                print(f"node {node.nid} has multiple parents")
                leftNodes = [lnk.source for lnk in node.leftLinks]
                parentList = []
                for candidate in leftNodes:
                    parentList.append(
                        [
                            elem.nid
                            for elem in candidate.parent
                            # if elem.nid != node.nid
                        ]  # remove self from parent
                    )
                for i, first in enumerate(parentList):
                    for j, second in enumerate(parentList[i + 1 :]):
                        common = list(set(first) & set(second))
                        if len(common) > 1 or common[0] != 1:
                            seq_ids_src1 = [
                                s._id for s in node.leftLinks[i].source.sequences
                            ]
                            seq_ids_src2 = [
                                s._id
                                for s in node.leftLinks[i + 1 + j].source.sequences
                            ]
                            # Find common sequences
                            common_seq_ids = set(seq_ids_src1) & set(seq_ids_src2)

                            if common_seq_ids:
                                # Reduce the count of leftNodes[i] by the number of common sequences
                                node.leftLinks[i].count -= len(common_seq_ids)
                                node.leftLinks[i].count = abs(node.leftLinks[i].count)
                            # if leftNodes[i].seqCount > leftNodes[i + 1 + j].seqCount:

                            #     node.leftLinks[i].count -= node.leftLinks[
                            #         i + 1 + j
                            #     ].count
                            #     node.leftLinks[i].count = abs(node.leftLinks[i].count)

                            # else:
                            #     node.leftLinks[i + 1 + j].count -= node.leftLinks[
                            #         i
                            #     ].count
                            #     node.leftLinks[i + 1 + j].count = abs(
                            #         node.leftLinks[i + 1 + j].count
                            #     )

    def createLinks(self):
        """Create links between nodes."""
        # print([x.value for x in self.nodes])
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
        uniqueValue = list({x.value for x in self.nodes})

        bundleList = []
        merged = []  # list of nodes in merge
        for node in self.nodes:
            if len(node.rightLinks) > 1 or len(node.leftLinks) > 1:
                bundleList.append(node)

        while bundleList:
            currentBundle = max(bundleList, key=lambda x: x.nid)
            if currentBundle.nid in merged:
                ind = bundleList.index(currentBundle)
                print(f"Deleting {currentBundle.nid} from index {ind}")
                del bundleList[ind]
                continue
            groups = []
            if len(currentBundle.leftLinks) > 1:
                lNodes = [left.source for left in currentBundle.leftLinks]
                if lNodes:
                    groups.extend(self.groupMergeableNodes(lNodes, uniqueValue))
            if len(currentBundle.rightLinks) > 1:
                rNodes = [right.target for right in currentBundle.rightLinks]
                if rNodes:
                    groups.extend(self.groupMergeableNodes(rNodes, uniqueValue))

            if groups:
                for grp in groups:
                    delNodeIndices.extend([x.nid for x in grp])
                    newNode = self.mergeNodes(grp, merged)
                    if len(newNode.rightLinks) > 1 or len(newNode.leftLinks) > 1:
                        bundleList.append(newNode)

            ind = bundleList.index(currentBundle)
            del bundleList[ind]
            print(f"Deleting {currentBundle.nid} from index {ind}")

        delNodeIndices = sorted(delNodeIndices, reverse=True)
        self.nodes = [x for x in self.nodes if x.nid not in delNodeIndices]
        self.links = [
            x
            for x in self.links
            if x.source.nid not in delNodeIndices and x.target.nid not in delNodeIndices
        ]
        # for idx in sorted(delNodeIndices, reverse=True):
        #     self.nodes.remove()

    def mergeNodes(self, nodes, isMerged):
        """Merge the links into a single node"""
        newNode = RawNode.merge(nodes, self.nodes)
        # newNode.nid = self.nodes[-1].nid+1
        self.nodes.append(newNode)
        isMerged.extend(node.nid for node in nodes)
        # deleteLinks = []

        rightLinkCollection = list(chain.from_iterable(n.rightLinks for n in nodes))
        rightLinkCollection = sorted(rightLinkCollection, key=lambda x: x.target.nid)
        for _, igroupgen in groupby(rightLinkCollection, lambda x: x.target.nid):
            igroup = list(igroupgen)
            target = igroup[0].target
            target.leftLinks = [
                x.target.leftLinks[:] for x in igroup if x.source.nid not in isMerged
            ]  # keep non merging links intact
            link = Links(
                newNode,
                target,
                sum(lnk.count for lnk in igroup),
                mean(lnk.length for lnk in igroup),
            )
            target.leftLinks.append(link)
            self.links.append(link)

            newNode.rightLinks.extend(target.leftLinks)

        leftLinkCollection = list(chain.from_iterable(n.leftLinks for n in nodes))
        leftLinkCollection = sorted(leftLinkCollection, key=lambda x: x.source.nid)

        for _, igroupgen in groupby(leftLinkCollection, lambda x: x.source.nid):
            igroup = list(igroupgen)
            source = igroup[0].source
            # item for sublist in deleteLinks for item in sublist
            source.rightLinks = [
                x.source.rightLinks[:] for x in igroup if x.target.nid not in isMerged
            ]

            link = Links(
                source,
                newNode,
                sum(lnk.count for lnk in igroup),
                mean(lnk.length for lnk in igroup),
            )
            source.rightLinks.append(link)
            self.links.append(link)
            # link.calcLinkLength()
            newNode.leftLinks.extend(source.rightLinks)

        deleteLinkIndices = []
        # deleteLinks = [item for sublist in deleteLinks for item in sublist]
        # for delink in deleteLinks:
        #     deleteLinkIndices.append(self.links.index(delink))
        # deleteLinkIndices = list(set(deleteLinkIndices))
        # for idx in sorted(deleteLinkIndices, reverse=True):
        #     del self.links[idx]
        # self.links = [x for x in self.links if x not in deleteLinks]
        return newNode

    def groupMergeableNodes(self, nodes, uniqueValue):
        """Group nodes and merge."""
        subGroups = []
        for val in uniqueValue:
            subGroup = []
            checkMultiple = [node for node in nodes if node.value == val]
            if len(checkMultiple) > 1:
                for index, node in enumerate(checkMultiple):
                    linkExists = []  # Check if link exists within same items of a group
                    parentNid = [x.nid for x in node.parent]
                    flag = True
                    for idx, rightNode in enumerate(checkMultiple):
                        if index != idx:
                            linkExists.extend(
                                [
                                    link
                                    for link in self.links
                                    if (
                                        link.source == node and link.target == rightNode
                                    )
                                    or (
                                        link.target == node and link.source == rightNode
                                    )
                                ]
                            )
                            if linkExists:
                                flag = False
                                break
                            if rightNode.nid in parentNid:
                                flag = False
                                break

                    if flag:  # This node has no connection to own sub group
                        subGroup.append(node)

            if subGroup:
                subGroups.append(subGroup)
        # for subGroup in subGroups:
        return subGroups

    def getEventValueForNodes(self):
        """For every node in the graph, see how many seuqences it is present in."""
        for node in self.nodes:
            node.getEventValue()

    @staticmethod
    def assembleGraphs(graphList):
        """Create a single graph given a list of graph"""
        newGraph = Graph()
        for graph in graphList:
            newGraph.links.extend(graph.links)
            newGraph.nodes.extend(graph.nodes)
        return newGraph
