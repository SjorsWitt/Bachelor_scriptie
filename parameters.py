# default parameters are based on found literature
MIN_AVERAGE_NAME_LENGTH = 8 #10
MAX_AVERAGE_NAME_LENGTH = 14 #16
MAX_NAME_LENGTH = 23 #25

# minimum distance between clusters
CLUSTER_DISTANCE = 5

# global cluster is considered big with at least GLOBAL_BIG_CLUSTER number of variables
GLOBAL_BIG_CLUSTER = 4

# local cluster is considered big with at least GLOBAL_BIG_CLUSTER number of variables
LOCAL_BIG_CLUSTER = 3

# variable loses meaning over BIG_DISTANCE number of lines
BIG_DISTANCE = 10

# exclude iterators from single-letter variables
EXCLUDE_ITERATORS_SL = True

# exclude interators from below goal average names
EXCLUDE_ITERATORS_BA = False

# exclude single-letter variables from below goal average names
EXCLUDE_SINGLE_LETTER = True