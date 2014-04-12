#!/usr/bin/python3

def getintersection(x, y):
	x1,x2 = (x[0],x[1]) if x[0]<x[1] else (x[1],x[0])
	y1,y2 = (y[0],y[1]) if y[0]<y[1] else (y[1],y[0])
	if (x1<=y1<=x2) or (x1<=y2<=x2) or (y1<=x1 and y2>=x2):
		z1 = max(x1, y1)
		z2 = min(x2, y2)
		return z1, z2
	else:
		return None
def union(lSegments):
	lSubresult = []
	lResult = []
	for segment in lSegments:
		lSubresult.append((segment[0], segment[1]) if segment[0]<segment[1] else (segemnt[1], segment[0]))
	lSubresult.sort()
	for y in lSubresult:
		if len(lResult) == 0:
			lResult.append(y)
		else:
			x = lResult.pop()
			x1, x2 = x
			y1, y2 = y
			if (x1<=y1<=x2) or (x1<=y2<=x2) or (y1<=x1 and y2>=x2):
				z1 = min(x1, y1)
				z2 = max(x2, y2)
				lResult.append((z1, z2))
			else:
				lResult.append((x1, x2))
				lResult.append((y1, y2))		
	return lResult
