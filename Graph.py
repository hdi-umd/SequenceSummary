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
            "node_id": self.nid,
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
        meanStep {self.meanStep} seqcount {self.seqCount} pos {self.position}')

    @staticmethod
    def printNodes(nodeList):
        """Print all nodes in the list."""
        for node in nodeList:
            node.printNode()

    @staticmethod
    def merge(nodeList):
        """Merge all the nodes in nodeList into a single node."""
        node = RawNode()
        node.nid = min(x.nid for x in nodeList)
        node.value = nodeList[0].value
        node.seqCount = sum(nodes.seqCount for nodes in nodeList)
        node.pattern = "\n".join(nodes.pattern for nodes in nodeList)
        node.meanStep = sum(nodes.meanStep for nodes in nodeList)/len(nodeList)
        node.medianStep = sum(nodes.medianStep for nodes in nodeList)/len(nodeList)
        return node



class Links:
    """Links class contains information regarding which node is connected to which one"""

    def __init__(self, node1, node2, count):
        self.source = node1
        self.target = node2
        self.count = count

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


    def collapseNode(self):
        """Gets rid of extra nrange(lenodes and links"""
        RawNode.printNodes(self.nodes)
        delNodes = []
        delLinks = []
        newLinks = []

        for node in self.nodes:
            if node.value == -2:
                # ideally. there should be one source
                linkArrSrc = [
                    x for x in self.links if x.target == node.nid]
                print(f'source1 {[lnk.source for lnk in linkArrSrc]}')
                print(f'target1 {[lnk.target for lnk in linkArrSrc]}')
                # if len(linkArrSrc) == 1:
                #    linkArrSrc = linkArrSrc[0]

                linkArrTrgt = [
                    x for x in self.links if x.source == node.nid]
                print(f'source2 {[lnk.source for lnk in linkArrTrgt]}')
                print(f'target2 {[lnk.target for lnk in linkArrTrgt]}')

                if len(linkArrSrc) > 1 and len(linkArrTrgt) > 1:
                    print(
                        f'len source {len(linkArrSrc)}, len target {len(linkArrTrgt)}')
                    # continue
                    # [x.printNode() for x in self.nodes if x.node_id in ]
                    raise ValueError('multiple source and target')

                for j, _ in enumerate(linkArrSrc):
                    for i, _ in enumerate(linkArrTrgt):
                        newLinks.append(
                            Links(linkArrSrc[j].source,
                                  linkArrTrgt[i].target, linkArrTrgt[i].count))
                        delLinks.append(linkArrTrgt[i])
                    delLinks.append(linkArrSrc[j])

                delNodes.append(node)

        #print(f'Node delete {[node. nid for node in delNodes]}')
        # print(
        #    f'Link delete {[((link.source, link.target)) for link in delLinks]}')

        # print(self.printGraph())

        delNodeIndices = [self.nodes.index(x) for x in delNodes]
        delLinkIndices = [self.links.index(x) for x in delLinks]

        #print(f'Node delete {delNodeIndices}')
        #print(f'Link delete {delLinkIndices}')
        print(delLinkIndices)
        for idx in sorted(delNodeIndices, reverse=True):
            del self.nodes[idx]

        # To sure uniqueness we use list(set) operation here
        for idx in sorted(list(set(delLinkIndices)), reverse=True):
            print(f'index {idx}')
            del self.links[idx]

        self.links.extend(newLinks)

    def leftMost(self, node):
        current = node
        
        while(current):
            if current.before:
                break
            print(f'current {current}')
            current = current.before

        return current

    def findSuccessor(self, rootNode, node):

        if node.after:
                return [self.leftMost(node.after[i]) for i in range(len(node.after))]
        successor = node.parent
        while(successor):
            if successor not in node.after:
                break
            node = successor
            successor = node.parent
        return successor

    def allignNodes(self):
        """ Align  nodes according to their position in sequence. """
        """ rootNode = self.nodes[0]
        for node in self.nodes:
            successor = self.findSuccessor(rootNode, node)
            print(f'nodes {[node.nid]} successor {successor}')
            print(successor)
            linkExists = [x for x in self.links if x.source ==
                          node.nid and x.target == successor.nid]

            if not linkExists:
                self.links.append(Links(node.nid, successor.nid, 0)) """

        print("nodes sorted")
        node = sorted(self.nodes, key=lambda x: x.position)
        RawNode.printNodes(node)

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

    def createLinks(self):
        """ Create links between nodes."""
        print([x.value for x in self.nodes])
        for i, conn in enumerate(self.linkAdj):
            leftNode = [x for x in self.nodes if x.nid == conn][0]
            print(f'LeftNode {leftNode.value}')
            print(f'links {self.linkAdj[conn]}')
            for j, right in enumerate(self.linkAdj[conn]):
                print(f'Connection {self.linkAdj[conn][right]}')
                rightNode = [x for x in self.nodes if x.nid == right][0]
                print(f'RightNode {rightNode.value}')
                link = Links(leftNode, rightNode, self.linkAdj[conn][right])
                self.links.append(link)
                leftNode.rightLinks.append(link)
                rightNode.leftLinks.append(link)
        #self.printGraph()

    def bundle(self):
        """Bundle nodes."""
        uniqueValue = list(set([x.value for x in self.nodes]))
        print(uniqueValue)

        bundleList = []
        merged = [] #list of nodes in merge
        for node in self.nodes:
            if len(node.rightLinks) > 1 or len(node.leftLinks) > 1:
                bundleList.append(node)
        print(f'Heer {len(bundleList)}')
        while bundleList:
            currentBundle = max(bundleList, key=lambda x: x.nid)
            if currentBundle.nid in merged:
                continue
            groups = []
            if len(currentBundle.leftLinks) > 1:
                lNodes = [left.source for left in currentBundle.leftLinks]
                groups = groups.extend(self.groupMergeableNodes(lNodes, uniqueValue))

            if len(currentBundle.rightLinks) > 1:
                rNodes = [right.target for right in currentBundle.rightLinks]
                groups = groups.extend(self.groupMergeableNodes(rNodes, uniqueValue))

            if groups:
                for grp in groups:
                    newNodes = self.mergeNodes(grp, merged)
                    
            ind = bundleList.index(currentBundle)
            del bundleList[ind]
        

        #currentSeq = max(seqs, key=lambda x: x.seqCount)

    def mergeNodes(self, nodes, isMerged):
        """ Merge the links into a single node"""
        newNode = RawNode.merge(nodes)
        newNode.nid = self.nodes[-1].nid+1
        self.nodes.append(newNode)
        isMerged.extend(node.nid for node in nodes)
        deleteLinks = []

        rightLinkCollection = list(chain.from_iterable(n.rightLinks for n in nodes))
        for _, igroup in groupby(rightLinkCollection, lambda x: x.target.nid):
            target = igroup[0].target
            print(f'target {target}')
            target.leftLinks = [target.leftLinks for target in igroup if target.source not in isMerged]
            deleteLinks.extend(target.leftLinks for target in igroup if target.source in isMerged)
            link = Links(newNode, igroup[0].target, sum(lnk.count for lnk in igroup))
            target.leftLinks.append(link)
            self.links.append(link)
            newNode.rightLinks.extend(target.leftLinks)
        
        leftLinkCollection = list(chain.from_iterable(n.leftLinks for n in nodes))
        for _, igroup in groupby(leftLinkCollection, lambda x: x.source.nid):
            source = igroup[0].source
            print(f'source {source}')
            source.rightLinks = [source.rightLinks for source in igroup if source.target not in isMerged]
            deleteLinks.extend(source.rightLinks for source in igroup if source.target in isMerged)
            link = Links(igroup[0].source, newNode, sum(lnk.count for lnk in igroup))
            source.rightLinks.append(link)
            self.links.append(link)
            newNode.leftLinks.extend(source.rightLinks) 


    def groupMergeableNodes(self, nodes, uniqueValue):
        """Group nodes and merge."""
        subGroups = []
        for val in uniqueValue:
            subGroup = []
            checkMultiple = [node for node in nodes if node.nid == val]
            if(len(checkMultiple) > 1):
                for index, node in checkMultiple:
                    linkExists = [] # Check if link exists within same items of a group
                    for rightNode in checkMultiple[index+1]:
                        linkExists.append([link for link in self.links 
                                           if (link.source == node and link.target == rightNode)
                                           or (link.target == node and link.source == rightNode)])
                        if linkExists:
                            break
                    if not linkExists: #This node has no connection to own sub group
                        subGroup.append(node)
            subGroups.append(subGroup)
        return subGroups

