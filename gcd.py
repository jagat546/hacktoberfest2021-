# Recursive function to return gcd of a and b
def gcd(a,b):
	
	# Everything divides 0
	if (b == 0):
		return a
	return gcd(b, a%b)

# Driver program to test above function
a = 98
b = 56
if(gcd(a, b)):
	print('GCD of', a, 'and', b, 'is', gcd(a, b))
else:
	print('not found')

