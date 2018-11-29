from analysis.eclat import eclat
from analysis.rendering import buildGraph
import pandas as pd

# Open data
data = pd.read_csv("examples/data/missing.csv", index_col="index")

# Computes graph on features
features = eclat(data)
print(features)
buildGraph(features).render('examples/full')

# Merge some features
# Can be useful if some data are redundant
features = eclat(data, {"f1":["f1", "f1_1"], "f2": ["f2", "f2_2"], "f3": ["f3"]})
print(features)
buildGraph(features).render('examples/match')

# Only look at a subset
features = eclat(data, ["f1", "f2", "f3"])
print(features)
buildGraph(features).render('examples/subset')