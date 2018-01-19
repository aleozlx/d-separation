x = [1,1,1,1,-1,-1,1,-1,-1,1,1,1,-1,-1,-1,-1,1,-1,-1,1]

def maxsum(x):
	assert x
	if len(x)>=2:
		rest, last = x[:-1], x[-1]
		if last < 0:
			return maxsum(rest)
		else:
			return maxsum(rest)+last
	else:
		