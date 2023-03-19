import os
import sys
from totalsegmentator.map_to_binary import class_map
import numpy as np
np.random.seed(42)

def main(output_file):
    mylines = '0   0   0   0    0 0 0 "Back Ground"\n'
    for int_val,str_val in class_map['total'].items():
        r,g,b = np.random.randint(0,255,3)
        myline = f'{int_val} {r} {g} {b} 1 1 1 "{str_val}"\n'
        mylines+=myline
    with open(output_file,'w') as f:
        f.write(mylines)

if __name__ == "__main__":
    output_file = sys.argv[1]
    main(output_file)
    