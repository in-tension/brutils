import imp

import brutils as br
imp.reload(br)


l = [x for x in range(10)]
data = [l for x in range(10)]

outpath = '/Users/baylieslab/Documents/Amelia/code_dev/projects/brutils/testing.csv'

br.rows_to_csv(outpath)