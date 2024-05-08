import re

ONLY_DIRECTION_GU = re.compile('[동서남북]*구')
SI = re.compile('.*시')
DO = re.compile('.*도')
GU = re.compile('.*구')
UB = re.compile('.*읍')
MYN = re.compile('.*면')
RI = re.compile('.*리')
DONG = re.compile('.*동')
