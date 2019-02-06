from analysis.eclat import eclat, eclat_multiple_files
from analysis.rendering import buildGraph
import pandas as pd

# Open data
missing = pd.read_csv("examples/data/missing.csv", index_col="index")
no_missing = pd.read_csv("examples/data/no_missing.csv", index_col="index")
subset = pd.read_csv("examples/data/subset_features.csv", index_col="index")

# Computes graph on features
features = eclat(missing)
print(features)
buildGraph(features).render('examples/full')

# Merge some features
# Can be useful if some data are redundant
features = eclat(missing, {"f1":["f1", "f1_1"], "f2": ["f2", "f2_2"], "f3": ["f3"]})
print(features)
buildGraph(features).render('examples/match')

# Only look at a subset
features = eclat(missing, ["f1", "f2", "f3"])
print(features)
buildGraph(features).render('examples/subset')

# Two files
features = eclat_multiple_files([missing, no_missing, subset])
print(features)
buildGraph(features).render('examples/multiple_files')

# Only principal branch
buildGraph(features, mainBranch = True, minCount = 3).render('examples/multiple_files_main_branch')
print(features.__str__(mainBranch = True, minCount = 3))