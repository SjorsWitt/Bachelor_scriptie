# default parameters are based on found literature
MIN_AVERAGE_NAME_LENGTH = 8 #10
MAX_AVERAGE_NAME_LENGTH = 14 #16
MAX_NAME_LENGTH = 20 #25

# minimum distance between clusters
CLUSTER_DISTANCE = 5

# global cluster is considered big with at least GLOBAL_BIG_CLUSTER number of variables
GLOBAL_BIG_CLUSTER = 4

# local cluster is considered big with at least GLOBAL_BIG_CLUSTER number of variables
LOCAL_BIG_CLUSTER = 3

# variable loses meaning over BIG_DISTANCE number of lines
BIG_DISTANCE = 10

# exclude iterators when looking for single-letter variables
EXCLUDE_ITERATORS = True

# exclude single-letter variables from below goal average names
EXCLUDE_SINGLE_LETTER = False