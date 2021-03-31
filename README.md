# Microchronology
Tools for working with Oracle Bone Microchronology
At the moment, all code is in the main file.  I'm using Shaughnessy's Microchronology model, but taking an average month of 29.5 days.
Eventually uncertainty bounds will be implemented.
Input data as month/ganzhi where the ganzhi has been converted to its numerical place in the cycle.
Right now, the program just takes in data, orders it, and then outputs to the command-line.
Because the algorithm throws out anything incompatible with existing date ranges, when you see an error in a month, you will need to review all data for that month to determine the source of the error.  The same is true when compiling year data.
At the moment, dates suspected to be from additional years can be added simply by adding numbers beyond 12 or 13.
The next step is to implement user input.
