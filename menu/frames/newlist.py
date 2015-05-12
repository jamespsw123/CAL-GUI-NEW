def newlist(l):
	for i in range(len(l)):
		if i != 0:
			l[i] = l[i] +l[i-1]
	return l

			

l = [1, 2, 2, 4, 5, 9]

print newlist(l)