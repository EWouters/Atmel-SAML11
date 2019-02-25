from dgilib_thread import *

data = ([0.0021333333333333334,
         0.46120853333333334, 
         0.9612976, 
         1.25,
         1.4613029333333334,
         1.9613818666666667, 
         2.4613904, 
         2.9614949333333334, 
         3.461536, 
         3.9616213333333334, 
         4.4616672, 
         4.9617392], 
        [[True, True, False, False],
         [True, True, True, False],
         [True, True, True, False],
         [True, True, False, False],
         [True, True, True, False],
         [True, True, False, False],
         [True, True, True, False],
         [True, True, False, False],
         [True, True, True, False],
         [True, True, False, False],
         [True, True, True, False],
         [True, True, True, False]])


print(identify_hold_times(data, True, 2))
