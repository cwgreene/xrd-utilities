import optparse as op

parser = op.OptionParser()
parser.add_option("-r",dest="range",default="0:360")
(options,args) = parser.parse_args()
(start,end) = map(float,options.range.split(":"))
