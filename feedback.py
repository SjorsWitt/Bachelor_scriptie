TOO_SHORT_AVERAGE = "Your variable names likely do not convey enough meaning, as they are too short on average.\n"
TOO_LONG_AVERAGE = "Your variable names are too long on average. Long variable names can be hard to type or can obscure the visual structure of your program.\n"
SINGLE_LETTER = "Variable names should not consist of a single letter, unless it is a very simple for loop iterator.\nYou should reconsider the following names: "
TOO_LONG = "Variable names of more than 25 characters should be avoided where possible.\nThe following names are too long: "

TOO_MANY_IN_ONE_CLUSTER = "A variable that is used this many times within a small scope should be shorter to improve readability."
TOO_LITTLE_IN_ONE_CLUSTER = "A variable that is used this little within a small scope should be more descriptive."

GLOBAL_BIG_CLUSTER = "Global variable names should be longer than local variables, unless it is used too much within a small piece of code."
LOCAL_BIG_CLUSTER = "This variable is used too much within a small piece of code and should thus have a shorter name."
SMALL_LOCAL_SCOPE = "Long names should not be used in local scopes that are relatively small."