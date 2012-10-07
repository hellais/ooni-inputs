# -*- encoding: utf-8 -*-
#
# This file is used for splitting the alexa top 1M url list into chunks of 10k
# sites each to analysis.
#
# :authors: Arturo Filastò
# :licence: see LICENSE

import sys
if len(sys.argv) < 2:
    print "Usage %s path/to/alexa-top-1m.txt"
    sys.exit()

filename = sys.argv[1]

f = open(filename)
i = 0
j = 0
for line in f:
    if (i % 10000) == 0:
        j += 10000
        out_file = 'processed-alexa-top-1m-%s.txt' % str(j)

    out_fp = open(out_file, 'a+')
    out_fp.write(line)
    out_fp.close()
    i += 1

f.close()
