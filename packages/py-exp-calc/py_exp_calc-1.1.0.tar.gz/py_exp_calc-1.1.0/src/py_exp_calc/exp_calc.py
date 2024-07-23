"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = py_exp_calc.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import warnings
import sys
import copy
import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.spatial import distance_matrix
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import cut_tree
from scipy import stats
import itertools
import statsmodels.api as sm


from py_exp_calc import __version__

__author__ = "seoanezonjic"
__copyright__ = "seoanezonjic"
__license__ = "MIT"



# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from py_exp_calc.skeleton import fib`,
# when using this Python module as a library.


####################################
# LIST OPERATIONS
####################################

# One List operation
####################################

def get_stats_from_list(data): #TODO: think inj a dry version #DONE
  data = np.array(data).reshape((1,len(data)))
  primary_stats = get_primary_stats(data)
  stats = []
  stats.append(['Elements', primary_stats["count"]])
  stats.append(['Elements Non Zero', primary_stats["countNonZero"]])
  stats.append(['Non Zero Density', primary_stats["countNonZero"]/primary_stats["count"]])
  stats.append(['Max', primary_stats["max"]])
  stats.append(['Min', primary_stats["min"]])
  stats.append(['Average', primary_stats["average"]])
  stats.append(['Variance', primary_stats["variance"]])
  stats.append(['Standard Deviation', primary_stats["standardDeviation"]])
  stats.append(['Q1', primary_stats["q1"]])
  stats.append(['Median', primary_stats["median"]])
  stats.append(['Q3', primary_stats["q3"]])
  stats.append(['Min Non Zero', primary_stats["minNonZero"]])
  stats.append(['Average Non Zero', primary_stats["averageNonZero"]])
  stats.append(['Variance Non Zero', primary_stats["varianceNonZero"]])
  stats.append(['Standard Deviation Non Zero', primary_stats["standardDeviationNonZero"]])
  stats.append(['Q1 Non Zero', primary_stats["q1NonZero"]])
  stats.append(['Median Non Zero', primary_stats["medianNonZero"]])
  stats.append(['Q3 Non Zero', primary_stats["q3NonZero"]])
  stats = map(lambda x: [x[0],str(x[1])],stats)
  return stats

def uniq(arr1):
  used = set()      
  return [x for x in arr1 if x not in used and (used.add(x) or True)]

def flatten(arr):
    result = []
    if type(arr) is not list:
        return [arr]
    elif len(arr) == 0: 
        return []
    elif len(arr) == 1: 
        return flatten(arr[0]) 
    elif len(arr) > 1:
        for sub_arr in arr: 
            result += flatten(sub_arr)
        return result

def add_tags(table, tags, keys, default_tag = None):
  tagged_file=[]
  for row in table: 
    record = dig(tags, *tuple([row[key] for key in keys]))
    if record is not None:
      row.append(record)
      tagged_file.append(row)
    elif default_tag:
      row.append(default_tag)
      tagged_file.append(row)
  return tagged_file

# Stats
####################################

def get_test(table, idx_factor, alternative = "two-sided", adj_pval=None, assumptions={"continuos": True, "paired": False}, header = True, binarize_factor = True, parametric = True):
    idx_variable = diff(list(range(0,len(table[0]))), idx_factor)
    header = get_header(table, idx_factor, header, idx_variable)
    stats = []
    for factor in idx_factor:
      for variable in idx_variable:
        table_pair = [[row[index] for index in [factor,variable]] for row in table]
        factor_values = [row[factor] for row in table]
        factor_values = list(set(factor_values))
        if len(factor_values) > 2:
          for factorA, factorB in itertools.combinations(factor_values,2):
            filtered_table_pair = [row for row in table if row[factor] in [factorA, factorB]]
            pvalue = one_hypothesis(table_pair, alternative, assumptions, parametric)
            stats.append([f"{header[factor]}_{factorA}:{factorB}", header[variable], pvalue])
        else:
          pvalue = one_hypothesis(table_pair, alternative, assumptions, parametric)
          stats.append([header[factor], header[variable], pvalue])
    if adj_pval: 
      pvalues =  [row[2] for row in stats]
      adj_pvals = sm.stats.multipletests(pvalues, method=adj_pval, is_sorted=False, returnsorted=False)[1]
      for i in range(len(pvalues)):
        stats[i].append(adj_pvals[i])
    return stats

def get_header(table, idx_factor, header, idx_variable):
    if header:
      header = table.pop(0)
    else:
      header = []
      factor_number = 1
      variable_number = 1
      for i in range(0,len(table[0])):
        if i in idx_factor:
          header.append(f"F{factor_number}")
          factor_number += 1
        if i in idx_variable:
          header.append(f"V{variable_number}")
          variable_number += 1
    return header

def one_hypothesis(table_pair, alternative, assumptions={"continuos": True, "paired": False}, parametric = True):
  # 1) Continuos or not? 2) Paired? 3) Parametric?
  if assumptions["continuos"]:
    factor_values = sorted(list(set([row[0] for row in table_pair])))
    a = [row[1] for row in table_pair if row[0] == factor_values[0]]
    b = [row[1] for row in table_pair if row[0] == factor_values[1]]
    
    if assumptions["paired"]:  
      pvalue = scipy.stats.ttest_rel(a, b, axis=0, nan_policy='propagate', alternative=alternative).pvalue
    else:
      if parametric:
        pvalue = stats.ttest_ind(a, b, axis=0, equal_var=False, 
        nan_policy='propagate',
        alternative=alternative).pvalue
      else:
        pvalue = stats.mannwhitneyu(a, b, alternative=alternative, nan_policy='propagate').pvalue
  else:
    raise Exception("Not implemented yet for categorical variables")
  return pvalue

# Scores
####################################

def get_rank_metrics(scores, ids, pos_selection="worst"):
    ordered_scores = []
    ordered_indexes = np.argsort(scores)  # from smallest to largest
    number_of_all_nodes = len(ids)

    last_val = None
    n_elements = ordered_indexes.shape[0]
    if pos_selection == "best":
      positions = reversed(range(0,n_elements))
    elif pos_selection == "worst":
      positions = range(0,n_elements)

    for pos in positions:
        order_index = ordered_indexes[pos]
        val = scores[order_index]
        node_name = ids[order_index]

        if pos_selection == "worst":
          rank = get_position_for_items_with_same_score(
                  pos, val, last_val, n_elements, ordered_scores)  # number of items behind
          rank = n_elements - rank  # number of nodes below or equal
        elif pos_selection == "best":
          rank = get_position_members_up(
                  pos, val, last_val, n_elements, ordered_scores)  # number of items behind or equal
        rank_percentage = rank/number_of_all_nodes

        ordered_scores.append(
                [node_name, val, rank_percentage, rank])
        last_val = val

    if pos_selection == "worst": ordered_scores.reverse()  # from largest to smallest
    ordered_scores = add_absolute_rank_column(
            ordered_scores)
        
    return ordered_scores

def get_position_members_up(pos, val, prev_val, n_elements, ordered_scores):
    members_behind = 1
    if prev_val is not None:
        if prev_val > val:
            members_behind = n_elements - pos 
        else:
            members_behind = ordered_scores[-1][3] 
    return members_behind

def get_position_for_items_with_same_score(pos, val, prev_val, n_elements, ordered_scores):
    members_behind = 0
    if prev_val is not None:
        if prev_val < val:
            members_behind = pos
        else:
            members_behind = n_elements - ordered_scores[-1][3]
    return members_behind

def add_absolute_rank_column(ranking):
    ranking_with_new_column = []
    absolute_rank = 1
    n_rows = len(ranking)
    for row_pos in range(n_rows):
        if row_pos == 0:
            new_row = ranking[row_pos] + [absolute_rank]
            ranking_with_new_column.append(new_row)
        else:
            prev_val = ranking[row_pos-1][2]
            val = ranking[row_pos][2]
            if val > prev_val:
                absolute_rank += 1

            new_row = ranking[row_pos] + [absolute_rank]
            ranking_with_new_column.append(new_row)
    return ranking_with_new_column

# List x List operation
####################################

def intersection(arr1, arr2, indexing = False):
  if indexing: 
    index_arr2 = flatlist2dic(arr2)
    intersection = [item for item in arr1 if index_arr2.get(item)] 
  else:
    intersection = [item for item in arr1 if item in arr2] 
  return intersection

def union(arr1, arr2, indexing = False):
  if indexing:
    index_arr1 = flatlist2dic(arr1)
    union = arr1 + [item for item in arr2 if not index_arr1.get(item)] 
  else:
    union = arr1 + [item for item in arr2 if item not in arr1]
  return union

def diff(arr1, arr2, indexing = False):
  if indexing:
    index_arr2 = flatlist2dic(arr2)
    diff = [item for item in arr1 if not index_arr2.get(item)]
  else:
    diff = [item for item in arr1 if item not in arr2]
  return diff

####################################
# DIC OPERATIONS
####################################

# Values - operation
####################################

## Get
######

def dig(dictio, *keys):
  try:
    for key in keys:
        dictio = dictio[key]
    return dictio
  except KeyError:
    return None 

def get_hash_values_idx(dictio):
  x_names_indx = {}
  i = 0
  for k, values in dictio.items():
    for val_id in values:
      if type(val_id) is list: val_id = val_id[0]
      query = x_names_indx.get(val_id)
      if query == None:
        x_names_indx[val_id] = i
        i += 1
  return x_names_indx

# Insert
########

# This method absorbed the add_record version of netanalyzer
def add_record(dictio, key, record, uniq=False):
  query = dictio.get(key)
  if query == None:
    dictio[key] = [record]
  elif not uniq: # We not take care by repeated entries
    query.append(record)
  elif not record in query: # We want uniq entries
    query.append(record)

def add_nested_value(dic, keys, value, multivalue = False):
    nested_dic = dic
    for key in keys[:-1]:
        if key not in nested_dic:
            nested_dic[key] = {}
        nested_dic = nested_dic[key]
    if not multivalue:
      nested_dic[keys[-1]] = value
    else:
      add_record(nested_dic, keys[-1], value)

# Keys - operation
####################################

def transform_keys(hash, function):
  new_hash = {}
  for key, val in hash.items():
    new_key = function(key)
    new_hash[new_key] = val
  return new_hash

def invert_hash(h):
    new_h = {}
    for k, vals in h.items():
        for v in vals:
            query = new_h.get(v)
            if query == None:
                new_h[v] = [k]
            else:
                query.append(k)
    return new_h

def invert_nested_hash(h):
  new_h = {}
  for k1, vals1 in h.items():
    for k2, vals2 in vals1.items(): 
      query = new_h.get(k2)
      if query == None:
        new_h[k2] = {k1 : vals2}
      else:
        query[k1] = vals2
  return new_h

def remove_nested_entries(nested_hash, func):
  empty_root_ids = []
  for root_id, entries in nested_hash.items():
    delete_entries = []
    for k, v in entries.items():
      if not func(k,v): delete_entries.append(k)
    if len(delete_entries) == len(entries):
      empty_root_ids.append(root_id)
    else:
      for k in delete_entries: entries.pop(k)
  for k in empty_root_ids: nested_hash.pop(k)

####################################
# ARRAY (Matrix) OPERATIONS
####################################

# I/O operations
####################################

def save(matrix, matrix_filename, x_axis_names=None, x_axis_file=None, y_axis_names=None, y_axis_file=None):
  if x_axis_names != None:
    with open(x_axis_file, 'w') as f:
      f.write("\n".join(x_axis_names))
  if y_axis_names != None:
    with open(y_axis_file, 'w') as f:
      f.write("\n".join(y_axis_names))
  np.save(matrix_filename, matrix)

def load(matrix_filename, x_axis_file=None, y_axis_file=None):
  x_axis = None
  y_axis = None
  if x_axis_file != None:
    with open(x_axis_file, 'r') as f: x_axis = list(map(lambda x: x.rstrip(), f.readlines()))
  if y_axis_file != None:
    with open(y_axis_file, 'r') as f: y_axis = list(map(lambda x: x.rstrip(), f.readlines()))
  matrix = np.load(matrix_filename)
  return matrix, x_axis, y_axis

# Normalization
####################################

def normalize_matrix(matrix, method="rows_cols"):
  if method == "rows_cols":
    normalized_matrix = row_col_normalization(matrix)
  elif method == "min_max":
    normalized_matrix = min_max_normalization_matrix(matrix)
  elif method == "cosine":
    normalized_matrix = cosine_normalization(matrix)
  else:
    raise ValueError("Invalid normalization method specified.")
  return normalized_matrix

def min_max_normalization_matrix(matrix):
  x_min = np.min(matrix)
  x_max = np.max(matrix)
  normalized_matrix = (matrix - x_min)/(x_max - x_min)
  return normalized_matrix

def row_col_normalization(matrix):
  # Classic degree normalization in adjacencies and laplacian matrix.
  D = np.zeros(matrix.shape)
  np.fill_diagonal(D, matrix.sum(axis=1))
  D_inv_sqrt = np.linalg.inv(np.sqrt(D))
  normalized_matrix = np.dot(np.dot(D_inv_sqrt, matrix), D_inv_sqrt)
  return normalized_matrix

def cosine_normalization(matrix):
  # TODO: Need to check when matrix with zeros in diagonal.
  dims = np.shape(matrix)
  normalized_matrix =  np.zeros(dims)
  for i in range(0, dims[0]):
    for j in range(0, dims[1]):
      norm = matrix[i, j]/np.sqrt(matrix[i, i] * matrix[j,j])
      normalized_matrix[i, j] = norm
  return normalized_matrix

# Sim <-> Dis conversion
####################################

def coords2sim(coords, sim = "dotProduct"):
  if sim == "dotProduct":
    sim_mat = coords.dot(coords.T)
  elif sim == "normalizedScaling":
    min_dist = np.min(coords2dis(coords, dist="euclidean"))
    max_dist = np.max(coords2dis(coords, dist="euclidean"))
    sim_mat = 1 - (coords2dis(coords, dist="euclidean") - min_dist) / (max_dist - min_dist)  
  elif isinstance(sim, (float, int)) or sim == "infinity" or sim == "euclidean":
    sim_mat = coords2dis(coords, dist=sim)
    sim_mat = 1 / (sim_mat + 1)
  else:
    raise ValueError("Invalid similarity measure specified.")
  return sim_mat

def coords2dis(coords, dist = "euclidean"):
  if "euclidean": dist = 2
  dist = distance_matrix(coords, coords, p = dist)
  return dist

# Stats
####################################

def get_corr(x = None, y = None, alternative='two-sided', method=None, corr_type= "pearson", rowvar= False):
  if rowvar and y is None:
    # Now, variables are the rows
    x = x.T
  if corr_type == "pearson":
    R, P = pearsonr(x, y, alternative, method)
  elif corr_type == "spearman":
    corr_obj = stats.spearmanr(a=x, b=y, alternative=alternative, nan_policy = "omit")
    R = corr_obj.correlation
    P = corr_obj.pvalue
  else:
    raise ValueError("Invalid correlation type specified.")
  return R, P

def pearsonr(x=None,y=None, alternative='two-sided', method=None): 
  if y is not None:
    corr_obj = stats.pearsonr(x, y, alternative=alternative, method= method)
    R = corr_obj.correlation
    P = corr_obj.pvalue
  else:
    x = x.T
    if alternative == 'two-sided':
        p = lambda t,n: 2 * (1 - stats.t.cdf(abs(t), n - 2))
    elif alternative == 'greater':
        p = lambda t,n: 1 - stats.t.cdf(t, n - 2)
    elif alternative == 'less':
        p = lambda t,n: stats.t.cdf(t, n - 2)
    else:
        raise ValueError("Invalid alternative argument. Valid options are 'two-sided', 'greater', or 'less'.")
    N = np.ones((x.shape[0], x.shape[0]))*x.shape[1] # This should be adopted to na cases?
    R = np.corrcoef(x) 
    T = (R*np.sqrt(N-2))/(np.sqrt(1-R**2))
    P = p(T,N)
  return R, P

def get_stats_from_matrix(matrix): 
  stats = []
  primary_stats = get_primary_stats(matrix)
  #stats << ['Matrix - Symmetric?', matrix.symmetric?]
  stats.append(['Matrix - Dimensions', 'x'.join(map(str, matrix.shape))])
  stats.append(['Matrix - Elements', primary_stats["count"]])
  stats.append(['Matrix - Elements Non Zero', primary_stats["countNonZero"]])
  stats.append(['Matrix - Non Zero Density', primary_stats["countNonZero"]/primary_stats["count"]])
  stats.append(['Weigth - Max', primary_stats["max"]])
  stats.append(['Weigth - Min', primary_stats["min"]])
  stats.append(['Weigth - Average', primary_stats["average"]])
  stats.append(['Weigth - Variance', primary_stats["variance"]])
  stats.append(['Weigth - Standard Deviation', primary_stats["standardDeviation"]])
  stats.append(['Weigth - Q1', primary_stats["q1"]])
  stats.append(['Weigth - Median', primary_stats["median"]])
  stats.append(['Weigth - Q3', primary_stats["q3"]])
  stats.append(['Weigth - Min Non Zero', primary_stats["minNonZero"]])
  stats.append(['Weigth - Average Non Zero', primary_stats["averageNonZero"]])
  stats.append(['Weigth - Variance Non Zero', primary_stats["varianceNonZero"]])
  stats.append(['Weigth - Standard Deviation Non Zero', primary_stats["standardDeviationNonZero"]])
  stats.append(['Weigth - Q1 Non Zero', primary_stats["q1NonZero"]])
  stats.append(['Weigth - Median Non Zero', primary_stats["medianNonZero"]])
  stats.append(['Weigth - Q3 Non Zero', primary_stats["q3NonZero"]])
  connections = get_connection_number(matrix)
  connection_stats = get_primary_stats(connections)
  stats.append(['Node - Elements', connection_stats["count"]])
  stats.append(['Node - Elements Non Zero', connection_stats["countNonZero"]])
  stats.append(['Node - Non Zero Density', connection_stats["countNonZero"]/connection_stats["count"]])
  stats.append(['Edges - Max', connection_stats["max"]])
  stats.append(['Edges - Min', connection_stats["min"]])
  stats.append(['Edges - Average', connection_stats["average"]])
  stats.append(['Edges - Variance', connection_stats["variance"]])
  stats.append(['Edges - Standard Deviation', connection_stats["standardDeviation"]])
  stats.append(['Edges - Q1', connection_stats["q1"]])
  stats.append(['Edges - Median', connection_stats["median"]])
  stats.append(['Edges - Q3', connection_stats["q3"]])
  stats.append(['Edges - Min Non Zero', connection_stats["minNonZero"]])
  stats.append(['Edges - Average Non Zero', connection_stats["averageNonZero"]])
  stats.append(['Edges - Variance Non Zero', connection_stats["varianceNonZero"]])
  stats.append(['Edges - Standard Deviation Non Zero', connection_stats["standardDeviationNonZero"]])
  stats.append(['Edges - Q1 Non Zero', connection_stats["q1NonZero"]])
  stats.append(['Edges - Median Non Zero', connection_stats["medianNonZero"]])
  stats.append(['Edges - Q3 Non Zero', connection_stats["q3NonZero"]])
    
  stats = map(lambda x: [x[0],str(x[1])],stats)
    
  return stats

def get_primary_stats(matrix):
  stats = {}
  max = matrix[0, 0] # Initialize max value
  min = matrix[0, 0] # Initialize min value
  min_non_zero = np.inf # Initialize min value
  values = matrix.flatten()

  stats["count"] = 0
  stats["countNonZero"] = 0 
  stats["sum"] = 0
  for value in values:
    stats["count"] += 1
    stats["countNonZero"] += 1 if value != 0 else 0
    stats["sum"] += value
    max = value if value > max else max
    min = value if value < min else min
    if value != 0 and value < min_non_zero:
      min_non_zero = value
    
  stats["max"] = max
  stats["min"] = min
  stats["minNonZero"] = min_non_zero

  quartile_stats = get_quartiles(values, stats["count"])
  stats.update(quartile_stats)
  non_zero_values = [v for v in values if v != 0]
  quartile_stats_non_zero = get_quartiles(non_zero_values, stats["countNonZero"])
  stats.update(transform_keys(quartile_stats_non_zero, lambda x: x + "NonZero"))
  get_composed_stats(stats, values)
  return stats

def get_connection_number(matrix, count_diagonal=False):
  connections = matrix != 0
  if not count_diagonal: np.fill_diagonal(connections,0)
  connections = connections.sum(1)
  connections = connections[np.newaxis, :]
  return connections

def get_quartiles(values, n_items):
  stats = {}
  stats['q1'] = np.percentile(values,25)
  stats['median'] = np.percentile(values,50)
  stats['q3'] = np.percentile(values,75)
  return stats
  
def get_composed_stats(stats, values):
  average = stats["sum"]/stats["count"]
  average_non_zero = stats["sum"]/stats["countNonZero"]
  stats["average"] = average
  stats["averageNonZero"] = average_non_zero
  stats["sumDevs"] = 0
  stats["sumDevsNonZero"] = 0
  for value in values:
    stats["sumDevs"] += (value - average) ** 2
    stats["sumDevsNonZero"] += (value - average_non_zero) ** 2 if value != 0 else 0
  stats["variance"] = stats["sumDevs"]/stats["count"]
  stats["varianceNonZero"] = stats["sumDevsNonZero"]/stats["countNonZero"]
  stats["standardDeviation"] = stats["variance"] ** 0.5
  stats["standardDeviationNonZero"] = stats["varianceNonZero"] ** 0.5


# Filtering
####################################

def binarize_mat(matrix):
  matrix = matrix > 0
  matrix = matrix.astype(float)
  return matrix
  
def filter_cutoff_mat(matrix, cutoff):
  filtered_mat = matrix >= cutoff
  mat_result = matrix * filtered_mat
  return mat_result

def percentile_filter(matrix, percentile_threshold=90):
  # Note: Percentiles is applied to rows 
  # Could be interesting to expand applications to cols and row_cols
  percentiles = np.percentile(matrix, percentile_threshold, axis=1) # TODO: Check is this is valid for non-square matrix
  result_mat = matrix >= percentiles[:, np.newaxis]
  new_adj = result_mat.transpose()*result_mat
  matrix[~new_adj] = 0
  return matrix

def remove_zero_lines(matrix, rowIds, colIds, symmetric=False):
  # TODO: semgent this in two functions for rows and columns.
  rows2delete = np.all(matrix == 0, axis=1)
  if symmetric:
      cols2delete = rows2delete
  else:
      cols2delete = np.all(matrix == 0, axis=0)

  matrix = matrix[~rows2delete]
  matrix = matrix[:,~cols2delete]
  if rowIds is not None: rowIds = [rowIds[i] for i in range(0,len(rowIds)) if not rows2delete[i]]
  if colIds is not None: colIds = [colIds[i] for i in range(0,len(colIds)) if not cols2delete[i]]

  return matrix, rowIds, colIds


# Clustering
####################################

def get_hc_clusters(matrix, dist = 'euclidean', method = 'single', identify_clusters = 'cut_tree', height = None, n_clusters= None, item_list = None ):
  cls_objects = {}
  if dist == 'custom': # User gives a custom distance matrix so we only tranfor to pdist output format
    np.fill_diagonal(matrix, 0)
    dist_vector = squareform(matrix)
  else:
    dist_vector = pdist(matrix, metric=dist)
  cls_objects['dist_vector'] = dist_vector
  hc_clust = linkage(dist_vector, method)
  cls_objects['link'] = hc_clust
  if identify_clusters == 'cut_tree':
    clusters = cut_tree(hc_clust, height=height, n_clusters = n_clusters )
  elif identify_clusters == 'max_avg': # use only with matrix distances between 0 - 1
    if dist == 'custom':
      dist_matrix = matrix
    else:
      dist_matrix = squareform(dist_vector)
    clusters = get_cls_max_avg(hc_clust, dist_matrix)
  else:
    raise ValueError("Invalid cluster identifier metric specified.")
  cls_objects['cls'] = clusters # Give raw clustering object

  tag_singletons(clusters)
  if item_list != None: clusters = tag_items_in_clusters(clusters, item_list)  
  return clusters, cls_objects

def get_cls_max_avg(hc_clust, matrix):
  y_len, x_len = matrix.shape
  tree = {} # clust id : [member_ids]
  cl_avg_values = {} #clust_id : [ cluster_partition_density ]

  counter = x_len # this works as cluster id. This is used by the linkage method to tag the intermediate clusters: https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html
  last_dist = None
  last_cluster_pool = []
  max_avg_value = 10000000000
  max_cluster_ids = []
  max_avg_val_tree = {}
  for a_id, b_id, dist, n_members in hc_clust:
    dist = round(dist, 5) # To make equal similar distances that differs in very low values
    if last_dist != None and dist != last_dist: # We could have several clusters at the same dist, so we group the merge events to clculate the partition density
      avg_value = get_avg_value4tree_cut(last_cluster_pool, cl_avg_values, tree, x_len)
      if avg_value < max_avg_value: # check the best partition density
        max_avg_value = avg_value
        max_cluster_ids = last_cluster_pool
        max_avg_val_tree = copy.copy(tree)
    a_id = int(a_id) # Linkage method returns member ids as float instead of int
    b_id = int(b_id)
    member_list = get_member_list(counter, a_id, b_id, x_len, tree) # members that we merge to build the new agglomerative cluster
    cl_avg_values[counter] = get_cluster_avg_value(member_list, matrix)
    last_cluster_pool = [ cl_id for cl_id in last_cluster_pool if cl_id not in [a_id, b_id] ] # update clusters removin merged cl ids and adding the new cluters ids
    last_cluster_pool.append(counter)
    last_dist = dist
    counter += 1
      
  avg_value = get_avg_value4tree_cut(last_cluster_pool, cl_avg_values, tree, x_len) # update clusters removin merged cl ids and adding the new cluters ids
  if avg_value < max_avg_value: # check the best partition density on the last distance that not was checked
    max_avg_value = avg_value
    max_cluster_ids = last_cluster_pool
    max_avg_val_tree = copy.copy(tree)
  final_clusters = np.repeat([[None]], x_len, axis=0)
  for cluster_id in max_cluster_ids:
    members = max_avg_val_tree[cluster_id]
    for m in members: final_clusters[m] = [cluster_id]
  return final_clusters

def get_avg_value4tree_cut(last_cluster_pool, cl_avg_values, tree , n_elements):
  avg_value = np.median([ cl_avg_values[cl_id] for cl_id in last_cluster_pool])
  total = sum([ len(tree[cl_id]) for cl_id in last_cluster_pool])
  avg_value = (1 - total/(n_elements+1)) * (1 + avg_value)
  # avg_value = sum([ cl_avg_values[cl_id] * len(tree[cl_id]) for cl_id in last_cluster_pool])/total
  return avg_value

def get_member_list(cluster_id, a_id, b_id, n_records, tree):
  member_list = []
  add_cluster_members(member_list, a_id, n_records, tree) # get cluster members from previous a cluster
  add_cluster_members(member_list, b_id, n_records, tree) # get cluster members from previous b cluster
  tree[cluster_id] = member_list
  return member_list

def add_cluster_members(cluster, member_id, n_records, tree):
  if member_id < n_records: # check if member_id is a cluster with only one member that is a original record. That id is less than n_records is the criteria described in https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html
    cluster.append(member_id)
  else: # The id represents the merge of two previous clusters. We obtain the member list from the tree and remove it to merge it in the new cluster
    cluster.extend(tree.pop(member_id))

def get_cluster_avg_value(member_list, matrix):
  members = copy.copy(member_list)
  values = []
  while len(members) > 1:
    ref = members.pop()
    values.extend([matrix[ref, m] for m in members])
  return np.mean(values)

def tag_singletons(clusters):
  counter = 0
  for i in range(0, len(clusters)):
    if clusters[i] is None:
      clusters[i] = [f"S{counter}"]
      counter += 1

def tag_items_in_clusters(data, item_list):
  clustering_data = []
  for i, cluster_id in enumerate(data): clustering_data.append([item_list[i], cluster_id[0]])
  clusters = {}
  for item_id, cluster_id in clustering_data:
    query = clusters.get(cluster_id)
    if query == None:
        clusters[cluster_id] = [item_id]
    else:
        query.append(item_id)
  return clusters  

####################################
# Explicit conversions
####################################

# General conversor #

def transform2obj(obj, inFormat=None, outFormat=None, rowIds= None, colIds= None): 
  if outFormat == 'pair':
    if inFormat == 'matrix': 
        obj = matrix2pairs(obj, rowIds=rowIds, colIds=colIds)
    if inFormat == 'nested_pairs':
        obj = nested_pairs2pairs(obj)
  elif outFormat == 'matrix':
    if inFormat == 'pair': 
        obj, rowIds, colIds = pairs2matrix(obj)
    if inFormat == 'nested_pairs':
        obj, rowIds, colIds = pairs2matrix(nested_pairs2pairs(obj)) # Talk with PSZ about the trade-off combinatorial vs optimization
  elif outFormat == "nested_pairs":
    if inFormat == "pair":
        obj = list2dic(pairs)
  else:
    raise ValueError("Invalid conversion specified.")
  return obj, rowIds, colIds

# List -> Dic
####################################

def flatlist2dic(l):
  return {el:True for el in l}

# List -> dic
#############

def list2dic(pairs):
  dic_from_list = {}
  for pair in pairs: add_nested_value(dic_from_list, keys=pairs[:-1],value=pairs[-1])
  return dic_from_list

# Dic -> Matrix(array)
####################################

def to_bmatrix(dictio):
  x_names_indx = get_hash_values_idx(dictio)
  y_names = list(dictio.keys())
  x_names = list(x_names_indx.keys())
   # row (y), cols (x)
  matrix = np.zeros((len(dictio), len(x_names)))
  i = 0
  for id, items in dictio.items():
    for item_id in items: matrix[i, x_names_indx[item_id]] = 1
    i += 1
  return matrix, y_names, x_names

def to_wmatrix(dictio, squared = True, symm = True):
  if squared:
    matrix, element_names = to_wmatrix_squared(dictio, symm=symm)
    return matrix, element_names
  else:
    matrix, y_names, x_names = to_wmatrix_rectangular(dictio)
    return matrix, y_names, x_names

def to_wmatrix_squared(dictio, symm = True):
  element_names = {}
  for elementA, relations in dictio.items():
    if element_names.get(elementA) == None:
      element_names[elementA] = True
    for elementB in relations.keys():
      if element_names.get(elementB) == None: 
        element_names[elementB] = True
  
  element_names = list(element_names.keys())
  matrix = np.zeros((len(element_names), len(element_names)))
  i = 0
  for elementA in element_names:
    relations = dictio.get(elementA)
    if relations != None:
      for j, elementB in enumerate(element_names):
        if elementA != elementB:
          query = relations.get(elementB)
          if query != None:
            matrix[i, j] = query
            if symm: # TODO: PSZ, lo q se hace aqui no me cuadra
              matrix[j, i] = query
    i += 1
  return matrix, element_names

def to_wmatrix_rectangular(dictio):
  y_names = list(dictio.keys())
  x_names = list(get_hash_values_idx(dictio).keys())
  matrix = np.zeros((len(y_names), len(x_names)))
  i = 0
  for elementA, relations in dictio.items():
    for j, elementB in enumerate(x_names):
        query = relations.get(elementB)
        if query != None:
          matrix[i, j] = query
    i += 1
  return matrix, y_names, x_names

# Dic -> List
####################################

def nested_pairs2pairs(nested_dic_pairs): 
  pairs = []
  for item_a, dat in nested_dic_pairs.items(): 
    for item_b, val in dat.items(): pairs.append([item_a, item_b, val])
  return pairs

# List -> Matrix(Array)
####################################

def pairs2matrix( pairs, symm= True): 
  count_A = 0
  index_A = {}
  count_B = 0
  index_B = {}
  if symm:
      for pair in pairs:
          elementA, elementB, val = pair
          count_A = update_index(index_A, elementA, count_A)
          count_A = update_index(index_A, elementB, count_A)
      index_B = index_A
  else:
      for pair in pairs:
          elementA, elementB, val = pair
          count_A = update_index(index_A, elementA, count_A)
          count_B = update_index(index_B, elementB, count_B)

  elementA_names = list(index_A.keys())
  elementB_names = list(index_B.keys())

  matrix = np.zeros((len(elementA_names), len(elementB_names)))
  for pair in pairs:
      elementA, elementB, val = pair
      i = index_A[pair[0]] 
      j = index_B[pair[1]] 
      matrix[i, j] = val
      if symm: matrix[j, i] = val

  return matrix, elementA_names, elementB_names

def update_index(index, element, count): 
  if index.get(element) is None:
    index[element] = count
    count += 1
  return count

# Matrix(Array) -> List
####################################
# TODO: Talk with PSZ: The next three methods are redundant, 
# but i dont see an efficient manner of making one generic function (Fred)

def matrix2pairs(matrix, rowIds, colIds, symm = False): 
  relations = []
  if symm:
    for rowPos, rowId in enumerate(rowIds):
      for colPos, colId in enumerate(colIds[rowPos:]):
        colPos += rowPos
        relations.append([rowId, colId, matrix[rowPos, colPos]])
  else:
    for rowPos, rowId in enumerate(rowIds):
      for colPos, colId in enumerate(colIds):
        relations.append([rowId, colId, matrix[rowPos, colPos]])
  return relations

def matrixes2pairs(matrixes, rowIds, colIds, symm = False): 
  # When there are multiple matrix with the same rows and cols.
  relations = []
  if symm:
    for rowPos, rowId in enumerate(rowIds):
      for colPos, colId in enumerate(colIds[rowPos:]):
        colPos += rowPos
        associationValues = [matrix[rowPos, colPos] for matrix in matrixes]
        relations.append([rowId, colId, *associationValues])
  else:
    for rowPos, rowId in enumerate(rowIds):
      for colPos, colId in enumerate(colIds):
        associationValues = [matrix[rowPos, colPos] for matrix in matrixes]
        relations.append([rowId, colId, *associationValues])
  return relations

def matrix2relations(finalMatrix, rowIds, colIds, symm = False): 
  relations = []
  if symm:
    for rowPos, rowId in enumerate(rowIds):
      for colPos, colId in enumerate(colIds[rowPos:]):
        colPos += rowPos
        associationValue = finalMatrix[rowPos, colPos]
        if associationValue >= 0: relations.append([rowId, colId, associationValue])
  else:
    for rowPos, rowId in enumerate(rowIds):
      for colPos, colId in enumerate(colIds):
        associationValue = finalMatrix[rowPos, colPos]
        if associationValue >= 0: relations.append([rowId, colId, associationValue])
  return relations