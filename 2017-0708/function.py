print(abs(-10))
f = abs
print(f)
print(f(-10))
#abs = 10  不可以这样做
#print(abs(-10))

def add(x,y,f):
	return f(x) + f(y)

x = -5
y = 6
f = abs
print(add(x,y,f))