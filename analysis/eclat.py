"""
    Standard Eclat Algorithm
"""
import pandas as pd

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

    def __str__(self, move = 0, mainBranch = False):
        string = "| " * move + " + Node : {} - Count : {} \n".format(self.name, self.count)
        for child in sorted(self.children, key = lambda c: c.count)[::-1]:
            string += child.__str__(move + 1, mainBranch)
            if mainBranch:
                # Main branch only look at the first child
                break
        return string

def eclat_rec(data, features, keysToExplore, minCount = 1):
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
        
        if count >= minCount:
            newNode = Node(name, count)
            for i in range(lenKeys - 1):
                # Discover all the data that as the current feature
                newNode.addChild(eclat_rec(data[na], features, keysToExplore[i+1:], minCount))
            return newNode
    return None

def eclat(data, features = None, minCount = 1):
    """
        Eclat algorithm

        Arguments:
            data {pd DataFrame} -- Data
            features {None / List / Dict} -- Features to explore
                If None -> All features in data
                If List -> Only the one in the list (has to be present in data)
                If Dict -> Keys are used has node and values has to be list of features present in data
    """
    assert minCount >= 1
    assert minCount <= len(data), "Cut {} has to be lower than the number of datapoints {}".format(minCount, len(data))
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
        result.addChild(eclat_rec(data, features, keys[i:], minCount))

    return result

def eclat_multiple_files(data_list, features = None, minCount = 1):
    """
        In the case of multiple files (for instance time series)
        For which you want to check the overlapping features
        
        Arguments:
            data_list {List data structure} -- Different time series
        
        Keyword Arguments:
            features {Dict / List / None} -- Features to explore
    """
    featured_data = {}
    for i, d in enumerate(data_list):
        featured_data[i] = {feat: d[feat].notna().mean() for feat in d.columns}
    return eclat(pd.DataFrame.from_dict(featured_data, orient='index'), features, minCount)