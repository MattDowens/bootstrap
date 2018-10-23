import bootstrap
import matplotlib.pyplot as plt
import time
import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from new_ising_class import *
import sys
from symengine.lib.symengine_wrapper import *
import mpmath
import xml.dom.minidom
import re
import math
bootstrap.sdpb_path = "/usr/local/Cellar/sdpb/0.0.2/bin/sdpb"

ell = Symbol('ell')
delta  = Symbol('delta')
delta_ext = Symbol('delta_ext')
prec = 800
chol_tol = 1e-200
dec_prec = int((3.0 / 10.0) * prec)
mpmath.mp.dps = dec_prec
tiny = RealMPFR("1e-" + str(dec_prec // 2), prec)
rho_cross = 3 - 2 * mpmath.sqrt(2)
r_cross = eval_mpfr(3 - 2 * sqrt(2), prec)

class Point(object):
	def __init__(self, sig, eps, kmax, lmax, mmax, nmax, components, max_dimension, table_before, table_after, good_spins, bad_spins, cb_time, cb_cpu):
		self.sig = sig
		self.eps = eps
		self.kmax = kmax
		self.lmax = lmax
		self.mmax = mmax
		self.nmax = nmax
		self.components = components
		self.max_dimension = max_dimension
		self.table_before = table_before
		self.table_after = table_after
		self.good_spins = good_spins
		self.bad_spins = bad_spins
		#self.allowed = allowed
		#self.run_time = run_time
		#self.cpu_time = cpu_time
		self.cb_time = cb_time
		self.cb_cpu = cb_cpu
		#self.xml_time = xml_time
		#self.xml_cpu = xml_cpu
		#self.sdp_time = sdp_time
		#self.sdp_cpu = sdp_cpu

	# Saves a Point object' data to file named in self.name
	def save(self, name):
		with open(name + ".py", 'a') as file:
			file.write("sig = " + str(self.sig) + "\n")
			file.write("eps = " + str(self.eps) + "\n")
			file.write("kmax = " + str(self.kmax) + "\n")
			file.write("lmax = " + str(self.lmax) + "\n")
			file.write("mmax = " + str(self.mmax) + "\n")
			file.write("nmax = " + str(self.nmax) + "\n")
			file.write("components = " + str(self.components) + "\n")
			file.write("max_dimension = " + str(self.max_dimension) + "\n")
			file.write("table_before = " + str(self.table_before) + "\n")
			file.write("table_after = " + str(self.table_after) + "\n")
			file.write("good_spins = " + str(self.good_spins) + "\n")
			file.write("bad_spins = " + str(self.bad_spins) + "\n")
			file.write("cb_time = " + str(self.cb_time) + "\n")
			file.write("cb_cpu = " + str(self.cb_cpu) + "\n")
			file.write("self.point_table.append(Point(sig, eps, kmax, lmax, mmax, nmax, components, max_dimension, allowed, table_before, table_after, good_spins, bad_spins, cb_time, cb_cpu))" + "\n")

class PolynomialVector:
	def __init__(self, derivatives, spin_irrep, poles):
		if type(spin_irrep) == type(1):
			spin_irrep = [spin_irrep, 0]
		self.vector = derivatives
		self.label = spin_irrep
		self.poles = poles

class SDP:
	def __init__(self, dim_list, conv_table_list, vector_types = [[[[[[1, 0, 0, 0]]]], 0, 0]], prototype = None):
		# If a user is looking at single correlators, we will not punish
		# her for only passing one dimension
		if type(dim_list) != type([]):
			dim_list = [dim_list]
		if type(conv_table_list) != type([]):
			conv_table_list = [conv_table_list]

		# Same story here
		self.dim = 0
		self.k_max = 0
		self.l_max = 0
		self.m_max = 0
		self.n_max = 0
		self.odd_spins = False

		# Just in case these are different
		for tab in conv_table_list:
			self.dim = max(self.dim, tab.dim)
			self.k_max = max(self.k_max, tab.k_max)
			self.l_max = max(self.l_max, tab.l_max)
			self.m_max = max(self.m_max, tab.m_max)
			self.n_max = max(self.n_max, tab.n_max)

		self.points = []
		self.m_order = []
		self.n_order = []
		self.table = []
		self.unit = []
		self.irrep_set = []

		# Turn any "raw elements" from the vectorial sum rule into 1x1 matrices
		for i in range(0, len(vector_types)):
			for j in range(0, len(vector_types[i][0])):
				if type(vector_types[i][0][j][0]) != type([]):
					vector_types[i][0][j] = [[vector_types[i][0][j]]]

		# Again, fill in arguments that need not be specified for single correlators
		for i in range(0, len(vector_types)):
			for j in range(0, len(vector_types[i][0])):
				for k in range(0, len(vector_types[i][0][j])):
					for l in range(0, len(vector_types[i][0][j][k])):
						if len(vector_types[i][0][j][k][l]) == 2:
							vector_types[i][0][j][k][l].append(0)
							vector_types[i][0][j][k][l].append(0)

		# We must assume the 0th element put in vector_types corresponds to the singlet channel
		# This is because we must harvest the identity from it
		for matrix in vector_types[0][0]:
			chosen_tab = conv_table_list[matrix[0][0][1]]

			for i in range(0, len(chosen_tab.table[0].vector)):
				unit = 0
				for r in range(0, len(matrix)):
					for s in range(0, len(matrix[r])):
						quad = matrix[r][s]
						tab = conv_table_list[quad[1]]
						unit += quad[0] * tab.table[0].vector[i].subs(delta, 0).subs(delta_ext, (dim_list[quad[2]] + dim_list[quad[3]]) / 2.0)

				self.m_order.append(chosen_tab.m_order[i])
				self.n_order.append(chosen_tab.n_order[i])
				self.unit.append(unit)

		# Looping over types and spins gives "0 - S", "0 - T", "1 - A" and so on
		for vec in vector_types:
			if (vec[1] % 2) == 1:
				self.odd_spins = True
				start = 1
			else:
				start = 0

			for l in range(start, self.l_max, 2):
				size = len(vec[0][0])

				outer_list = []
				for r in range(0, size):
					inner_list = []
					for s in range(0, size):
						derivatives = []
						large_poles = []
						for matrix in vec[0]:
							quad = matrix[r][s]
							tab = conv_table_list[quad[1]]

							if tab.odd_spins:
								index = l
							else:
								index = l // 2
							if quad[0] != 0:
								large_poles = tab.table[index].poles

							for i in range(0, len(tab.table[index].vector)):
								derivatives.append(quad[0] * tab.table[index].vector[i].subs(delta_ext, (dim_list[quad[2]] + dim_list[quad[3]]) / 2.0))
						inner_list.append(PolynomialVector(derivatives, [l, vec[2]], large_poles))
					outer_list.append(inner_list)
				self.table.append(outer_list)

		# We are done with vector_types now so we can change it
		for vec in vector_types:
			matrix = deepcopy(vec[0][0])
			for r in range(0, len(matrix)):
				for s in range(0, len(matrix)):
					quad = matrix[r][s]
					dim2 = dim_list[quad[2]]
					dim3 = dim_list[quad[3]]
					dim1 = dim2 + conv_table_list[quad[1]].delta_12
					dim4 = dim3 - conv_table_list[quad[1]].delta_34
					matrix[r][s] = [dim1, dim2, dim3, dim4]
			self.irrep_set.append([matrix, vec[2]])

def add_point(sdp, spin_irrep = -1, dimension = -1, extra = []):
	if spin_irrep == -1:
		sdp.points = []
		return

	if type(spin_irrep) == type(1):
		spin_irrep = [spin_irrep, 0]
	if dimension != -1:
		sdp.points.append((spin_irrep, dimension, extra))
	else:
		for p in sdp.points:
			if p[0] == spin_irrep:
				sdp.points.remove(p)

def get_table_index(sdp, spin_irrep):
	if type(spin_irrep) == type(1):
		spin_irrep = [spin_irrep, 0]
	for l in range(0, len(sdp.table)):
		if sdp.table[l][0][0].label == spin_irrep:
			return l
	return -1

def shifted_prefactor(poles, base, x, shift):
		product = 1
		for p in poles:
			product *= x - (p - shift)
		return (base ** (x + shift)) / product

def integral(pos, shift, poles):
	"""
		Returns the inner product of two monic monomials with respect to the
		positive measure prefactor that turns a `PolynomialVector` into a rational
		approximation to a conformal block.
	"""
	single_poles = []
	double_poles = []
	ret = mpmath.mpf(0)

	for p in poles:
		p = mpmath.mpf(str(p))

		if (p - shift) in single_poles:
			single_poles.remove(p - shift)
			double_poles.append(p - shift)
		elif (p - shift) < 0:
			single_poles.append(p - shift)

	for i in range(0, len(single_poles)):
		denom = mpmath.mpf(1)
		pole = single_poles[i]
		other_single_poles = single_poles[:i] + single_poles[i + 1:]
		for p in other_single_poles:
			denom *= pole - p
		for p in double_poles:
			denom *= (pole - p) ** 2
		ret += (mpmath.mpf(1) / denom) * (rho_cross ** pole) * ((-pole) ** pos) * mpmath.factorial(pos) * mpmath.gammainc(-pos, a = pole * mpmath.log(rho_cross))

	for i in range(0, len(double_poles)):
		denom = mpmath.mpf(1)
		pole = double_poles[i]
		other_double_poles = double_poles[:i] + double_poles[i + 1:]
		for p in other_double_poles:
			denom *= (pole - p) ** 2
		for p in single_poles:
			denom *= pole - p
		# Contribution of the most divergent part
		ret += (mpmath.mpf(1) / (pole * denom)) * ((-1) ** (pos + 1)) * mpmath.factorial(pos) * ((mpmath.log(rho_cross)) ** (-pos))
		ret -= (mpmath.mpf(1) / denom) * (rho_cross ** pole) * ((-pole) ** (pos - 1)) * mpmath.factorial(pos) * mpmath.gammainc(-pos, a = pole * mpmath.log(rho_cross)) * (pos + pole * mpmath.log(rho_cross))

		factor = 0
		for p in other_double_poles:
			factor -= mpmath.mpf(2) / (pole - p)
		for p in single_poles:
			factor -= mpmath.mpf(1) / (pole - p)
		# Contribution of the least divergent part
		ret += (factor / denom) * (rho_cross ** pole) * ((-pole) ** pos) * mpmath.factorial(pos) * mpmath.gammainc(-pos, a = pole * mpmath.log(rho_cross))

	return (rho_cross ** shift) * ret

def coefficients(polynomial):
	if not "args" in dir(polynomial):
		return [polynomial]
	if polynomial.args == ():
		return [polynomial]

	coeff_list = sorted(polynomial.args, key = extract_power)
	degree = extract_power(coeff_list[-1])

	pos = 0
	ret = []
	for d in range(0, degree + 1):
		if extract_power(coeff_list[pos]) == d:
			if d == 0:
				ret.append(eval_mpfr(coeff_list[0], prec))
			else:
				ret.append(eval_mpfr(coeff_list[pos].args[0], prec))
			pos += 1
		else:
			ret.append(0)
	return ret

def extract_power(term):
	if not "args" in dir(term):
		return 0

	if term.args == ():
		return 0
	elif term.args[1].args == ():
		return 1
	else:
		return int(term.args[1].args[1])

def unitarity_bound(dim, spin):
	if spin == 0:
		return (dim / Integer(2)) - 1
	else:
		return dim + spin - 2

def deepcopy(array):
	ret = []
	for el in array:
		ret.append(list(el))
	return ret

def read_output(name = "mySDP"):
	ret = {}
	out_file = open(name + ".out", 'r')
	for line in out_file:
		(key, delimiter, value) = line.partition(" = ")
		value = value.replace('\n', '')
		value = value.replace(';', '')
		value = value.replace('{', '[')
		value = value.replace('}', ']')
		value = re.sub("([0-9]+\.[0-9]+e?-?[0-9]+)", r"RealMPFR('\1', prec)", value)
		command = "ret['" + key.strip() + "'] = " + value
		exec(command)
	out_file.close()
	return ret

def reshuffle_with_normalization(vector, norm):
		norm_hack = []
		for el in norm:
			norm_hack.append(float(el))

		max_index = norm_hack.index(max(norm_hack, key = abs))
		const = vector[max_index] / norm[max_index]
		ret = []

		for i in range(0, len(norm)):
			ret.append(vector[i] - const * norm[i])

		ret = [const] + ret[:max_index] + ret[max_index + 1:]
		return ret

def short_string(num):
		if abs(num) < tiny:
			return "0"
		else:
			return str(num)

def make_laguerre_points(degree):
		ret = []
		for d in range(0, degree + 1):
			point = -(pi ** 2) * ((4 * d - 1) ** 2) / (64 * (degree + 1) * log(r_cross))
			ret.append(eval_mpfr(point, prec))
		return ret

def get_index(array, element):
	if element in array:
		return array.index(element)
	else:
		return -1

def write_xml(sdp, obj, norm, name = "mySDP"):
	obj = reshuffle_with_normalization(obj, norm)
	laguerre_points = []
	laguerre_degrees = []
	extra_vectors = []
	degree_sum = 0

	# Handle discretely added points
	for p in sdp.points:
		l = get_table_index(sdp, p[0])
		size = len(sdp.table[l])

		outer_list = []
		for r in range(0, size):
			inner_list = []
			for s in range(0, size):
				new_vector = []
				for i in range(0, len(sdp.table[l][r][s].vector)):
					addition = sdp.table[l][r][s].vector[i].subs(delta, p[1])
					for quint in p[2]:
						if quint[3][0] != r or quint[3][1] != s:
							continue
						l_new = get_table_index(sdp, quint[0])
						r_new = quint[2][0]
						s_new = quint[2][1]
						coeff = quint[4]
						coeff *= shifted_prefactor(sdp.table[l_new][0][0].poles, r_cross, quint[1], 0)
						coeff /= shifted_prefactor(sdp.table[l][0][0].poles, r_cross, p[1], 0)
						addition += coeff * sdp.table[l_new][r_new][s_new].vector[i].subs(delta, quint[1])
					new_vector.append(addition)
				inner_list.append(PolynomialVector(new_vector, p[0], sdp.table[l][r][s].poles))
			outer_list.append(inner_list)
		extra_vectors.append(outer_list)
	sdp.table += extra_vectors

	doc = xml.dom.minidom.Document()
	root_node = doc.createElement("sdp")
	doc.appendChild(root_node)

	objective_node = doc.createElement("objective")
	matrices_node = doc.createElement("polynomialVectorMatrices")
	root_node.appendChild(objective_node)
	root_node.appendChild(matrices_node)

	# Here, we use indices that match the SDPB specification
	for n in range(0, len(obj)):
		elt_node = doc.createElement("elt")
		elt_node.appendChild(doc.createTextNode(short_string(obj[n])))
		objective_node.appendChild(elt_node)

	for j in range(0, len(sdp.table)):
		size = len(sdp.table[j])

		matrix_node = doc.createElement("polynomialVectorMatrix")
		rows_node = doc.createElement("rows")
		cols_node = doc.createElement("cols")
		elements_node = doc.createElement("elements")
		sample_point_node = doc.createElement("samplePoints")
		sample_scaling_node = doc.createElement("sampleScalings")
		bilinear_basis_node = doc.createElement("bilinearBasis")
		rows_node.appendChild(doc.createTextNode(size.__str__()))
		cols_node.appendChild(doc.createTextNode(size.__str__()))

		degree = 0
		if j >= len(sdp.bounds):
			delta_min = 0
		else:
			delta_min = sdp.bounds[j]

		for r in range(0, size):
			for s in range(0, size):
				polynomial_vector = reshuffle_with_normalization(sdp.table[j][r][s].vector, norm)
				vector_node = doc.createElement("polynomialVector")

				for n in range(0, len(polynomial_vector)):
					expression = polynomial_vector[n].expand()
					# Impose unitarity bounds and the specified gap
					expression = expression.subs(delta, delta + delta_min).expand()
					coeff_list = coefficients(expression)
					degree = max(degree, len(coeff_list) - 1)

					polynomial_node = doc.createElement("polynomial")
					for coeff in coeff_list:
						coeff_node = doc.createElement("coeff")
						coeff_node.appendChild(doc.createTextNode(short_string(coeff)))
						polynomial_node.appendChild(coeff_node)
					vector_node.appendChild(polynomial_node)
				elements_node.appendChild(vector_node)

		poles = sdp.table[j][0][0].poles
		index = get_index(laguerre_degrees, degree)

		if j >= len(sdp.bounds):
			points = [sdp.points[j - len(sdp.bounds)][1]]
		elif index == -1:
			points = make_laguerre_points(degree)
			laguerre_points.append(points)
			laguerre_degrees.append(degree)
		else:
			points = laguerre_points[index]

		for d in range(0, degree + 1):
			elt_node = doc.createElement("elt")
			elt_node.appendChild(doc.createTextNode(points[d].__str__()))
			sample_point_node.appendChild(elt_node)
			damped_rational = shifted_prefactor(poles, r_cross, points[d], eval_mpfr(delta_min, prec))
			elt_node = doc.createElement("elt")
			elt_node.appendChild(doc.createTextNode(damped_rational.__str__()))
			sample_scaling_node.appendChild(elt_node)

		matrix = []
		if j >= len(sdp.bounds):
			delta_min = mpmath.mpf(delta_min.__str__())
			result = integral(0, delta_min, poles)
			result = 1.0 / mpmath.sqrt(result)
			matrix = mpmath.matrix([result])
		else:
			matrix = sdp.basis[j]

		for d in range(0, (degree // 2) + 1):
			polynomial_node = doc.createElement("polynomial")
			for q in range(0, d + 1):
				coeff_node = doc.createElement("coeff")
				coeff_node.appendChild(doc.createTextNode(matrix[d, q].__str__()))
				polynomial_node.appendChild(coeff_node)
			bilinear_basis_node.appendChild(polynomial_node)

		matrix_node.appendChild(rows_node)
		matrix_node.appendChild(cols_node)
		matrix_node.appendChild(elements_node)
		matrix_node.appendChild(sample_point_node)
		matrix_node.appendChild(sample_scaling_node)
		matrix_node.appendChild(bilinear_basis_node)
		matrices_node.appendChild(matrix_node)
		degree_sum += degree + 1

	# Recognize an SDP that looks overdetermined
	if degree_sum < len(sdp.unit):
		print("Crossing equations have too many derivative components")

	sdp.table = sdp.table[:len(sdp.bounds)]
	xml_file = open(name + ".xml", 'w')
	doc.writexml(xml_file, addindent = "    ", newl = '\n')
	xml_file.close()
	doc.unlink()

def determine_line_spins(key):
	for r in range(len(rows)):
		sig = eval_mpfr(rows[r][0][0], bootstrap.prec)
		eps = eval_mpfr(rows[r][1][0], bootstrap.prec)

		start = time.time()
		start_cpu = time.clock()

		g_tab1 = bootstrap.ConformalBlockTable(3, *key)
		g_tab2 = bootstrap.ConformalBlockTable(3, *(key + [eps-sig, sig-eps, "odd_spins = True"]))
		g_tab3 = bootstrap.ConformalBlockTable(3, *(key + [sig-eps, sig-eps, "odd_spins = True"]))

		tab_list = mixed.convolved_table_list(g_tab1, g_tab2, g_tab3)

		dimension = (4 * len(tab_list[0].table[0].vector)) + (1 * len(tab_list[1].table[0].vector))
		max_dimension = 0
		for tab in tab_list:
			max_dimension = max(max_dimension, len(tab.table[0].vector))

		print("Testing point " + "(" + sig.__str__() + "," + eps.__str__() + ").")
		print("Number of components (dim of PolynomialVectorMatrices) : " + dimension.__str__() + ".")
		print("Kmax should be around (max dimension of convolved block tables): " + max_dimension.__str__() + ".")
		print("It is: " + key[0].__str__() + ".")

		cb_end = time.time()
		cb_end_cpu = time.clock()
		cb_time = datetime.timedelta(seconds = int(cb_end - start))
		cb_cpu = datetime.timedelta(seconds = int(cb_end_cpu - start_cpu))
		print("The calculation of the required conformal blocks has successfully completed.")
		print("Time taken: " + str(cb_time))
		print("CPU_time: " + str(cb_cpu))

		sdp = SDP([sig, eps], tab_list, vector_types = mixed.info)

		table_before = len(sdp.table)

		sdp.bounds = [0.0] * len(sdp.table)
		sdp.options = []
		sdp.basis = [0] * len(sdp.table)

		bad_indices = []

		for l in range(0, len(sdp.table)):
			spin = sdp.table[l][0][0].label[0]
			sdp.bounds[l] = [spin, unitarity_bound(sdp.dim, spin)]

			poles = sdp.table[l][0][0].poles
			delta_min = mpmath.mpf(sdp.bounds[l][1].__str__())
			bands = []
			matrix = []

			degree = 0
			size = len(sdp.table[l])
			for r in range(0, size):
				for s in range(0, size):
					polynomial_vector = sdp.table[l][r][s].vector

					for n in range(0, len(polynomial_vector)):
						expression = polynomial_vector[n].expand()
						degree = max(degree, len(coefficients(expression)) - 1)

			for d in range(0, 2 * (degree // 2) + 1):
				result = integral(d, delta_min, poles)
				bands.append(result)
			for r in range(0, (degree // 2) + 1):
				new_entries = []
				for s in range(0, (degree // 2) + 1):
					new_entries.append(bands[r + s])
				matrix.append(new_entries)

			matrix = mpmath.matrix(matrix)
			try:
				matrix = mpmath.cholesky(matrix, tol = mpmath.mpf(chol_tol))
			except ValueError:
				bad_indices.append(l)
				continue
			else:
				matrix = mpmath.inverse(matrix)
				sdp.basis[l] = [spin, matrix]
		
		bad_spins = []
		for l in bad_indices:
			spin = sdp.table[l][0][0].label[0]
			if spin not in bad_spins:
				bad_spins.append(spin)
		
		sdp.bounds = [couple[1] for couple in sdp.bounds if couple[0] not in bad_spins]
		sdp.table = [polyvecmatrix for polyvecmatrix in sdp.table if polyvecmatrix[0][0].label[0] not in bad_spins]
		sdp.basis = [entry[1] for entry in sdp.basis if isinstance(entry,(list,)) and entry[0] not in bad_spins and isinstance(entry[1], mpmath.matrix)]

		table_after = len(sdp.table)

		good_spins = []
		for l in range(len(sdp.table)):
			spin = sdp.table[l][0][0].label[0]
			if spin not in good_spins:
				good_spins.append(spin)
		
		good_spins.sort()
		bad_spins.sort()

		point = Point(*([sig, eps] + key + [dimension, max_dimension, table_before, table_after, good_spins, bad_spins, cb_time, cb_cpu,]))
		#self.point_table.append(point)
		point.save(mixed.point_file)

sig_num = 20
eps_num = 20

start = [0.516, 1.39]
stop = [0.523, 1.44]

SGE_TASK_ID = int(sys.argv[1])
index = SGE_TASK_ID - 1
lmax = 70

def compute_n(kmax):
	return math.floor(kmax**(0.5))

keys = []
for i in range(15, 61):
	n = int(compute_n(i))
	m = int(n-2)
	keys.append([i, lmax, m, n])

mixed = MixedCorrelator()
mixed.point_file = index.__str__()
rows = mixed.generate_rows(start, stop, sig_num, eps_num)

determine_line_spins(keys[index])
