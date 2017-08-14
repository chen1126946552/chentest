def fact(n):
	if n==1:
		return 1
	return n * fact(n-1)
#尾递归
def fact_iter(num,product):
	if num == 1:
		return product
	return fact_iter(num-1,num * product)

def fact_2(n):
	return fact_iter(n,1)


#首先明白基本思想：
#1.把A柱子上的n-1个盘子挪到B上
#2.把A柱上最后一个挪到C上
#3.再把B上的n-1个盘子挪到C上
#你可以从两个开始推，会发现n个数量盘子总是依赖于n-1个的解决方法，
#n-1（递归作为n）依赖于n-2（作为n-1）一直到移动3个需要先移动2个，推推就明白了
def move(n,a,b,c):
	if n == 1:
		print(a,'->',c)
		return
	move(n-1,a,c,b)
	move(1,a,b,c)
	move(n-1,b,a,c)



def main():
	print(fact(5))
	print(fact_2(5))
	move(3,'A','B','C')

if __name__ == "__main__":
    main()