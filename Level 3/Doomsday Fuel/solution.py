from fractions import Fraction


def answer(m):
	# your code here
	if len(m) == 1:
		return [1, 1]

	v = [1]
	for i in range(len(m) - 1):
		v.append(0)

	terminals = []
	factors = []

	for i in range(len(m)):
		if all(v == 0 for v in m[i]):
			terminals.append(i)

	# normalize matrix
	for row in range(len(m)):
		denominator = 0
		for col in range(len(m)):
			denominator = denominator + m[row][col]
		if denominator != 0:
			for col in range(len(m)):
				m[row][col] = Fraction(m[row][col], denominator)

	# create identity matrix
	identity = make_identity(len(m))

	id_minus_m = sub_mat(identity, m)

	id_minus_m_inv = inv(id_minus_m)

	probs_temp = mult_vec(v, id_minus_m_inv)
	probs = []

	for i in range(len(probs_temp)):
		if i in terminals:
			probs.append(probs_temp[i])

	lcm = lcm_list([n.denominator for n in probs])

	probs_fin = [(lcm / n.denominator) * n.numerator for n in probs]
	probs_fin.append(lcm)

	return probs_fin


def inv(matrix):
	m = matrix
	lead = 0
	rows = len(m)
	cols = len(m[0])
	inv = make_identity(len(m))

	for r in range(rows):
		if cols <= lead:
			return
		i = r
		while m[i][lead] == 0:
			i = i + 1
			if rows == i:
				i = r
				lead = lead + 1
				if cols == lead:
					return
		m[i], m[r] = m[r], m[i]
		inv[i], inv[r] = inv[r], inv[i]
		if m[r][lead] != 0:
			denom = m[r][lead]
			denom2 = inv[r][lead]
			for col in range(len(m[r])):
				m[r][col] = m[r][col] / denom
				inv[r][col] = inv[r][col] / denom
		for x in range(rows):
			if x != r:
				prod = mult(m[x][lead], m[r])
				prod2 = mult(m[x][lead], inv[r])
				m[x] = sub(m[x], prod)
				inv[x] = sub(inv[x], prod2)
		lead = lead + 1

	return inv


def mult(n, r):
	res = []
	for col in range(len(r)):
		res.append(n * r[col])

	return res


def mult_vec(v, m):
	res = []
	for col in range(len(v)):
		sum = 0
		for row in range(len(m)):
			sum = sum + v[row] * m[row][col]
		res.append(sum)

	return res


def sub(r1, r2):
	res = []
	for col in range(len(r1)):
		res.append(r1[col] - r2[col])

	return res


def sub_mat(m1, m2):
	res = [[0 for col in range(len(m1[0]))] for row in range(len(m1))]
	for row in range(len(m1)):
		for col in range(len(m1[0])):
			res[row][col] = m1[row][col] - m2[row][col]

	return res


def make_identity(size):
	identity = [[0 for col in range(size)] for row in range(size)]
	one = 0
	for col in range(size):
		identity[col][one] = 1
		one = one + 1

	return identity


def gcd(x, y):
	while y:
		x, y = y, x % y

	return x


def lcm(x, y):
	return x * y / gcd(x, y)


def lcm_list(lst):
	return reduce(lambda x, y: lcm(x, y), lst)
