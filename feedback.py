import parameters

TOO_SHORT_AVERAGE = "Your variable names likely do not convey enough meaning, as they are too short on average."
TOO_LONG_AVERAGE = "Your variable names are too long on average. Long variable names can be hard to type or can obscure the visual structure of your program."

SAME_LANGUAGE = "Make sure all your variable names are in the same language."

SINGLE_LETTER = "Variable names should not consist of a single letter, unless it is a very simple for loop iterator or it is a widely accepted name (e.g. x & y as coordinates).\nYou should reconsider the following names: "
TOO_LONG = "Variable names of more than " + str(parameters.MAX_NAME_LENGTH) + " characters should be avoided where possible.\nThe following names are too long: "

GLOBAL_TOO_SHORT_CLUSTER = "Global variable names should be relatively long, unless it is used frequently within a small piece of code. Short names will likely not convey enough meaning."
EXAMPLE_GLOBAL_SHORT_CLUSTER = "One example of a short global variable name in your code that could be longer:"

LOCAL_TOO_SHORT_CLUSTER = "Local variable names should generally be longer when the variable is rarely used. Short names will likely not convey enough meaning, while rarely used long names will not decrease the readability of your code."
EXAMPLE_LOCAL_SHORT_CLUSTER = "One example of a short local variable name in your code that could be longer:"

TOO_SHORT_LINE_RANGE = "Variable names should generally be longer when the variable is used over a longer distance. Short names are more likely to lose their meaning over a longer distance."
EXAMPLE_SHORT_LINE_RANGE = "One example of a short variable name that is used over a long distance:"

GLOBAL_TOO_LONG_CLUSTER = "Global variables that are frequently used within a small piece of code should be shorter. Long names that are frequently used within a small piece of code will decrease the readability of your code."
EXAMPLE_GLOBAL_LONG_CLUSTER = "One example of such a long global variable name in your code that should be shorter:"

LOCAL_TOO_LONG_CLUSTER = "Local variable names should be relatively short, unless it is rarely used. Long names that are frequently used within a small piece of code will decrease readability of your code."
EXAMPLE_LOCAL_LONG_CLUSTER = "One example of such a long local variable name in your code that should be shorter:"
