def tri():
	L = [1]
	yield L
	while True:
		L =[1] + [L[x]+L[x+1] for x in range(len(L)-1)]+[1]
		yield L
n = 0
for L in tri():
	print(L)
	n = n + 1
	if n == 10:
		break