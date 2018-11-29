"""
    Standard Eclat Algorithm
"""

class Node:
    """ 
        Tree structure used for the eclat algorithm
    """

    # Id of the given Node
    idNum = 0

    def __init__(self, name, count):
        """     
            Arguments:
                name {str} -- Name of the feature
                count {int} -- Number of points sharing this feature
                graph {graph object} -- To Display
        """

        self.name = name
        self.count = count
        self.children = []
        self.id = Node.idNum
        Node.idNum += 1

    def addChild(self, child):
        if child is not None:
            self.children.append(child)

    def __str__(self, move = 0):
        string = "| " * move + " + Node : {} - Count : {} \n".format(self.name, self.count)
        for child in self.children:
            string += child.__str__(move + 1)
        return string

def eclat_rec(data, features, keysToExplore):
    """
        Recursive Eclat Algorithm

        Arguments:
            keysToExplore {List} -- List of features to explore

        Returns:
            Node concerning the current feature
    """
    lenKeys = len(keysToExplore)
    if lenKeys > 0:
        # Select the first element
        name = keysToExplore[0]

        # Compute for each datapoint if any is not na in list of features
        na = data.notna()[features[name]].any(axis = 1)
        count = na.sum()
        
        # Select index
        indexToExplore = data[na].index

        if count > 0:
            newNode = Node(name, count)
            for i in range(lenKeys - 1):
                # Discover all the data that as the current feature
                newNode.addChild(eclat_rec(data[na], features, keysToExplore[i+1:]))
            return newNode
    return None

def eclat(data, features = None):
    """
        Eclat algorithm

        Arguments:
            data {pd DataFrame} -- Data
            features {None / List / Dict} -- Feautres to explore
                If None -> All features in data
                If List -> Only the one in the list (has to be present in data)
                If Dict -> Keys are used has node and values has to be list of features present in data
    """
    if features is None:
        features = data.columns
        features = {f:[f] for f in features}
    elif type(features) == list:
        for f in features:
            assert f in data.columns, "Feature {} not present in data".format(f)
        features = {f:[f] for f in features}
    else:
        for _, feat in features.items():
            for f in feat:
                assert f in data.columns, "Feature {} not present in data".format(f)

    keys = list(features.keys())
    result = Node("Data", len(data))
    for i in range(len(features)):
        result.addChild(eclat_rec(data, features, keys[i:]))

    return result