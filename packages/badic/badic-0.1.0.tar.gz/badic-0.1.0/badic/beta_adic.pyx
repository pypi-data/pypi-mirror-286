# coding=utf8
r"""
Beta-adic tools.

Beta-adic is a way to write numbers in the form

	- :math:`\sum_{i=0}^\infty \beta^i c_i`

where :math:`beta` is a element of a field (for example a complex number),
and the :math:`c_i` are varying in a finite set of digits.
The possible finite sequences of digits are given by a deterministic automaton.

AUTHORS:

- Paul Mercat (2013) -  I2M AMU Aix-Marseille Universite -initial version
- Dominique Benielli (2018) - Labex Archimede - I2M -
  AMU Aix-Marseille Universite - Integration in SageMath

EXAMPLES::

	# Tribonacci
	sage: from badic.beta_adic import BetaAdicSet
	sage: m = BetaAdicSet(x^3-x^2-x-1, {0,1})
	sage: print(m)
	b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 1 state and 2 letters
	sage: ared = m.reduced_words_automaton()
	sage: print(ared)
	DetAutomaton with 4 states and an alphabet of 2 letters
"""
# *****************************************************************************
#  Copyright (C) 2013 Paul Mercat <mercatp@icloud.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#	This code is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty
#	of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
#  See the GNU General Public License for more details; the full text
#  is available at:
#
#				  http://www.gnu.org/licenses/
# *****************************************************************************
from __future__ import division, print_function, absolute_import

from libc.stdlib cimport malloc, free
from libc.stdint cimport uint8_t, uint32_t
from libc.math cimport log, ceil, floor, round, fabs, M_PI as pi_number

from cysignals.signals cimport sig_on, sig_off, sig_check

import numpy as np
cimport numpy as np

from .cautomata cimport DetAutomaton, FreeAutomaton
from .cautomata_generators import DetAutomatonGenerators
from .cautomata import PIL_to_display


from sage.sets.set import Set
from sage.rings.qqbar import QQbar
from sage.rings.padics.factory import Qp
from sage.rings.integer import Integer
from sage.combinat.words.morphism import WordMorphism
from sage.rings.number_field.number_field import NumberField

def test_SDL ():
	TestSDL()

def dev (x, b, n=2000, verb=False):
	"""
	Compute the periodic b-expansion of x of length < n, for the greatest conjugate of b.
	Return [] if not found.
	"""
	K = x.parent()
	try:
		p = max(K.places(), key=lambda p:p(b))
	except:
		p = lambda x:x
	x0 = x
	r = []
	for i in range(n):
		if verb > 0:
			print("i=%s" % i)
		ix = int(floor(p(x)-.0000000001))
		r.append(ix)
		x = (x - ix)*b
		if (x-x0).is_zero(): # == 0:
			break
	else:
		return []
	return r

cdef uint32_t moy(uint32_t a, uint32_t b, float ratio):
	return <uint32_t><uint8_t>((a%256)*(1.-ratio) + (b%256)*ratio) | \
		   (<uint32_t>(<uint8_t>(((a>>8)%256)*(1.-ratio) + ((b>>8)%256)*ratio)))<<8 | \
		   (<uint32_t>(<uint8_t>(((a>>16)%256)*(1.-ratio) + ((b>>16)%256)*ratio)))<<16 | \
		   (<uint32_t>(<uint8_t>((a>>24)*(1.-ratio) + (b>>24)*ratio)))<<24;


cdef double fmax(double a, double b):
	if a < b:
		return b
	return a
	
# plot the Rauzy fractal corresponding to the direction vector d,
# for the C-adic system given by the Cassaigne's algorithm
def plot_Cadic(np.ndarray dv, cs=None, int sx=800, int sy=600,
			   float mx=-2, float my=-2, float Mx=2, float My=2,
			   int n=1000, int nptsmin=50000, int nptsmax=60000,
			   bint verb=False, bint printl=True, bint get_ndarray=False,
			   bint get_bounds=False, bint exchange=False,
			   axes=False, basis=None, colors=None):
	"""
	Plot the Rauzy fractal corresponding to the direction vector ``dv``
	for the C-adic system given by the Cassaigne's algorithm

	INPUT:

		- ``dv``- ndarray array , direction vector
		
		- ``cs`` - list (default ``None``) C-adic sequence to plot

		- ``sx`` int -- (default 800) size of Image direction x

		- ``sy`` int -- (default 60) size of Image direction y

		- ``mx`` float -- (default -2)

		- ``my`` float -- (default -2)

		- ``Mx``  float -- (default 2)

		- ``My`` float  -- (default 2)

		- ``n`` int -- (default 1000)

		- ``nptsmin`` int -- (default 50000)

		- ``nptsmax`` int -- (default 60000)

		- ``verb`` Bool -- (default ''False'')

		- ``printl`` Bool -- (default ''False'')
		
		- ``get_bounds`` Bool -- (default ''False'') if true returns observed bounds of the fractals

		- ``exchange`` Bool -- (default ''False'') draw the domains after exchange
		
		- ``axes`` Bool -- (default ''False'') plot the axes
		
		- ``basis`` list -- (default ''None'') orthonormal basis of P
		
		- ``colors`` list -- (default ''None'') list of colors for each letter and for the axes
		
		OUTPUT:

		Plot the Rauzy fractal corresponding to the direction vector dv.

		EXAMPLES::

			sage: from badic.beta_adic import *
			sage: import numpy as np
			sage: plot_Cadic(np.array((random(), random(), random())))	  # random

	"""
	cdef np.ndarray l, d, im, t2
	cdef int i, j, k, u, nA, i0, e, e0, npts, su, rsu
	cdef uint32_t x, y
	cdef uint32_t color
	cdef float fx, fy
	cdef float xmin = Mx, xmax=mx, ymin=My, ymax=my;
	cdef float f = (<float>sx)/(Mx-mx);

	npts = 0
	color = 255 << 24
	if colors is None:
		colors = [255 | 255 << 24, 255 << 8 | 255 << 24, 255 << 16 | 255 << 24, 255 << 24]
	
	dv = dv/sum(dv) # normalize
	d = np.empty(3, dtype=np.longdouble)
	d[0] = <long double>dv[0]
	d[1] = <long double>dv[1]
	d[2] = <long double>dv[2]
	print("d=%s" % d)
	from sage.combinat.words.morphism import WordMorphism
	s = WordMorphism('a->a,b->ac,c->b')
	t = WordMorphism('a->b,b->ac,c->c')
	auts = DumontThomas(s, proj=False)
	autt = DumontThomas(t, proj=False)
	if auts.states != autt.states:
		raise RuntimeError("Different sets of states !!!")
	Al = ['a','b','c']
	if verb:
		print(auts.states)
	pm = [auts.states.index(a) for a in Al] # permutation of pieces
	if verb:
		print("pm = %s" % pm)
	aut = [auts, autt]
	A = [np.array(a) for a in auts.alphabet]
	nA = len(A)
	#if autt.alphabet != A:
	#	raise RuntimeError("The two Dumont-Thomas automata must have the same alphabet !")
	ms = s.incidence_matrix()
	mt = t.incidence_matrix()
	if verb:
		print("ms=%s"%ms)
		print("mt=%s"%mt)
	msi = (ms**(-1)).numpy()
	mti = (mt**(-1)).numpy()
	if verb:
		print("msi=%s"%msi)
		print("mti=%s"%mti)
	lm = [ms.numpy(), mt.numpy()]
	if basis is None:
		# compute an orthonormal basis
		from sage.functions.other import sqrt
		# compute an orthonormal basis
		v1 = np.array([1, -1, 0])
		v2 = np.array([1, 0, -1])
		v1 = v1/sqrt(sum([t*t for t in v1]))
		v2 = v2 - (v2.dot(v1))*v1
		v2 = v2/sqrt(sum([t*t for t in v2]))
	else:
		v1 = np.array(basis[0])
		v2 = np.array(basis[1])
		
	def proj(t):
		t2 = np.empty(3, dtype=np.longdouble)
		t2[0] = <long double>t[0]
		t2[1] = <long double>t[1]
		t2[2] = <long double>t[2]
		t2 -= sum(t2)*dv
		return (t2.dot(v1), t2.dot(v2)) #((t2.dot(v1) - mx)*f, (t2.dot(v2) - my)*f)
	
	# Cassaigne's algorithm
	m = np.identity(3, dtype=int)
	v0 = np.zeros(3, dtype=int)
	v0[0] = 1
	if cs is None:
		l = np.empty(n, dtype=np.int8)
		su = 0
		for i in range(n):
			if d[0] > d[2]:
				d = msi.dot(d)
				l[i] = 0
			else:
				d = mti.dot(d)
				l[i] = 1
			m = m.dot(lm[l[i]])
			rsu = su
			su = sum(m.dot(v0))
			if rsu > nptsmin:
				n = i
				break
			if su > nptsmax:
				n = i
				break
			d = d/sum(d)
			if verb:
				print("d=%s" % d)
	else:
		if n < len(cs):
			cs = list(cs)[:n]
		l = np.array(cs, dtype=np.int8)
		n = len(cs)
		for i in range(n):
			m = m.dot(lm[l[i]])
	if verb or printl:
		print("n=%s, l=%s"%(n, l[:n]))
	# Draw the Rauzy fractal
	im = np.empty([sy, sx], dtype=np.dtype(
		(np.uint32, {'r': (np.uint8, 0), 'g': (np.uint8, 1),
					 'b': (np.uint8, 2), 'a': (np.uint8, 3)})))
	# im.fill(0) #fill the image with transparent
	im.fill(255 | 255 << 8 | 255 << 16 | 0 << 24)  # fill with white transparent

	if verb:
		print("A=%s" % A)
		print("nA=%s" % nA)

	p = [(np.zeros(3, dtype=int), 0, 0)]
	if exchange:
		mi = np.identity(3, int)
	while len(p) > 0:
		k = len(p)-1
		u = l[n-k-1]
		# print("k=%s"%k)
		t, i, e = p[-1]
		# print("t=%s, i=%s, e=%s"%(t, i, e))
		if k == n:
			e = pm[e]
			if e > 2:
				raise RuntimeError("e=%s !!!" % e)
			# we draw the point t
			# print(t)
			if exchange:
				t += mi[e]
			(fx,fy) = proj(t)
			if fx < xmin:
				xmin = fx;
			if fx > xmax:
				xmax = fx;
			if fy < ymin:
				ymin = fy;
			if fy > ymax:
				ymax = fy;
			fx = (fx - mx)*f #sx/(Mx-mx)
			fy = (fy - my)*f #sy/(My-my)
			x = <uint32_t> fx
			y = <uint32_t> fy
			if verb:
				print(t)
				print(fx, fy)
				print(x, y)
				# print("")
			if x < sx and y < sy:
				if x+1 < sx and y+1 < sy:
					im[y, x] = moy(im[y, x], colors[e], (1.-fx+x)*(1.-fy+y))
					im[y, x+1] = moy(im[y, x+1], colors[e], (fx-x)*(1.-fy+y))
					im[y+1, x] = moy(im[y+1, x], colors[e], (1.-fx+x)*(fy-y))
					im[y+1, x+1] = moy(im[y+1, x+1], colors[e], (fx-x)*(fy-y))
				else:
					im[y, x] = colors[e]
			npts += 1
			# increment
			# print("increment...")
			while True:
				t, i, e = p.pop()
				k = len(p)
				if k == 0:
					break
				t0, i0, e0 = p[-1]
				u = l[n-k]
				# print("k=%s, u=%s, t=%s, i=%s, e=%s"%(k, u, t, i, e))
				while True:
					i0 += 1
					if i0 == nA or aut[u].succ(e0, i0) != -1:
						break
				# print("i=%s"%i)
				if i0 != nA:
					p[-1] = (t0, i0, e0)
					p.append((lm[u].dot(t0)+A[i0], 0, aut[u].succ(e0, i0)))
					break
		else:
			i = 0
			while i < nA and aut[u].succ(e, i) == -1:
				i += 1
			# print("starting i=%s k=%s u=%s t=%s e=%s"%(i, k, u, t, e))
			p[-1] = (t, i, e)
			p.append((lm[u].dot(t)+A[i], 0, aut[u].succ(e, i)))
		#for j2, (m2, t2, i2, e2) in enumerate(p):
			#print("%s : m=%s, t=%s, i=%s, e=%s"%(j2, m2, t2, i2, e2))
	lp = [proj(np.array(m[:,i])) for i in range(3)]
	dx = set([x1-x2 for x1,y1 in lp for x2,y2 in lp])
	dy = set([y1-y2 for x1,y1 in lp for x2,y2 in lp])
	dm = max(max(dx), max(dy))*f
	if printl:
		print("%s pts computed." % npts)
		print("precision : about %.2f pixel" % dm)
		print(m)
	if axes:
		fx = -mx*f #sx/(Mx-mx);
		fy = -my*f #sy/(My-my);
		for i in range(-3,4):
			for j in range(-3,4):
				x = <uint32_t> (fx+i+.5);
				y = <uint32_t> (fy+j+.5);
				if x >= 0 and x < sx and y >= 0 and y < sy and i*i+j*j < 9:
					im[y, x] = colors[3];
	if get_ndarray:
		return im
	from PIL import Image
	if get_bounds:
		return PIL_to_display(Image.fromarray(im, 'RGBA')), ((xmin, xmax), (ymin, ymax))
	else:
		return PIL_to_display(Image.fromarray(im, 'RGBA'))


# plot the Rauzy fractal corresponding to the direction vector d,
# for the C-adic system given by the Cassaigne's algorithm
def plot_Cadic2(np.ndarray dv, int sx=800, int sy=600,
				float mx=-2, float my=-2, float Mx=2, float My=2,
				int n=40, bint verb=False, bint printl=True):
	cdef np.ndarray l, d, im
	cdef int i, j, k, u, nA, i0, e, e0, npts
	cdef uint32_t x, y
	cdef uint32_t color
	cdef float fx, fy

	npts = 0
	color = 255 << 24
	d = np.empty(3, dtype=float)
	d[0] = <float>dv[0]
	d[1] = <float>dv[1]
	d[2] = <float>dv[2]
	from sage.combinat.words.morphism import WordMorphism
	s = WordMorphism('a->a,b->ac,c->b')
	t = WordMorphism('a->b,b->ac,c->c')
	auts = DumontThomas(s, proj=False).mirror()
	autt = DumontThomas(t, proj=False).mirror()
	aut = [auts, autt]
	A = [np.array(a) for a in auts.alphabet]
	nA = len(A)
	# if autt.alphabet != A:
	#	raise RuntimeError("The two Dumont-Thomas automata must have the same alphabet !")
	ms = s.incidence_matrix()
	mt = t.incidence_matrix()
	if verb:
		print("ms=%s" % ms)
		print("mt=%s" % mt)
	msi = (ms**(-1)).numpy()
	mti = (mt**(-1)).numpy()
	if verb:
		print("msi=%s" % msi)
		print("mti=%s" % mti)
	lm = [ms.numpy(), mt.numpy()]
	# compute an orthonormal basis
	v1 = np.array([1,-1,0])
	v2 = np.array([1,0,-1])
	v1 = v1 - v1.dot(d)/d.dot(d)*d
	v2 = v2 - v2.dot(d)/d.dot(d)*d
	from sage.functions.other import sqrt
	v1 = v1/sqrt(v1.dot(v1))
	v2 = v2/sqrt(v2.dot(v2))
	v2 = v2 - v1.dot(v2)*v1
	# Cassaigne's algorithm
	l = np.empty(n, dtype=np.int8)
	for i in range(n):
		if d[0] > d[2]:
			d = msi.dot(d)
			l[i] = 0
		else:
			d = mti.dot(d)
			l[i] = 1
		d = d/sum(d)
		if verb:
			print("d=%s" % d)
	if verb or printl:
		print("l=%s" % l)
	# Draw the Rauzy fractal
	im = np.empty([sy, sx], dtype=np.dtype(
		(np.uint32, {'r': (np.uint8, 0), 'g': (np.uint8, 1),
					 'b': (np.uint8, 2), 'a': (np.uint8, 3)})))
	# im.fill(0) #fill the image with transparent
	im.fill(255 | 255 << 8 | 255 << 16 | 255 << 24)  # fill with white

	if verb:
		print("A=%s" % A)
		print("nA=%s" % nA)

	p = [(np.identity(3, dtype=int), np.zeros(3, dtype=int), 0, 0)]
	while len(p) > 0:
		k = len(p)-1
		u = l[k]
		#print("k=%s"%k)
		m, t, i, e = p[-1]
		#print("t=%s, i=%s, e=%s"%(t, i, e))
		if k == n-1:
			#we draw the point t
			#print(t)
			fx = (t.dot(v1) - mx)*sx/(Mx-mx)
			fy = (t.dot(v2) - my)*sy/(My-my)
			x = <uint32_t>fx
			y = <uint32_t>fy
			if verb:
				print(t)
				print(fx,fy)
				print(x,y)
				#print("")
			if x < sx and y < sy:
				#if x+1 < sx and y+1 < sy:
				#	im[y,x] = moy(im[y,x], color, (1.-fx+x)*(1.-fy+y))
				#	im[y,x+1] = moy(im[y,x+1], color, (fx-x)*(1.-fy+y))
				#	im[y+1,x] = moy(im[y+1,x], color, (1.-fx+x)*(fy-y))
				#	im[y+1,x+1] = moy(im[y+1,x+1], color, (fx-x)*(fy-y))
				#else:
				im[y,x] = color
			npts += 1
			#increment
			#print("increment...")
			while True:
				m, t, i, e = p.pop()
				k = len(p)
				if k == 0:
					break
				m0, t0, i0, e0 = p[-1]
				u = l[k-1]
				nA = aut[u].n_succs(e0)
				# print("k=%s, u=%s, t=%s, i=%s, e=%s"%(k, u, t, i, e))
				while True:
					i0 += 1
					if i0 == nA or aut[u].succ(e0, i0) != -1:
						break
				# print("i=%s"%i)
				if i0 != nA:
					p[-1] = (m0, t0, i0, e0)
					p.append((m, t0+m0.dot(A[i0]), 0, aut[u].succ(e0, i0)))
					break
		else:
			i = 0
			nA = aut[u].n_succs(e)
			while i < nA and aut[u].succ(e, i) == -1:
				i += 1
			# print("starting i=%s k=%s u=%s t=%s e=%s"%(i, k, u, t, e))
			p[-1] = (m, t, i, e)
			p.append((m.dot(lm[u]), lm[u].dot(t)+A[i], 0, aut[u].succ(e, i)))
		# for j2, (m2, t2, i2, e2) in enumerate(p):
			# print("%s : m=%s, t=%s, i=%s, e=%s"%(j2, m2, t2, i2, e2))
	print("%s pts computed." % npts)
	from PIL import Image
	return PIL_to_display(Image.fromarray(im, 'RGBA'))


# compute the p-adic absolute value
def absp(c, p, d):
	"""
	Computation of the p-adic absolute value.

	INPUT:

	- ``c`` -- the algebraic number for which we compute the absolute value

	- ``p`` -- the prime number

	- ``d`` -- the degree

	OUTPUT:

	The p-adic absolute value.

	TESTS:

		sage: absp(1, 2, 3) # not implemented

	"""
	return ((c.polynomial())(p).norm().abs())**(1/d)

def insert(e, l):
	"""
	Insert element e in list l with decreasing order w.r.t. e[0]
	Used in domain_translation_iterator()
	"""
	#print("insert %s %s" % (e,l))
	if len(l) == 0:
		return [e]
	if len(l) == 1:
		if l[0][0] < e[0]:
			return [e, l[0]]
		else:
			return [l[0], e]
	m = len(l)//2
	if l[m][0] > e[0]:
		return l[:m]+insert(e, l[m:])
	return insert(e, l[:m])+l[m:]

cdef getElement(e, Element r, int n):
	cdef j
	p = e.lift()
	for j in range(n):
		r.c[j] = p[j]

cdef InfoBetaAdic initInfoBetaAdic(self,
								   Ad, plus=True, nhash=1000003,
								   verb=False) except *:
	b = self.b
	K = b.parent()

	if verb:
		print(K)

	# determine the places to consider
	parch = []
	for p in K.places():  # archimedian places
		if plus:
			if p(b).abs() > 1:
				parch += [p]
		else:
			if p(b).abs() < 1:
				parch += [p]
	pi = K.defining_polynomial()
	from sage.arith.misc import gcd
	# return the polynomial with integer coefficients and capacity 1
	pi = pi / gcd(pi.list())
	if verb:
		print("pi=%s" % pi)
	# list of concerned prime numbers
	lp = (Integer(pi.list()[0])).prime_divisors()
	if verb:
		print("lp=%s" % lp)
	# list of the considered ultrametric places
	pultra = []
	for p in lp:
		# find every places behind p in the field K
		k = Qp(p)
		Kp = k['a']
		a = Kp.gen()
		for f in pi(a).factor():
			kp = f[0].root_field('e')
			if kp == k:
				c = f[0].roots(kp)[0][0]
			else:
				c = kp.gen()
			if verb:
				print("c=%s (abs=%s)" % (c, (c.norm().abs())**(1/f[0].degree())))
			if plus:
				if (c.norm().abs())**(1/f[0].degree()) > 1:
					pultra += [(c, f[0].degree())]
			else:
				if (c.norm().abs())**(1/f[0].degree()) < 1:
					pultra += [(c, f[0].degree())]

	if verb:
		print("spaces: ")
		print(parch)
		print(pultra)

	if (len(pultra) > 0):
		raise ValueError("Not implemented for b algebraic non-integer.")
	# compute the max bound for each absolute value
	Ad = [K(c) for c in Ad]
	if verb:
		print("Ad = %s" % Ad)

	n = K.degree()
	na = len(parch)
	ncmax = len(Ad)
	cdef InfoBetaAdic i
	if verb:
		print("alloc...")
	sig_on()
	i = allocInfoBetaAdic(n, na, ncmax, nhash, verb)
	sig_off()
	cdef int j
	# initialize bn
	if verb:
		print("init bn...")
	getElement(b**n, i.bn, n)
	# initialize b1
	if verb:
		print("init b1...")
	getElement(1/b, i.b1, n)
	# initialize places
	if verb:
		print("init places...")
	for k in range(na):
		for j in range(n):
			i.p[k].c[j] = to_complex(parch[k](b**j))
	# initialize digits and bounds
	if verb:
		print("init digits...")
	initCdInfoBetaAdic(self, &i, Ad=Ad, parch=parch, verb=verb)
	return i

cdef initCdInfoBetaAdic(self, InfoBetaAdic *i, list Ad, list parch, verb=False):
	if verb:
		print("initCdInfoBetaAdic Ad = %s" % Ad)
	m = dict([])
	for p in parch:
		m[p] = max([p(c).abs() for c in Ad])/abs(1.-p(self.b).abs())
	if verb:
		print("bounds : %s" % m)
	# conversion to C
	i.nc = len(Ad)
	if i.nc > i.ncmax:
		raise ValueError("Too much digits : %d > %d max (initialize BetaAdicSet with more digits)."%(i.nc, i.ncmax))
	for j, c in enumerate(Ad):
		getElement(c, i.c[j], i.n)
	for j, p in enumerate(parch):
		i.cM[j] = m[p]**2

cdef Complexe to_complex(c):
	cdef Complexe r
	r.x = c.real()
	r.y = c.imag()
	return r

cdef Color getColor(c):
	if len(c) < 4:
		raise ValueError("Colors must be defined by 4 float numbers between 0 and 1.")
	cdef Color r
	r.r = c[0] * 255
	r.g = c[1] * 255
	r.b = c[2] * 255
	r.a = c[3] * 255
	return r

cdef surface_to_img(Surface s, ep=100):
	from PIL import Image
	# arr = np.empty([s.sy, s.sx], dtype=['uint8', 'uint8', 'uint8', 'uint8'])
	# arr = np.empty([s.sy, s.sx], dtype=[('r', 'uint8'), ('g', 'uint8'),('b', 'uint8'), ('a', 'uint8')])
	# arr = np.zeros([s.sy, s.sx], dtype=[('r', 'uint8'), ('g', 'uint8'),('b', 'uint8'), ('a', 'uint8')])
	if s.sy == 1:
		sy2 = ep
	else:
		sy2 = s.sy
	arr = np.empty([sy2, s.sx], dtype=np.dtype((np.uint32, {'r':(np.uint8,0), 'g':(np.uint8,1), 'b':(np.uint8,2), 'a':(np.uint8,3)})))

#	cdef int x, y
#	cdef Color c
#	for x in range(s.sx):
#		for y in range(s.sy):
#			c = s.pix[x][s.sy - y - 1]
#			#arr[y, x]['r'] = c.r
#			#arr[y, x]['g'] = c.g
#			#arr[y, x]['b'] = c.b
#			arr[y, x] = c.r | c.g << 8 | c.b << 16 | c.a<<24;
	sig_on()
	SurfaceToNumpy (&s, arr)
	sig_off()
	return PIL_to_display(Image.fromarray(arr, 'RGBA'))

cdef Automaton getAutomaton(DetAutomaton a, list A, verb=False):
	cdef int i
	if verb:
		print("getAutomaton %s..." % a)
	cdef DetAutomaton fa
	cdef Automaton aut
	#if isinstance(a, DetAutomaton):
	if set(A).issubset(a.A):
		fa = a.permut(A, verb=verb)
	else:
		fa = a.bigger_alphabet(A)
	aut = fa.a[0]
	# free(fa.a)
	# fa.a = NULL
	aut = CopyAutomaton(aut, aut.n, aut.na);
	return aut
	# else:
	#	raise ValueError("DetAutomaton expected.")


def mahler(pi):
	from sage.rings.qqbar import AA
	from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
	from sage.rings.rational_field import RationalField
	QQ = RationalField()
	R = PolynomialRing(QQ, 'x')
	try:
		pi = R(pi)
	except:
		raise ValueError("The argument must be a polynomial over ZZ")
	pi.leading_coefficient()
	pi *= pi.denominator()
	rr = pi.roots(ring=QQbar)
	p = pi.leading_coefficient()
	for r in rr:
		if r[0] not in AA:
			rr.remove((r[0].conjugate(), r[1]))
		a = abs(r[0])
		if a > 1:
			p *= a
	return p


cdef BetaAdic getBetaAdic(m, prec=53, mirror=False, verb=False):
	from sage.rings.complex_mpfr import ComplexField
	CC = ComplexField(prec)
	cdef BetaAdic b
	a = m.a.prune().minimize()
	if mirror:
		a = a.mirror().determinize().minimize()
	A = a.alphabet
	nA = a.n_letters

	b = NewBetaAdic(nA)
	b.b = to_complex(CC(m.b))
	for i, c in zip(range(b.n), A):
		b.t[i] = to_complex(CC(c))
	b.a = getAutomaton(a, A=A, verb=verb)
	return b

cdef BetaAdic2 getBetaAdic2(BetaAdicSet self, la=None,
							prec=53, mirror=False, verb=False):
	if verb:
		print("getBetaAdic %s" % self)
	from sage.rings.complex_mpfr import ComplexField
	CC = ComplexField(prec)
	cdef BetaAdic2 b
	if la is None:
		la = self.get_la(verb=verb)

	# check that every element of la is a DetAutomaton or convert it
	la = [getDetAutomaton(self, a) for a in la]
	
	# add the automaton of self as first element
	la = [self.a]+la

	# simplify each automaton
	la = [a.prune().minimize() for a in la]

	if mirror:
		la = [a.mirror().determinize().minimize() for a in la]

	if verb:
		print("la=%s" % la)

	A = set()
	for a in la:
		A.update(a.alphabet)
	A = list(A)
	if verb:
		print("A=%s" % A)

	b = NewBetaAdic2(len(A), len(la))
	b.b = to_complex(CC(self.b))
	d = {}
	for i, c in zip(range(b.n), A):
		b.t[i] = to_complex(CC(c))
		d[c] = i
	# automata
	for i in range(len(la)):
		b.a[i] = getAutomaton(getDetAutomaton(self, la[i]), A=A, verb=verb)
	return b

cdef class ImageIn:
	r"""
	This class permits to load an image and test
	if a point is in the image or outside (using transparency).

	INPUT:

	- file_name - The location of the image file.

	EXAMPLE::

		sage: from badic.beta_adic import ImageIn
		sage: ImageIn("SomeImage.png")	  # not tested
		Traceback (most recent call last):
		...
		IOError: [Errno 2] No such file or directory: 'SomeImage.png'

	"""
	cdef np.ndarray img

	def __init__(self, file_name):
		import matplotlib.image as mpimg
		self.img = mpimg.imread(file_name)

	def __repr__(self):
		if self.img.ndim < 2:
			raise RuntimeError("the number of dimensions must be at least two")
		return "Image of size %sx%s" % (self.img.shape[1], self.img.shape[0])

	def __contains__(self, p):
		cdef int x,y,w,h
		if self.img.ndim < 2:
			raise RuntimeError("the number of dimensions must be at least two")
		h = self.img.shape[0]
		w = self.img.shape[1]
		from sage.rings.complex_mpfr import ComplexField
		CC = ComplexField(53)
		try:
			p = CC(p)
			x = p.real
			y = p.imag
		except:
			x,y = p
		if x < 0 or y < 0 or x >= w or y >= h:
			return False
		return self.img[y][x][3] > .5

	@property
	def img(self):
		return self.img

	def height(self):
		if self.img.ndim < 1:
			raise RuntimeError("the number of dimensions must be at least one")
		return self.img.shape[0]

	def width(self):
		if self.img.ndim < 2:
			raise RuntimeError("the number of dimensions must be at least two")
		return self.img.shape[1]


def getDetAutomaton(self, a):
	if type(a) is BetaAdicSet:
		if self.b != a.b:
			raise ValueError("The two beta-adic sets must have the same " +
							 "b (here %s != %s)." % (self.b.minpoly(), a.b.minpoly()))
		a = a.a
	else:
		try:
			a = DetAutomaton(a)
		except Exception:
			raise ValueError("The argument a must be a BetaAdicSet or an automaton.")
	return a


def get_beta_adic (b, a):
	r"""
	Return a BetaAdicSet from a and algebraic number b.
	"""
	if type(a) is DetAutomaton:
		return BetaAdicSet(b, a)
	return a

cdef class BetaBase:
	r"""
	The purpose of this class is just to write more conveniently some computations.
	It is used in the computation of a substitution describing a BetaAdicSet.
	"""

	def __init__(self, b):
		if type(b) == BetaAdicSet:
			self.m = b
			self.b = b.b
		else:
			self.m = BetaAdicSet(b, DetAutomaton(None))
			self.b = self.m.b

	@property
	def b(self):
		return self.b

	def Proj(self, DetAutomaton a, DetAutomaton b, DetAutomaton ap, DetAutomaton bp, t=0, m=1, closure=False, arel=None):
		self.m.a = a
		return self.m.proj(b, pls=ap, plo=bp, t=-t, m=m, closure=closure, arel=arel)

	def relations_automaton(self, t=0, m=1, bint isvide=False, list Ad=None, list A=None, list B=None,
							 bint couples=False, bint ext=False, bint mirror=False, bint keep_labels=False,
							 bint prune=True, int nhash=1000003, int prec=53, int algo=1, int coeff=1,
							 float margin=.00000001, bint verb=False):
		r"""
		Assume that beta is an algebraic integer.
		Compute the relation automaton of the beta-adic set
		(also called "zero automaton").
		It is the minimal deterministic automaton that recognizes
		the set of words a_0 a_1 ... a_n in Ad^* such that
		:math:`a_0 + beta*a_1 + ... + beta^n*a_n = 0`.
		If couples is True, then it describes the set of words over AxB
		:math:`(a_0, b_0) (a_1, b_1) ... (a_n, b_n)` such that
		:math:`a_0 + beta*a_1 + ... + beta^n*a_n = b_0 + beta*b_1 + ... + beta^n*b_n`.

		If ext is True, it describes the set of words that can be prolongated to an infinite relation
		in the contracting space (which is the product of copies of R, C and p-adic spaces corresponding to
		places of the number field for which beta has an absolute value less than one).

		 INPUT:

		- ``t`` -  algebraic number (default: ``0``) the translation of one of the side

		- ``m`` - algebraic number (default: ``1``) multiplicative the factor of one of the side 

		- ``isvide`` Boolean - (default: ``False``) If isvide is True,
		  it only checks if the automaton is trivial or not.

		- ``Ad`` - list (default: ``None``)
		  Alphabet of differences A-B where A and B
		  are the alphabets to compare.

		- ``A`` -  (default: ``None``) alphabet on one side
		  (used if Ad is None)

		- ``B`` -  (default: ``None``) alphabet on the other side
		  (used if Ad is None)

		- ``couples``  Boolean - (default: ``False``) If ``True``, the alphabet of the resulting automaton is AxB. If ``False``, it is Ad (=A-B).

		- ``ext``  Boolean - (default: ``False``)
		  If ``True``, compute the automaton that describes infinite relations.

		- ``mirror``  Boolean - (default: ``False``) If ``True``, return the mirror.

		- ``prune`` Boolean - (default: ``True``) Prune the result or not.

		- ``keep_labels`` Boolean - (default: ``False``) - If ``True``, return a DetAutomaton with states labeled by algebraic numbers.
			If ``prune`` is ``True``, labels are losed.

		- ``nhash`` int (default: 1000003) Size of the hash table (only for algo 2).

		- ``prec`` - int (default:53)

		- ``algo`` - int (default: 3) Algorithm used (choose in the set {1,2,3}).

		- ``margin`` - float (default: ``.00000001``) - margin used to compare absolute values to bounds

		- ``verb`` Bool - (default: ``False``)
		  Print informations for debugging.

		OUTPUT:

		A DetAutomaton whose language describe the set of relations.

		EXAMPLES::

			sage: from badic import *
			sage: from badic.beta_adic import BetaBase
			sage: m = BetaBase(1/(1+I))
			sage: m.relations_automaton(A=[0,1,3], B=[0,1,3])
			DetAutomaton with 49 states and an alphabet of 7 letters

			sage: m = BetaAdicSet(1/(1+I), [0,1])
			sage: m.relations_automaton()
			DetAutomaton with 1 state and an alphabet of 4 letters
			sage: m.relations_automaton(ext=True)
			DetAutomaton with 7 states and an alphabet of 4 letters
			sage: m.plot()		  #random

		TESTS::

			sage: from badic import *
			sage: m = BetaBase(x^3-x-1)
			sage: a1 = m.relations_automaton(algo=1, Ad=[-1,0,1])
			sage: a2 = m.relations_automaton(algo=2, Ad=[-1,0,1])
			sage: a3 = m.relations_automaton(algo=3, Ad=[-1,0,1])
			sage: a1.has_same_language_as(a2)
			True
			sage: a2.has_same_language_as(a3)
			True

			sage: arel1 = m.relations_automaton(t=1, algo=1, Ad=[-1,0,1])
			sage: arel2 = m.relations_automaton(t=1, algo=2, Ad=[-1,0,1])
			sage: arel3 = m.relations_automaton(t=1, algo=3, Ad=[-1,0,1])
			sage: arel4 = m.relations_automaton(t=1, algo=3, keep_labels=True, Ad=[-1,0,1])
			sage: arel1.has_same_language_as(arel2)
			True
			sage: arel1.has_same_language_as(arel3)
			True
			sage: arel1.has_same_language_as(arel4)
			True

			sage: m = BetaBase(1/pi)
			sage: m.relations_automaton(Ad=[-1,0,1])
			Traceback (most recent call last):
			...
			ValueError: b must live in a number field!

		"""
		cdef InfoBetaAdic ib
		cdef Automaton a
		cdef Element e
		cdef DetAutomaton r
		cdef bint tb

		if mirror is not None:
			try:
				tb = mirror
			except Exception:
				raise ValueError("mirror=%s must be a Bool."%mirror)

		b = self.b
		K = b.parent()
		if not K.is_field():
			raise ValueError("b must live in a field!")
		if not K.is_exact() or not hasattr(K, 'abs_val'):
			raise ValueError("b must live in a number field!")
		pi = b.minpoly()
		if verb:
			print("minpoly : %s" % pi)
		pi = pi*pi.denominator()
		# alphabet
		if Ad is None:
			if A is None:
				raise ValueError("Alphabets A or Ad undefined !")
			if B is None:
				raise ValueError("Alphabet B or Ad undefined !")
			Ad = list(set([m*a1-b1 for a1 in A for b1 in B]))
		else:
			try:
				list(Ad[0])
				Ad = list(set([m*a1-b1 for a1, b1 in Ad]))
			except Exception:
				pass
		if verb:
			print("Ad=%s" % Ad)
		#if couples:
		#	dAd = dict()
		#	for x in A:
		#		for y in B:
		#			z = K(m*x-y)
		#			if z not in dAd:
		#				dAd[z] = []
		#			dAd[z].append((x,y))
		if ext:
			if algo == 1 and not mirror:
				if verb:
					print("Algo 1 cannot be used with ext=True and mirror=False: change to algo 3.")
				algo = 3
			elif (algo == 3 or algo == 2) and mirror:
				if verb:
					print("Algo 2 or 3 cannot be used with ext=True and mirror=True: change to algo 1.")
				algo = 1
		if verb:
			print("algo=%s, mirror=%s" % (algo, mirror))
		if algo == 1:
			if ext:
				b = 1/b
				pi = b.minpoly()
				pi = pi*pi.denominator()
				mirror = not mirror
			# find absolute values for which b is greater than one
			places = []
			narch = 0
			# archimedian places
			for p in K.places(prec=prec):
				if abs_val(K, p, b) > 1:
					places.append(p)
					narch+=1
			# ultra-metric places
			from sage.arith.misc import prime_divisors
			lc = pi.leading_coefficient()
			for p in prime_divisors(lc):
				for P in K.primes_above(p):
					if abs_val(K, P, b, prec=prec) > 1:
						places.append(P)
			if verb:
				print(places)
			# bounds
			bo = []
			for i, p in enumerate(places):
				labs = [abs_val(K, p, x) for x in Ad]
				modb = abs_val(K, p,b)
				if verb:
					print("labs = %s" % labs)
				if i < narch:
					bo.append(
						coeff*max(
							labs)/(modb - 1.))
				else:
					bo.append(
						coeff*max(
							labs)/modb)
			if verb:
				print("bounds=%s" % bo)
			# compute the automaton
			L = []
			S = [t]  # remaining state to look at
			t0 = t
			d = dict()  # states already seen and their number
			d[t] = 0
			c = 1  # count the states seen
			while len(S) > 0:
				S2 = []
				for s in S:
					for t in Ad:
						ss = b*s + t
						# test if we keep ss
						keep = True
						for p, mm in zip(places, bo):
							if abs_val(K, p, ss) > mm + margin:
								keep = False
								break
						if keep:
							if not ss in d:
								S.append(ss)
								d[ss] = c
								c += 1
							if keep_labels:
								L.append((ss, t, s))
							else:
								L.append((d[ss], t, d[s]))
				S = S2
			if keep_labels:
				r = DetAutomaton(L, A=Ad, i=t0, final_states=[0], avoidDiGraph=True)
			else:
				if 0 in d:
					r = DetAutomaton(L, A=Ad, i=0, final_states=[d[0]], avoidDiGraph=True)
				else:
					r = DetAutomaton(L, A=Ad, i=0, final_states=[], avoidDiGraph=True)
			if verb:
				print("before pruning: %s" % r)
			if mirror:
				r = r.mirror_det()
			if prune:
				if verb:
					print("prune...")
				if ext:
					r = r.prune_inf()
				else:
					r = r.prune()
			if ext:
				r.set_final_states(list(range(r.a.n)))
		elif algo == 2:
			ib = initInfoBetaAdic(self, Ad=Ad, plus=False, nhash=nhash, verb=verb)
			sig_on()
			e = NewElement(ib.n)
			sig_off()
			K = self.b.parent()
			t = K(t)
			getElement(t, e, ib.n)
			sig_on()
			a = RelationsAutomatonT(&ib, e, isvide, ext, verb)
			sig_off()
			r = DetAutomaton(None)
			r.a[0] = a
			if verb:
				print("a (%s etats)" % a.n)
				print("Free element...")
			sig_on()
			FreeElement(e)
			sig_off()
			r.A = Ad
			if verb:
				print("Free InfoBetaAdic...")
			sig_on()
			freeInfoBetaAdic(&ib)
			sig_off()
			if isvide:
				return a.na != 0
			if prune:
				if verb:
					print("prune...")
				if ext:
					r = r.prune_inf()
					r.set_final_states(r.states)
				else:
					r = r.prune()
			if mirror:
				r = r.mirror_det()
		else:
			# find absolute values for which b is less than one
			places = []
			narch = 0
			# archimedian places
			for p in K.places(prec=prec):
				if abs_val(K, p, b) < 1:
					places.append(p)
					narch+=1
			# ultra-metric places
			from sage.arith.misc import prime_divisors
			for p in prime_divisors(pi(0)):
				for P in K.primes_above(p):
					if abs_val(K, P, b, prec=prec) < 1:
						places.append(P)
			if verb:
				print(places)
				print("b.minpoly = %s" % pi)
				print("coeff=%s" % coeff)
			# bounds
			bo = []
			for i, p in enumerate(places):
				labs = [abs_val(K, p, x) for x in Ad]
				modb = abs_val(K, p,b)
				if verb:
					print("labs = %s" % labs)
					print("abs_val(b) = %s" % modb)
				if i < narch:
					bo.append(
						coeff*max(
							labs)/(1. - modb))
				else:
					bo.append(
						coeff*max(
							labs))
			if verb:
				print("bounds=%s" % bo)
			# compute the automaton
			L = []
			S = [t]  # remaining state to look at
			d = dict()  # states already seen and their number
			d[t] = 0
			t0 = t
			c = 1  # count the states seen
			while len(S) > 0:
				S2 = []
				for s in S:
					for t in Ad:
						ss = (s - t)/b
						# test if we keep ss
						keep = True
						for p, mm in zip(places, bo):
							if abs_val(K, p, ss) > mm + margin:
								if verb:
									print("|%s|=%s > %s"
										  % (ss, abs_val(K, p, ss), mm))
								keep = False
								break
						if keep:
							if ss not in d:
								S.append(ss)
								d[ss] = c
								c += 1
							#if couples:
							#	for c2 in dAd[t]:
							#		L.append((d[s], c2, d[ss]))
							#else:
							if keep_labels:
								L.append((s, t, ss))
							else:
								L.append((d[s], t, d[ss]))
							# L.append((s, ss, t))
				S = S2
			if keep_labels:
				r = DetAutomaton(L, A=Ad, i=t0, final_states=[0], avoidDiGraph=True)
			else:
				if 0 in d:
					r = DetAutomaton(L, A=Ad, i=0, final_states=[d[0]], avoidDiGraph=True)
				else:
					r = DetAutomaton(L, A=Ad, i=0, final_states=[], avoidDiGraph=True)
			if verb:
				print("before pruning: %s" % r)
			if mirror:
				r = r.mirror_det()
			if prune:
				if verb:
					print("prune...")
				if ext:
					r = r.prune_inf()
				else:
					r = r.prune()
			if ext:
				r.set_final_states(list(range(r.a.n)))
		if couples:
			if A is None or B is None:
				raise ValueError("Alphabets A and B must be defined !")
			d = {}
			for c1 in A:
				for c2 in B:
					c3 = m*c1-c2
					if not c3 in d:
						d[c3] = []
					d[c3].append((c1, c2))
			if verb:
				print(d)
			r = r.duplicate(d, verb=verb)
		return r

cdef getBetaAdicSet(BetaAdicSet self, a):
	if type(a) is BetaAdicSet:
		if self.b != a.b:
			raise ValueError("The two beta-adic sets must have the same b (here %s != %s).", self.b, a.b)
	elif type(a) is not DetAutomaton:
		try:
			a = DetAutomaton(a)
		except Exception:
			raise ValueError("The argument a must be a BetaAdicSet or an automaton.")
		a = BetaAdicSet(self.b, a)
	return a

def get_places(b, Ad=None, prec=53, verb=False):
	r"""
	Get places of the number field of b for which b has modulus >1 and <1.
	Return also bounds for the alphabet Ad if Ad is not None.

	INPUT:

		- ``Ad`` - list (default: ``None``) - alphabet to get bounds

		- ``prec`` - int (default: ``53``) - precision

		- ``verb`` - int (default: ``False``) - if >0, print informations.

	OUTPUT:
		A couple (list of expanding places, list of contracting spaces).
		With bounds if Ad is not None.

	EXAMPLES::

		sage: from badic import *
		sage: m = BetaAdicSet(x^2-x-1, [0,1])
		sage: get_places(m.b)
		[[Ring morphism:
			From: Number Field in b with defining polynomial x^2 - x - 1 with b = -0.618033988749895?
			To:   Real Double Field
			Defn: b |--> 1.618033988749895],
		 [Ring morphism:
			From: Number Field in b with defining polynomial x^2 - x - 1 with b = -0.618033988749895?
			To:   Real Double Field
			Defn: b |--> -0.6180339887498948]]

	"""
	K = b.parent()
	pi = b.minpoly()
	pi = pi*pi.denominator()
	# find absolute values for which b is greater than one
	eplaces = []
	cplaces = []
	# archimedian places
	for p in K.places(prec=prec):
		a = abs(p(b))
		if a > 1:
			if Ad is None:
				eplaces.append(p)
			else:
				labs = [abs(p(x)) for x in Ad]
				eplaces.append( (p, max(labs)/(a - 1)) )
		elif a < 1:
			if Ad is None:
				cplaces.append(p)
			else:
				labs = [abs(p(x)) for x in Ad]
				cplaces.append( (p, max(labs)/(1 - a)) )
		else:
			raise ValueError("The number %s is not hyperbolic !" % b)
	# ultra-metric places
	from sage.arith.misc import prime_divisors
	lc = pi.leading_coefficient()
	for p in prime_divisors(lc):
		for P in K.primes_above(p):
			a = abs_val(K, P, b, prec=prec)
			if a > 1:
				if Ad is None:
					eplaces.append(P)
				else:
					labs = [abs_val(K, P, x) for x in Ad]
					eplaces.append( (P, max(labs)/a) )
	from sage.arith.misc import prime_divisors
	for p in prime_divisors(pi(0)):
		for P in K.primes_above(p):
			a = abs_val(K, P, b, prec=prec)
			if a < 1:
				if Ad is None:
					cplaces.append(P)
				else:
					labs = [abs_val(K, P, x) for x in Ad]
					cplaces.append( (P, max(labs)) )
	return [eplaces,cplaces]

# this function permits to prevent a bug of sage (otherwise it computes the wrong absolute value)
def abs_val(K, v, iota, prec=None):
	r"""
	Return the value `|\iota|_{v}`.

	INPUT:

	- ``K```-- a NumberField
	- ``v`` -- a place of ``K``, finite (a fractional ideal) or infinite (element of ``K.places(prec)``)
	- ``iota`` -- an element of ``K``
	- ``prec`` -- (default: None) the precision of the real field

	OUTPUT:

	The absolute value as a real number

	EXAMPLES::

		sage: K.<xi> = NumberField(x^3-3)
		sage: phi_real = K.places()[0]
		sage: phi_complex = K.places()[1]
		sage: v_fin = tuple(K.primes_above(3))[0]
		sage: from badic.beta_adic import abs_val
		sage: abs_val(K, phi_real, xi^2)
		2.08008382305...

		sage: abs_val(K, phi_complex, xi^2)
		2.08008382305...

		sage: abs_val(K, v_fin, xi^2)
		0.11111111111...
	
	TESTS::
	
		sage: abs_val(K, v_fin, K(0))
		0
	"""
	if iota == 0:
		return 0
	if prec is None:
		prec = 53
	from sage.rings.real_mpfr import RealField
	R = RealField(prec)
	try:
		p = v.smallest_integer()
		iota_ideal = K.ideal(K(iota))
		exponent = - v.residue_class_degree() * iota_ideal.valuation(v)
		return R(p**exponent)
	except AttributeError:
		return R(v(iota).abs())

#def abs_val(K, p, t, prec=None):
#	modt = K.abs_val(p,t, prec=prec)
#	from sage.rings.number_field.number_field import is_real_place
#	if not is_real_place(p):
#		from sage.functions.other import sqrt
#		modt = sqrt(modt)
#	return modt

cdef class BetaAdicSet:
	r"""
	Define a numeration in base b, i.e. set of numbers of the form

		:math:`\sum_{i=0}^\infty \beta^i c_i`

	where :math:`\beta` is an element of a field (for example a complex number),
	and the :math:`c_i` form a word recognized by a deterministic automaton ``a``.

	INPUT:

	- ``b`` -- number, base of the numeration.

	- ``a`` -- DetAutomaton, giving the allowed sequence of digits.


	EXAMPLES::

		sage: from badic.beta_adic import BetaAdicSet
		sage: from badic.cautomata_generators import *
		sage: m1 = BetaAdicSet(3, dag.AnyWord([0, 1, 3]))
		sage: print(m1)
		b-adic set with b root of x - 3, and an automaton of 1 state and 3 letters
		sage: m2 = BetaAdicSet((1 + sqrt(5)) / 2, dag.AnyWord([0, 1]))
		sage: print(m2)
		b-adic set with b root of x^2 - x - 1, and an automaton of 1 state and 2 letters
		sage: b = (x^3-x-1).roots(ring=QQbar)[0][0]
		sage: m3 = BetaAdicSet(b, dag.AnyWord([0, 1]))
		sage: print(m3)
		b-adic set with b root of x^3 - x - 1, and an automaton of 1 state and 2 letters

	"""
	def __init__(self, b, a):
		r"""
		Construction of the b-adic with base ``b`` and automaton ``a``.

		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: from badic.cautomata_generators import *
			sage: m1 = BetaAdicSet(3, dag.AnyWord([0, 1, 3]))
			sage: m1
			b-adic set with b root of x - 3, and an automaton of 1 state and 3 letters
			sage: c = Automaton({0:{1:'0',2:'1',3:'2'}, 2:{5:'1'}},initial_states=[0])
			sage: m3 = BetaAdicSet(m1.b, c)
			sage: m3
			b-adic set with b root of x - 3, and an automaton of 5 states and 3 letters
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: m
			b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 1 state and 2 letters
			sage: m1 = BetaAdicSet(3,[0,1])
			sage: m1
			b-adic set with b root of x - 3, and an automaton of 1 state and 2 letters

		"""
		cdef int i, j
		from sage.rings.complex_mpfr import ComplexField
		CC = ComplexField()
		if b not in CC:
			# raise ValueError("b must be a number.")
			from sage.rings.qqbar import QQ
			from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
			K = PolynomialRing(QQ, 'x')
			try:
				pi = K(b)
				rr = [r[0] for r in pi.roots(ring=QQbar)]
				rrm = [r for r in rr if abs(r) < 1]
				if len(rrm) > 0:
					b = rrm[0]
				else:
					b = rr[0]
			except Exception:
				raise ValueError("b must be a number, or a polynomial over QQ")
		try:
			b = QQbar(b)
			pi = QQbar(b).minpoly()
			K = NumberField(pi, 'b', embedding=b)
			self.b = K.gen()
		except Exception:
			self.b = b

		if type(a) != DetAutomaton:
			try:
				a = DetAutomaton(a)
			except Exception:
				try:
					a = list(a)
				except Exception:
					raise ValueError("a must be an automaton or an iterable.")
				from .cautomata_generators import dag
				a = dag.AnyWord(a)
		self.a = a

		# test if letters of a are in K
		try:
			K = self.b.parent()
			self.a.A = [K(c) for c in self.a.A]
		except Exception:
			raise ValueError("Alphabet %s of the automaton is not in the field %s of b !"%(self.a.A, self.b.parent()))

	def __repr__(self):
		r"""
		Returns the string representation of the BetaAdicSet.

		EXAMPLES::

			sage: from badic.cautomata_generators import *
			sage: from badic.beta_adic import BetaAdicSet
			sage: BetaAdicSet((1+sqrt(5))/2, dag.AnyWord([0, 1]))
			b-adic set with b root of x^2 - x - 1, and an automaton of 1 state and 2 letters
			sage: BetaAdicSet(3, dag.AnyWord([0, 1, 3]))
			b-adic set with b root of x - 3, and an automaton of 1 state and 3 letters


		TESTS::

			sage: from badic.cautomata_generators import *
			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(3/sqrt(2), dag.AnyWord([0, 1]))
			sage: repr(m)
			'b-adic set with b root of x^2 - 9/2, and an automaton of 1 state and 2 letters'

		"""

		from sage.rings.qqbar import QQbar
		if self.b not in QQbar:
			str = "(%s)-adic set with an "%self.b
		else:
			K = self.b.parent()
			from sage.rings.rational_field import QQ
			if K.base_field() == QQ:
				str = "b-adic set with b root of %s, and an "%self.b.minpoly()
			else:
				if K.characteristic() != 0:
					str = "b-adic set with b root of %s (in characteristic %s), and an "%(self.b.minpoly(), K.characteristic())
				else:
					str = "b-adic set with b root of %s, and an "%K.modulus()
		str += "automaton of %s state"%self.a.a.n
		if self.a.a.n > 1:
			str += 's'
		str += " and %s letter" % (self.a.a.na)
		if self.a.a.na > 1:
			str += 's'
		return str

	def string(self):
		r"""
		Return a string that can be evaluated to recover the BetaAdicSet

		OUTPUT:
		Return a string to define a BetaAdicSet, this set can be obtained by the ``use_draw`` method

		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: m1 = BetaAdicSet(3,[0,1])
			sage: m1.string()
			'BetaAdicSet((x - 3).roots(ring=QQbar)[0][0], DetAutomaton([[0], [(0, 0, 0), (0, 0, 1)]], A=[0, 1], i=0, final_states=[0]))'
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: m.string()
			'BetaAdicSet((x^3 - x^2 - x - 1).roots(ring=QQbar)[1][0], DetAutomaton([[0], [(0, 0, 0), (0, 0, 1)]], A=[0, 1], i=0, final_states=[0]))'

		"""
		pi = self.b.minpoly()
		from sage.rings.qqbar import QQbar
		rr = pi.roots(ring=QQbar)
		for i, r in enumerate(rr):
			if r[0] == self.b:
				break
		from sage.rings.rational_field import QQ
		if len([c for c in self.a.A if c not in QQ]) == 0:
			return "BetaAdicSet((%s).roots(ring=QQbar)[%s][0], %s)"%(pi, i, self.a.string())
		else:
			return "m = BetaAdicSet((%s).roots(ring=QQbar)[%s][0], DetAutomaton(None))\nb=m.b\nBetaAdicSet(b, %s)"%(pi, i, self.a.string())

	@property
	def a(self):
		"""
		Get the ``DetAutomaton`` ``a`` of the ``BetaAdicSet``

		OUTPUT:

		``DetAutomaton`` ``a`` attribut

		EXAMPLES::

			sage: from badic.cautomata_generators import *
			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet((1+sqrt(5))/2, dag.AnyWord([0, 1]))
			sage: m.a
			DetAutomaton with 1 state and an alphabet of 2 letters

		"""
		return self.a

	@property
	def b(self):
		"""
		Get the number ``b`` of the ``BetaAdicSet``

		OUTPUT:

		number ``b`` attribut

		EXAMPLES::

			sage: from badic.cautomata_generators import *
			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet((1+sqrt(5))/2, dag.AnyWord([0, 1]))
			sage: m.b
			b

		"""
		return self.b

	def copy(self):
		"""
		return a copy of  the ``BetaAdicSet``

		OUTPUT:

		a ``BetaAdicSet``

		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet((1+sqrt(5))/2, [0, 1])
			sage: m.copy()
			b-adic set with b root of x^2 - x - 1, and an automaton of 1 state and 2 letters

		TESTS::
			
			sage: from badic.beta_adic import BetaAdicSet
			sage: from badic.cautomata_generators import *
			sage: m = BetaAdicSet((1+sqrt(5))/2, dag.AnyLetter([0,1]))
			sage: m2 = m.copy()
			sage: m.a.set_final(0)
			sage: m.a == m2.a
			False

		"""

		return BetaAdicSet(self.b, self.a.copy())

	def mirror(self):
		"""
		Return the beta-adic set with the mirror automaton.

		OUTPUT:

		A ``BetaAdicSet`` with the mirror automaton as attribut ``a``

		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet((1+sqrt(5))/2, [0, 1])
			sage: m.mirror()
			b-adic set with b root of x^2 - x - 1, and an automaton of 1 state and 2 letters

		"""
		return BetaAdicSet(self.b, self.a.mirror())

	def is_included(self, other, pl=None, pls=None, plo=None, t=0, m=1, arel=None, arel0=None, bint closure=False, int verb=False):
		"""
		Determine if the BetaAdicSet m*self+t is included in the BetaAdicSet given by other.

		INPUT:

			- ``other`` - ``BetaAdicSet`` or ``DetAutomaton`` - BetaAdicSet to compare

			- ``pl`` - BetaAdicSet or DetAutomaton (default: ``None``) - projection language
						Allows to make the computation easier if pl is simple enough.

			- ``pls`` - BetaAdicSet or DetAutomaton (default: ``None``) - projection language for left side (self).
						Allows to make the computation easier if pls is simple enough.

			- ``plo`` - BetaAdicSet or DetAutomaton (default: ``None``) - projection language for right side (other).
						Allows to make the computation easier if plo is simple enough.

			- ``arel`` - DetAutomaton (default: ``None``) - relations automaton

			- ``arel0`` - DetAutomaton (default: ``None``) - relations automaton for t=0 and without languages. States are assumed to be labeled by algebraic numbers.

			- ``t`` - algebraic number (default: ``0``) - translation to do to self

			- ``m`` - algebraic number (default: ``1``) - multiplication to do to self

			- ``closure`` - bool (default: ``False``) - test is self is included in the closure of other

			- ``verb`` - int (default: ``False``) - if > 0, display informations for debug.

		OUTPUT:
			A bool.
			``True``  if the BetaAdicSet is included in the BetaAdicSet given
			by a, ``False`` otherwise


		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: m1 = BetaAdicSet(x^3-x^2-x-1, [0,1,2])
			sage: m1.is_included(m)
			False
			sage: m.is_included(m1)
			True

		"""
		cdef BetaAdicSet mp
		other = get_beta_adic(self.b, other)
		if verb > 0:
			print("other=%s" % other)
		K = self.b.parent()
		t = K(t)
		m = K(m)
		mp = other.proj(self, pl=pl, plo=plo, pls=pls, arel=arel, arel0=arel0, t=-t/m, m=1/m, closure=closure, verb=verb-1)
		if verb > 0:
			print("mp = %s" % mp)
		return self.a.included(mp.a)

	def find_invariance (self, pl=None, bint proj=True, int kmax=30, int verb=False):
		r"""
		Find k such that self is b^k-invariant.
		pl is assumed to be b-invariant.

		INPUT:

			- ``pl`` - BetaAdicSet or DetAutomaton (default: ``None``) - language used for projections.
						It must be b-invariant.

			- ``kmax`` - int (default: ``30``) - maximum k to test

			- ``verb`` - int (default: ``False``) - if > 0, print informations.

		OUTPUT:
			An integer.

		EXAMPLES::

			sage: from badic import *
			sage: m = BetaAdicSet(x^3-x^2-x-1, dag.AnyWord([0]).concat(dag.Word([1,0,0,0])).concat(dag.AnyWord([0,1])))
			sage: m.find_invariance()
			1
			sage: m = BetaAdicSet(x^3-x^2-x-1, dag.Word([0,0,0]).concat(dag.AnyWord([0,1])))
			sage: m.find_invariance()
			1
			sage: m = BetaAdicSet(x^3-x^2-x-1, dag.Words([[0,0,0],[1,0,0]]).concat(dag.AnyWord([0,1])))
			sage: m.find_invariance()
			3

		"""
		cdef BetaAdicSet mp
		if pl is not None and proj:
			self = self.proj(pl)
		else:
			self = self.copy()
			self.a.zero_complete_op()
		for k in range(1,kmax+1):
			if verb > 0:
				print("k=%s..." % k)
			if self.is_included(self, m=self.b**k):
				if verb > 0:
					print("k=%s works !!" % k)
				break
		else:
			raise ValueError("k not found ! Try with bigger kmax.")
		return k

	def is_equal_to(self, other, pl=None, pls=None, plo=None, t=0, m=1, arel=None, arel0=None, bint closure=False):
		"""
		Determine if the ``BetaAdicSet`` m*self+t is equal to the given ``BetaAdicSet`` other.

		INPUT:

			- ``other`` - ``BetaAdicSet`` or ``DetAutomaton`` to compare

			
			- ``pl`` - BetaAdicSet or DetAutomaton (default: ``None``) - projection language
						Allows to make the computation easier if pl is simple enough.

			- ``pls`` - BetaAdicSet or DetAutomaton (default: ``None``) - projection language for left side (self).
						Allows to make the computation easier if pls is simple enough.

			- ``plo`` - BetaAdicSet or DetAutomaton (default: ``None``) - projection language for right side (other).
						Allows to make the computation easier if plo is simple enough.

			- ``arel`` - DetAutomaton (default: ``None``) - relations automaton

			- ``arel0`` - DetAutomaton (default: ``None``) - relations automaton for t=0 and without languages. States are assumed to be labeled by algebraic numbers.

			- ``t`` - algebraic number (default: ``0``) - translation to do to self

			- ``m`` - algebraic number (default: ``1``) - multiplication to do to self

			- ``closure`` - bool (default: ``False``) - test is self is included in the closure of other

		OUTPUT:
			A bool.
			``True``  if the BetaAdicSet is equal in the BetaAdicSet given
			by a  ``False`` otherwise
 

		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: m1 = BetaAdicSet(x^3-x^2-x-1, [0,1,2])
			sage: m1.is_equal_to(m)
			False


		"""
		other = getBetaAdicSet(self, other)
		return self.is_included(other, pl=pl, plo=plo, pls=pls, arel=arel, arel0=arel0, t=t, m=m, closure=closure)\
				and other.is_included(self, pl=pl, plo=plo, pls=pls, arel=arel, arel0=arel0, t=-t/m, m=1/m, closure=closure)

	def is_empty(self):
		"""
		Tell if the BetaAdicSet is empty.

		OUTPUT:

		``True``  if the BetaAdicSet is empty in the BetaAdicSet given
		by a  ``False`` otherwise
 

		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: m.is_empty()
			False
			sage: m = BetaAdicSet(3, [])
			sage: m.is_empty()
			True

		TESTS::

			sage: from badic.beta_adic import BetaAdicSet
			sage: from badic.cautomata import DetAutomaton
			sage: m = BetaAdicSet(1/(1+I), DetAutomaton([(0,0,0),(0,1,1)], i=0, final_states=[]))
			sage: m.is_empty()
			True
			sage: m = BetaAdicSet(1/(1+I), DetAutomaton([(0,0,0),(0,1,1)], i=0, final_states=[1]))
			sage: m.is_empty()
			False

		"""
		return self.a.has_empty_language()

#	def _testSDL(self):
#		"""
#		Open a window to test the SDL library used for graphical representation.
#
#		TESTS::
#
#			sage: m3 = BetaAdicSet(1/(1+I), dag.AnyWord([0, 1]))
#			sage: m3._testSDL()
#			Video Mode: 800x600 32 bits/pixel
#		"""
#		sig_on()
#		TestSDL()
#		sig_off()

	def get_la(self, bint verb=False):
		"""
		Return a list of automata corresponding to each final state of the automaton.
		For each state of self, give a copy of self but whose set of final states is this state.

		INPUT:

		-``verb`` -- Bool (default ''False'') - set to ''True'' for verbose mode

		OUTPUT:
		Return a list of automata.

		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: from badic.cautomata_generators import *
			sage: m=BetaAdicSet((1+sqrt(5))/2, dag.AnyWord([0, 1]))
			sage: m.get_la()
			[DetAutomaton with 1 state and an alphabet of 2 letters]
			
		 #. plot a Rauzy fractal
			sage: from badic.beta_adic import DumontThomas
			sage: m=DumontThomas(WordMorphism('a->ab,b->ac,c->a'))
			sage: la = m.get_la()
			sage: la
			[DetAutomaton with 3 states and an alphabet of 2 letters,
			 DetAutomaton with 3 states and an alphabet of 2 letters,
			 DetAutomaton with 3 states and an alphabet of 2 letters]
			sage: m.plot_list(la)	   #random
		"""
		cdef DetAutomaton a = self.a.copy()
		# compute la
		la = []
		for v in range(a.a.n):
			a.set_final_states([v])
			la.append(a.copy())
		return la

#	def points_exact(self, n=None, i=None):
#		r"""
#		Returns a set of exacts values (in the number field of b)
#		corresponding to points of the b-adic set for words of length at most ``n``.
#
#		INPUT:
#
#		- ``n`` - integer (default: ``None``)
#		  The number of iterations used to plot the fractal.
#		  Default values: between ``5`` and ``16`` depending on the number
#		  of generators.
#
#		- ``i`` - integer (default: ``None``)
#		  State of the automaton of self taken as the initial state .
#
#		OUTPUT:
#
#			List of numbers, given with exact values.
#
#		EXAMPLES::
#
#			#. The dragon fractal::
#			sage: e = QQbar(1/(1+I))
#			sage: m=BetaAdicSet(e, dag.AnyWord([0, 1]))
#			sage: print(m)
#			b-adic set with b root of x^2 - x + 1/2, and an automaton of 1 state and 2 letters
#			sage: P = m.points_exact()
#			age: len(P)
#			65536
#			sage: P = m.points_exact(i=0)
#			sage: len(P)
#			65536
#		"""
#		K = self.K
#		b = self.b
#		a = self.a
#		A = a.alphabet
#		ng = a.n_letters
#
#		if i is None:
#			i = a.initial_state
#
#		if n is None:
#			if ng == 2:
#				n = 16
#			elif ng == 3:
#				n = 9
#			else:
#				n = 5
#
#		if n == 0:
#			return [0]
#		else:
#			orbit_points = set()
#			V = set([v for c in A for v in [a.succ(i, c)] if v != -1])
#			orbit_points0 = dict()
#			for v in V:
#				orbit_points0[v] = self.points_exact(n=n-1, i=v)
#			for c in A:
#				v = a.succ(i, c)
#				if v is not None:
#					orbit_points.update([b*p+c for p in orbit_points0[v]])
#		return orbit_points

	def user_draw(self, n=None,
				  int sx=800, int sy=600, bint ajust=True, int prec=53, color=(0, 0, 0, 255),
				  bint simplify=True, bint mirror=False, bint only_aut=False, bint verb=False):
		r"""
		Display a window where the user can draw a b-adic set based on the current b-adic set.
		Use keyboard p to reduce the size of the pen and the keyboard m to increse.
		Draw the figure with the the mouse and click to record the shape.

		INPUT:

		- ``n`` - integer (default: ``None``)
		  The number of iterations used to plot the fractal.
		  Default values: between ``5`` and ``16`` depending on the number
		  of generators.

		- ``sx`` -- integer (default: ``800``) - width of the window

		- ``sy`` -- integer (default: ``600``) - height of the window

		- ``ajust``  -- Boolean (default ``True``) - If True, change the zoom in order to fit the window.

		- ``prec`` -- integer (default: ``53``) - precision of computed values

		- ``color`` -- tuple (default: (0, 0, 0, 255)) - color in RGBA values

		- ``simplify`` -- (default: ``True``) - If True, minimize the result

		- ``only_aut`` -- (default: ``False``) - If True return a DetAutomaton, otherwise return a BetaAdicSet

		- ``verb`` -- (default ``False``) - set to ``True`` for verbose mod

		OUTPUT:

		A b-adic set, corresponding to what has been drawn by the user. Or only the automaton if only_aut was True.

		EXAMPLES::

			#. Draw a BetaAdicSet from the dragon fractal::

				sage: from badic.beta_adic import BetaAdicSet
				sage: m = BetaAdicSet(1/(1+I), [0, 1])
				sage: P = m.user_draw()	 # not tested (need the intervention of the user)
				sage: P.string()			# not tested

			#. Draw a BetaAdicSet from a Rauzy fractal::

				sage: from badic.beta_adic import DumontThomas
				sage: m = DumontThomas(WordMorphism('a->ab,b->ac,c->a')).mirror()
				sage: P = m.user_draw()	 # not tested (need the intervention of the user)
				sage: P.plot()			  # not tested

		"""
		cdef BetaAdic b
		cdef Automaton a
		cdef DetAutomaton r
		b = getBetaAdic(self, prec=prec, mirror=mirror, verb=verb)
		# if verb:
		#	printAutomaton(b.a)
		# dessin
		cdef Color col
		col.r = color[0]
		col.g = color[1]
		col.b = color[2]
		col.a = color[3]
		if n is None:
			n = -1
		if HaySDL ():
			spr = self.a.prune().spectral_radius()
			sig_on()
			a = UserDraw(b, sx, sy, n, ajust, col, spr, verb)
			sig_off()
		else:
			raise NotImplementedError("This function does not exists in this version of Sage, because it uses the library SDL2. To use this function, you need to install the library SDL2 on your system and then reinstall the package badic.")
		r = DetAutomaton(None)
		r.a[0] = a
		r.A = self.a.A
		r.S = list(range(a.n))
		if simplify:
			r = r.minimize()
		if only_aut:
			return r
		else:
			return BetaAdicSet(self.b, r)

	def draw_zoom(self, n=None, int sx=800, int sy=600,
				  bint ajust=True, int prec=53, color=(0, 0, 0, 255),
				  int nprec=4, bint mirror=False, bint verb=False):
		r"""
		Display the BetaAdicSet in a window, with possibility for the user to zoom in.
		Use 'p' to zoom in, 'm' to zoom out, the arrows to translate the view, and 'Esc' to quit.
		You can also select a zone to zoom in with the mouse.

		INPUT:

		- ``n`` - integer (default: ``None``)
		  The number of iterations used to plot the fractal.
		  Default values: between ``5`` and ``16`` depending on the number
		  of generators.

		- ``sx``  -- (default 800)

		- ``sy``  -- (default 600)

		- ``ajust``  -- (default ``True``) If ``True``, change the zoom in order to fit the window.

		- ``prec``  precision of computed values -- (default: ``53``)

		- ``color`` tuple of color in RGB values -- (default: (0, 0, 0, 255))

		- ``nprec`` int -- (default 4) - additional iterations for the drawing (if ``n`` is None).

		- ``mirror`` Bool -- (default ``False) set to ``True`` to use the mirror of the automaton

		- ``verb`` -- (default ``False``) set to ``True`` for verbose mod

		OUTPUT:

		A word that corresponds to the place where we draw.

		EXAMPLES::

			#. The dragon fractal::

				sage: from badic.beta_adic import BetaAdicSet
				sage: m = BetaAdicSet(1/(1+I), [0, 1])
				sage: w = m.draw_zoom()	 # not tested (need the intervention of the user)


			#. Zoom in a complicated Rauzy fractal

				sage: from badic.beta_adic import DumontThomas
				sage: s = WordMorphism('1->2,2->3,3->12')
				sage: m = DumontThomas(s).mirror(); m
				b-adic set with b root of x^3 - x - 1, and an automaton of 4 states and 2 letters
				sage: m.draw_zoom()		 # not tested (need the intervention of the user)

		"""
		cdef BetaAdic b
		b = getBetaAdic(self, prec=prec, mirror=mirror, verb=verb)
		# dessin
		cdef int *word
		cdef Color col
		cdef int i
		col.r = color[0]
		col.g = color[1]
		col.b = color[2]
		col.a = color[3]
		if n is None:
			n = -1
		#try:
		if HaySDL():
			spr = self.a.prune().spectral_radius()
			sig_on()
			word = DrawZoom(b, sx, sy, n, ajust, col, nprec, spr, verb)
			sig_off()
		else:
			raise NotImplementedError("This function does not exists in this version of Sage, because it uses the library SDL2. To use this function, you need to install the library SDL2 on your system and then reinstall the package badic.")
			#recompile Sage from the sources where you include the ticket https://trac.sagemath.org/ticket/21072.")
		res = []
		if word is not NULL:
			for i in range(1024):
				if word[i] < 0:
					break
				res.append(self.a.alphabet[word[i]])
			res.reverse()
		return res

	def plot(self, n=None, int sx=800, int sy=600,
			 bint ajust=True, int prec=53, color=(0, 0, 0, 255),
			 int nprec=4, bint mirror=False, bint verb=False):
		r"""
		Draw the beta-adic set.

		INPUT:

		- ``n`` - integer (default: ``None``)
		  The number of iterations used to plot the fractal.
		  If None, choose the number of iteration depending on the modulus of b
		  and the spectral radius of the automaton.

		- ``place`` - place of the number field of beta (default: ``None``)
		  The place used to evaluate elements of the number field.

		- ``sx`` -- int (default: 800) - dimensions of the resulting in x dimension

		- ``sy`` -- int (default : 600) - dimensions of the resulting
		  in y dimension image

		- ``ajust`` -- Bool (default: ``True``) - adapt the drawing
		  to fill all the image, with ratio 1 

		- ``prec`` - int (default: ``53``) - precision of returned values

		- ``color`` - list of four integers between 0
		  and 255 (RGBA format, default: ``(0,0,0,255)``) Color of the drawing.

		- ``mirror`` Bool -- (default ``False``) - set to ``True`` to use the mirror of the automaton

		- ``nprec`` int -- (default 4) - additionnal iterations (if n is ``None``)

		- ``verb`` - Bool (default: ``False``)
		  Print informations for debugging.

		OUTPUT:

			A Graphics object.

		EXAMPLES::

			#. The dragon fractal::

				sage: from badic.beta_adic import BetaAdicSet
				sage: from badic.cautomata_generators import *
				sage: m = BetaAdicSet(1/(1+I), dag.AnyWord([0,1]))
				sage: m.plot()									  # random

			#. Another dragon fractal::

				sage: from badic.beta_adic import BetaAdicSet
				sage: from badic.cautomata_generators import *
				sage: m = BetaAdicSet(2*x^2+x+1, dag.AnyWord([0,1]))
				sage: m.plot()									  # random

			#. The Rauzy fractal of the Tribonacci substitution::

				sage: from badic.beta_adic import DumontThomas
				sage: s = WordMorphism('1->12,2->13,3->1')
				sage: m = DumontThomas(s).mirror()
				sage: m.plot()									  # random

			#. The Rauzy fractal of the flipped Tribonacci substitution::

				sage: from badic.beta_adic import DumontThomas
				sage: s = WordMorphism('1->12,2->31,3->1')
				sage: m = DumontThomas(s).mirror()
				sage: m.plot()									  # random

			#. A non-Pisot Rauzy fractal::

				sage: from badic.beta_adic import DumontThomas
				sage: s = WordMorphism({1:[3,2], 2:[3,3], 3:[4], 4:[1]})
				sage: m = DumontThomas(s).mirror()
				sage: m.plot()									  # random
				sage: m = BetaAdicSet(1/m.b, m.a)
				sage: m.plot()									  # random

			#. A part of the boundary of the dragon fractal::

				sage: from badic.cautomata_generators import *
				sage: from badic.beta_adic import BetaAdicSet
				sage: m = BetaAdicSet(1/(1+I), dag.AnyWord([0,1]))
				sage: mi = m.intersection_words([0], [1])
				sage: mi.plot(nprec=6)							  # random

			#. A part of the boundary of the "Hokkaido" fractal::

				sage: from badic.beta_adic import DumontThomas
				sage: s = WordMorphism('a->ab,b->c,c->d,d->e,e->a')
				sage: m = DumontThomas(s).mirror()
				sage: mi = m.intersection_words([0], [1])
				sage: mi.plot()									 # random

			#. A limit set that look like a tiling but with holes::

				sage: from badic.beta_adic import DumontThomas
				sage: from badic.beta_adic import BetaAdicSet
				sage: m = BetaAdicSet(x^4 + x^3 - x + 1, [0,1])
				sage: m.plot()									  # random

		"""
		cdef Surface s
		cdef BetaAdic b
		cdef Automaton aut
		cdef int i, j
		sig_on()
		b = getBetaAdic(self, prec=prec, mirror=mirror, verb=verb)
		sig_off()
		cdef int sy2 = sy
		# test if in dimension 1
		if verb:
			print("b.y = %s" % b.b)
		if b.b.y == 0.:
			for i in range(b.n):
				if verb:
					print("t[%s] = %s" % (i, b.t[i]))
				if b.t[i].y != 0.:
					break
			else:
				if verb:
					print("Dimension 1")
				sy2 = 1
		sig_on()
		s = NewSurface(sx, sy2)
		sig_off()
		if verb:
			print("b=%s+%s*I" % (b.b.x, b.b.y))
			print("n=%s" % b.n)
			for i in range(b.n):
				print("t[%s] = %s+%s*I" % (i, b.t[i].x, b.t[i].y))
			# print("a=%s"%b.a)
			for i in range(b.a.n):
				if b.a.e[i].final:
					print("(%s) " % i)
				else:
					print("%s " % i)
			aut = b.a;
			for i in range(aut.n):
				for j in range(aut.na):
					print("%s -%s-> %s\n" % (i, j, aut.e[i].f[j]))
		cdef Color col
		col.r = color[0]
		col.g = color[1]
		col.b = color[2]
		col.a = color[3]
		if n is None:
			n = -1
		spr = self.a.prune().spectral_radius()
		if verb:
			print("spr = %s" % spr)
		sig_on()
		Draw(b, s, n, ajust, col, nprec, spr, verb)
		sig_off()
		sig_on()
		im = surface_to_img(s)
		sig_off()
		if verb:
			print("Free...")
		sig_on()
		FreeSurface(s)
		FreeBetaAdic(b)
		sig_off()
		return im

	def plot_list(self, list la=None, n=None,
				  int sx=800, int sy=600, bint ajust=True, int prec=53, colormap='hsv',
				  backcolor=None, float opacity=1., bint mirror=False,
				  int nprec=4, bint verb=False):
		r"""
		Draw the beta-adic set self, with color according to the list of automata or BetaAdicSets given.

		INPUT:

		- ``la``- list (default: ``None``)
		  List of automata or BetaAdicSet to plot.

		- ``n`` - integer (default: ``None``)
		  The number of iterations used to plot the fractal.

		- ``sx`` -- int (default: 800) - width of the result image

		- ``sy`` -- int (default : 600) - height of the result image

		- ``ajust`` -- Bool (default: ``True``) - adapt the drawing to fill all the image, with
		  ratio 1 (default: ``True``)

		- ``prec`` - precision of returned values (default: ``53``)

		- ``colormap`` - list of colors (default: ``hsv``)
		  Colors of the drawing.

		- ``backcolor`` - (default: ``None``) list of four integers between 0
		  and 255  .

		- ``opacity`` -- float (default: ``1.``)
		  Transparency of the drawing coefficient.

		- ``mirror`` -- Bool (default ``False) set to ``True`` to use the mirror of the automaton

		- ``nprec`` -- int (default 4) - additionnal iterations

		- ``verb`` -- Bool (default: ``False``)
		  Print informations for debugging.

		OUTPUT:

			A Graphics object.

		EXAMPLES::

			#. The Rauzy fractal of the Tribonacci substitution::

				sage: from badic.beta_adic import DumontThomas
				sage: s = WordMorphism('1->12,2->13,3->1')
				sage: m = DumontThomas(s)
				sage: m.plot_list(mirror=True)  # random

			#. A non-Pisot Rauzy fractal::

				sage: from badic.beta_adic import DumontThomas
				sage: s = WordMorphism({1:[3,2], 2:[3,3], 3:[4], 4:[1]})
				sage: m = DumontThomas(s)
				sage: from badic.beta_adic import BetaAdicSet
				sage: m = BetaAdicSet(1/m.b, m.a)
				sage: m.plot_list(mirror=True)			 # random
				sage: m = BetaAdicSet(m.b, m.a.mirror())
				sage: m.plot_list(mirror=True)			 # random

			#. The dragon fractal and its boundary::

				sage: from badic.beta_adic import BetaAdicSet
				sage: m = BetaAdicSet(1/(1+I), [0,1])
				sage: mi = m.intersection_words([0], [1])
				sage: m.plot_list([mi], n=19, colormap=[(.5,.5,.5,.5), (0,0,0,1.)])  # random

			#. The "Hokkaido" fractal and its boundary::

				sage: from badic.beta_adic import DumontThomas
				sage: s = WordMorphism('a->ab,b->c,c->d,d->e,e->a')
				sage: m = DumontThomas(s).mirror()
				sage: mi = m.intersection_words([0], [1])					# long time
				sage: m.plot_list([mi], colormap='gist_rainbow')			 # not tested

			#. A limit set that look like a tiling::

				sage: from badic.beta_adic import BetaAdicSet
				sage: m = BetaAdicSet(x^4 + x^3 - x + 1, [0,1])
				sage: m = m.reduced().mirror()
				sage: m.plot_list(mirror=True)				 # random

			#. Plot a domain exchange computed from a BetaAdicSet

				sage: from badic.beta_adic import DumontThomas
				sage: s = WordMorphism('a->ab,b->c,c->d,d->e,e->a')
				sage: m = DumontThomas(s).mirror()
				sage: la = m.domain_exchange()			  # long time
				sage: m.plot_list([a for t,a in la])		# not tested
		"""
		cdef Surface s = NewSurface(sx, sy)
		cdef BetaAdic2 b
		sig_on()
		b = getBetaAdic2(self, la=la, prec=prec, mirror=mirror, verb=verb)
		sig_off()
		# dessin
		if n is None:
			n = -1

		# Manage colors
		if backcolor is None:
			backcolor = (.5, .5, .5, .5)
		cdef ColorList cl
		sig_on()
		cl = NewColorList(b.na)
		sig_off()
		if isinstance(colormap, list):
			# if b.na > len(colormap):
			#	raise ValueError("The list of color must contain at least %d elements."%b.na)
			for i in range(b.na):
				if i < len(colormap):
					cl[i] = getColor(colormap[i])
				else:
					cl[i] = randColor(255)
				sig_check()
		elif isinstance(colormap, str):
			from matplotlib import cm
			if not colormap in cm.datad.keys():
				raise ValueError("Color map %s not known (type 'from matplotlib import cm' and look at cm for valid names)" % colormap)
			colormap = cm.__dict__[colormap]
			cl[0] = getColor(backcolor)
			for i in range(b.na-1):
				cl[i+1] = getColor(colormap(float(i)/float(b.na-1)))
				sig_check()
		else:
			raise TypeError("Type of option colormap (=%s) must be list of colors or str" % colormap)
		spr = self.a.prune().spectral_radius()
		sig_on()
		DrawList(b, s, n, ajust, cl, opacity, spr, nprec, verb)
		sig_off()
		# enregistrement du résultat
		sig_on()
		im = surface_to_img(s)
		sig_off()
		if verb:
			print("Free...")
		sig_on()
		FreeSurface(s)
		if la is None:
			FreeAutomatons(b.a, b.na)
		FreeBetaAdic2(b)
		FreeColorList(cl)
		sig_off()
		return im

#	def critical_exponent_aprox(self, niter=10, verb=False):
#		"""
#		Return an approximation of the critical exponent.
#		This function is inefficient and returns a bad approximation.
#
#		INPUT:
#
#		- ``niter`` int (default: 10) number of iterations
#
#		- ``verb`` - Bool (default: ``False``)
#		  verbose mode
#
#		OUTPUT:
#		A 
#
#		EXAMPLES::
#
#		#.
#			sage: m = BetaAdicSet(1/(1+I), dag.AnyWord([0,1]))
#			sage: m.critical_exponent_aprox()
#			2.0
#
#		#.
#			sage: s = WordMorphism('1->12,2->13,3->1')
#			sage: m = DumontThomas(s)
#			sage: m.critical_exponent_aprox()
#			2.0994952521...
#
#		"""
#		cdef set S, S2, S3
#		b = self.b
#		K = b.parent()
#		A = self.a.alphabet
#		S = set([K.zero()])
#		for i in range(niter):
#			S2 = set([])
#			for s in S:
#				for c in A:
#					S2.add((s+c)/b)
#			# intervertit S et S2
#			S3 = S2
#			S2 = S
#			S = S3
#			if verb:
#				print(len(S))
#		#m = mahler((1/b).minpoly())
#		m = abs(b.n())
#		return (log(len(S)) / (niter * abs(log(m))))

	def complexity(self, list Ad=None, prec=None, bint verb=False):
		r"""
		Return a estimation of an upper bound of the number of states
		of the relations automaton.
		This estimation is obtained by computing the volume occupied by the lattice containing the BetaAdicSet, in the space product of completions of Q for every absolute archimedian value and p-adic absolute value for which beta as modulus different of one.

		INPUT:

		 - ``Ad`` -- list (default: ``None``) - list of differences of digits

		 - ``prec`` -- integer (default: ``None``) - precision used for the computation

		 - ``verb`` - Boolean (default: ``False``) - Display informations for debug.

		OUTPUT:

		A positive integer.

		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: m.complexity()
			109

			sage: m = BetaAdicSet(x^3-x-1, [0,1])
			sage: m.complexity()
			1125
		"""
		b = self.b
		K = b.parent()
		pi = b.minpoly()
		pi = pi*pi.denominator()

		if verb:
			print(K)

		A = self.a.A
		if Ad is None:
			Ad = list(set([c1-c2 for c1 in A for c2 in A]))

		# archimedian places
		places = K.places(prec=prec)
		narch = len(places)
		# ultra-metric places
		from sage.arith.misc import prime_divisors
		lc = pi.leading_coefficient()*pi(0)
		for p in prime_divisors(lc):
			for P in K.primes_above(p):
				if abs_val(K, P, b, prec=prec) != 1:
					places.append(P)
		if verb:
			print(places)
		# bounds
		bo = []
		vol = 1.
		for i, p in enumerate(places):
			if i < narch:
				bo.append(
					max([abs_val(K, p, x) for x in Ad])/abs(1 - abs_val(K, p, b)))
				if verb:
					print("bo = %s" % bo[-1])
				if p(b).imag() == 0:
					vol *= 2*bo[-1]
				else:
					vol *= pi_number*bo[-1]**2
			else:
				bo.append(max([abs_val(K, p, x) for x in Ad])/abs_val(K, p, b))
				vol *= bo[-1]
			if verb:
				print("vol = %s", vol)
		if verb:
			print("bounds=%s" % bo)
		# from sage.functions.other import ceil
		return <int>(ceil(vol))

	def interior_op (self, other):
		"""
		Determine the interior of self with respect to other.
		Assume that other is strongly connected.

		INPUT:

			- ``other`` - DetAutomaton - language to found in self.
					Assumed to be strongly connected.

		EXAMPLES::

			sage: from badic import *
			sage: s = WordMorphism('a->ab,b->c,c->d,d->e,e->a')
			sage: m = DumontThomas(s).mirror()
			sage: s2 = WordMorphism('a->b,b->c,c->ab')
			sage: m2 = DumontThomas(s2).mirror()
			sage: mp = m2.proj(m); mp
			b-adic set with b root of x^3 - x - 1, and an automaton of 185 states and 2 letters
			sage: mp.interior_op(m)
			sage: mp.plot()				# random

		"""
		self.a.interior_op(getDetAutomaton(self,other))

	def prefix(self, list w):
		"""
		Return a BetaAdicSet like self but where we keep only words starting by w.

		INPUT:

		- ``w`` - list - word that we want as prefix

		OUTPUT:

		BetaAdicSet

		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: from badic.cautomata_generators import *
			sage: m = BetaAdicSet(x^3-x^2-x-1, dag.AnyWord([0,1]))
			sage: mp = m.prefix([0, 1, 1, 1]); mp
			b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 5 states and 2 letters
			sage: m.plot_list([mp])	 # random

		"""
		return BetaAdicSet(self.b, self.a.prefix(w))

	def intersection_words(self, list w1, list w2, bint closure=True, bint verb=False):
		r"""
		Compute the intersection of the adherences of the two beta-adic sets
		corresponding to words with prefix w1 and prefix w2.

		INPUT:

		- ``w1``- word
		  The first prefix.

		- ``w2``- word
		  The second prefix.

		OUTPUT:

		A Automaton.

		EXAMPLES::

			#. Compute a part of the boundary of the dragon fractal::

				sage: from badic.beta_adic import BetaAdicSet
				sage: m = BetaAdicSet(1/(1+I), [0,1])
				sage: m.intersection_words([0], [1])
				b-adic set with b root of x^2 - x + 1/2, and an automaton of 21 states and 2 letters

			#. Draw a part of the boundary of a Rauzy fractal::

				sage: from badic.beta_adic import DumontThomas
				sage: m = DumontThomas(WordMorphism('a->ab,b->ac,c->a')).mirror()
				sage: mi = m.intersection_words([0], [1])
				sage: mi.plot()						# not tested
		"""
		m1 = self.prefix(w1)
		m2 = self.prefix(w2)
		mi = m1.proj(m2, closure=closure, verb=verb)
		return mi

	def reduced_words_automaton(self, bint full=False, int step=100, alex=None,
								bint mirror=False, int algo_rel=1, int algo_inter=1, int verb=False):
		r"""
		Compute the reduced words automaton for the alphabet of the automaton of self.
		See http://www.i2m.univ-amu.fr/perso/paul.mercat/Publis/
		Semi-groupes%20fortement%20automatiques.pdf
		for a definition of such automaton.
		The number beta is assumed algebraic.

		INPUT:

		- ``full`` - Bool (default: False)
		  If True, compute a reduced_words_automaton for the full set
		  of words over the alphabet of the automaton of self.

		- ``mirror`` - Bool (default: ``False``)
		  If True, compute the mirror.

		- ``algo_rel`` - int (default ``3``)
		  Algorithm used for the computation of the relations automaton.

		- ``algo_inter`` - int (default ``2``)
		  Algorithm used for the computation of intersections of languages.

		- ``alex`` - DetAutomaton (default: ``None``) Automaton of a strict total order

		- ``verb`` - Bool (default: ``False``)
		  If True, print informations for debugging.

		- ``step`` - int (default: 100)
		  number of steps done (used for debugging)

		OUTPUT:

		DetAutomaton.

		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: ared = m.reduced_words_automaton()
			sage: ared
			DetAutomaton with 4 states and an alphabet of 2 letters

			sage: m = BetaAdicSet(x^3-x-1, [0,1])
			sage: ared = m.reduced_words_automaton()
			sage: ared
			DetAutomaton with 808 states and an alphabet of 2 letters

		TESTS::

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(pi, [0,1])
			sage: m.reduced_words_automaton()
			Traceback (most recent call last):
			...
			ValueError: b must live in a number field!

		"""
		cdef list A
		cdef list Ad
		cdef list Adp
		cdef int nAd, nA
		cdef DetAutomaton arel
		cdef int ne, ei

		A = self.a.A
		nA = len(A)
		
		try:
			QQbar(self.b)
		except:
			raise ValueError("b must live in a number field!")

		if full:
			# compute the relations automaton
			arel = BetaBase(self).relations_automaton(algo=algo_rel, A=self.a.A, B=self.a.A, mirror=mirror)
			if verb:
				print("arel = %s" % arel)
			if step == 1:
				return arel

			# add a new state
			ei = arel.a.i
			ne = arel.a.n  # new added state
			arel.add_state(True)
			arel.set_final(ei, final=False)  # the new state is final
			if step == 2:
				return arel

			Ad = arel.A
			nAd = len(Ad)

			# add edges from the new state (copy edges from the initial state)
			for j in range(nAd):
				arel.set_succ(ne, j, arel.succ(ei, j))
			if step == 3:
				return arel

			Adp = [i for i in range(
				nAd) if Ad[i] in [x-y for j, x in enumerate(A) for y in A[:j]]]

			# suppress some edges from the initial state
			for j in Adp:
				arel.set_succ(ei, j, -1)
			if step == 4:
				return arel

			# change edges that point to the initial state :
			# make them point to the new state
			for e in arel.states:
				if e != ei:
					for j in range(nAd):
						if arel.succ(e, j) == ei:
							arel.set_succ(e, j, ne)
			if step == 5:
				return arel

			# project, determinise and take the complementary
			d = {}
			for a in A:
				for b in A:
					if (a - b) not in d:
						d[a-b] = []
					d[a-b].append((a, b))
			if verb:
				print(d)
			arel = arel.duplicate(d)  # replace differences with couples
			d = {}
			for j in A:
				for i in A:
					d[(i, j)] = i
			if verb:
				print(d)
				print(arel)
			arel = arel.determinize_proj(d, noempty=False, nof=True)  # , verb=True)
			# project on the first value of the couple, determinise and take the complementary
			if verb:
				print(arel)
			arel = arel.prune()
			if step == 10:
				return arel
			return arel.minimize()
		else:
			arel = self.relations_automaton(algo=algo_rel)
			if verb > 0:
				print("arel = %s" % arel)
			if alex is None:
				alex = DetAutomaton([(0, (i, i), 0) for i in A]
									+ [(0, (A[i], A[j]), 1)
									   for i in range(nA) for j in range(i)]
									+ [(1, (i, j), 1) for i in A for j in A],
									i=0, final_states=[1], avoidDiGraph=True)
			if verb > 0:
				print("alex=%s" % alex)
			ai = arel.intersection(alex, algo=algo_inter, verb=verb-1)
			if verb > 0:
				print("ai=%s" % ai)
			ai = ai.proji(1)
			if verb > 0:
				print("ai=%s" % ai)
			ai.complementary_op()
			if verb > 0:
				print("ai=%s" % ai)
			return ai.intersection(self.a, algo=algo_inter, verb=verb-1)

	def reduced(self, bint mirror=False, int algo_rel=3, int algo_inter=1, int verb=False):
		r"""
		Compute a ``BetaAdicSet`` describing the same set, but with unicity (i.e. each point is described by an unique word).

		INPUT:

		- ``mirror`` Bool -- (default ``False) set to ``True`` in order to compute the mirror of the reduced language

		- ``algo_rel`` - int (default ``3``)
		  Algorithm used for the computation of the relations automaton.

		- ``algo_inter`` - int (default ``2``)
		  Algorithm used for the computation of intersections of languages.

		- ``verb`` - Bool (default: ``False``)
		  If True, print informations for debugging.


		OUTPUT:

		DetAutomaton.

		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: ared = m.reduced()
			sage: ared
			b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 4 states and 2 letters
		"""
		return BetaAdicSet(self.b, self.reduced_words_automaton(mirror=mirror,
																algo_rel=algo_rel,
																algo_inter=algo_inter,
																verb=verb))

	def critical_exponent_free(self, prec=None, simplify=True, int verb=1):
		r"""
		Compute the critical exponent of the beta-adic set,
		assuming it is free (or reduced, i.e. there is no relation,
		i.e. every point is uniquely represented by a word).
		When the beta-adic set is moreover algebraic and conformal, then it is equal
		to the Hausdorff dimension of the limit set in the
		contracting space (R or C).

		Rk: beta-adic sets coming from DumontThomas()
		are always free and algebraic.

		INPUT:

		- ``prec``- precision (default: ``None``)

		- ``verb``- int (default: ``1``)
		  Print more or less informations.

		OUTPUT:

		A real number.

		EXAMPLES::

			#. Hausdorff dimension of limit set of 3-adic expansion with numerals set {0,1,3}::

				sage: from badic.beta_adic import BetaAdicSet
				sage: from badic.cautomata_generators import *
				sage: m = BetaAdicSet(3, dag.AnyWord([0,1,3]))
				sage: mr = m.reduced()
				sage: mr.critical_exponent_free()
				log(y)/log(3) where y is the max root of x^2 - 3*x + 1, and 3 is root of x - 3.
				0.8760357589...

			#. Hausdorff dimension of limit set of phi-adic expansion with numerals set {0,1}::

				sage: from badic.beta_adic import BetaAdicSet
				sage: from badic.cautomata_generators import *
				sage: m = BetaAdicSet((1+sqrt(5))/2, dag.AnyWord([0,1]))
				sage: m = m.reduced()
				sage: m.critical_exponent_free()
				log(y)/log(1.618033988749895?) where y is the max root of x^2 - x - 1, and 1.618033988749895? is root of x^2 - x - 1.
				1.0


			#. Hausdorff dimension of the boundary of the dragon fractal::

				sage: from badic.beta_adic import BetaAdicSet
				sage: from badic.cautomata_generators import *
				sage: m = BetaAdicSet(1/(1+I), dag.AnyWord([0,1]))
				sage: mi = m.intersection_words(w1=[0], w2=[1])
				sage: mi.critical_exponent_free()
				log(y)/log(1.414213562373095?) where y is the max root of x^3 - x^2 - 2, and 1.414213562373095? is root of x^2 - 2.
				1.5236270862...


			#. Hausdorff dimension of the boundary of a Rauzy fractal::

				sage: from badic.beta_adic import DumontThomas
				sage: s = WordMorphism('1->12,2->13,3->1')
				sage: m = DumontThomas(s)
				sage: mi = m.intersection_words(w1=[0], w2=[1])
				sage: mi.critical_exponent_free()
				log(y)/log(1.356203065626296?) where y is the max root of x^4 - 2*x - 1, and 1.356203065626296? is root of x^6 - x^4 - x^2 - 1.
				1.0933641642...

			#. Hausdorff dimension of a non-Pisot Rauzy fractal::

				sage: from badic.beta_adic import DumontThomas
				sage: s = WordMorphism({1:[3,2], 2:[3,3], 3:[4], 4:[1]})
				sage: m = DumontThomas(s).mirror()
				sage: m.critical_exponent_free()
				log(y)/log(1.215716761013442?) where y is the max root of x^3 - x^2 + x - 2, and 1.215716761013442? is root of x^6 - x^4 + 2*x^2 - 4.
				1.5485260383...
		"""
		cdef DetAutomaton a
		if simplify:
			a = self.a.prune().minimize()
		else:
			a = self.a
		M = a.adjacency_matrix()
		if verb > 1:
			print("Eigenvalues...", flush=True)
		e = M.eigenvalues()
		if verb > 1:
			print("max...", flush=True)
		y = max(e, key=abs)
		if verb > 1:
			print("max = %s" % y, flush=True)
		#m = QQbar(mahler((1/self.b).minpoly()))
		m = QQbar(self.b)
		m = m*m.conjugate()
		m.simplify()
		m = m.sqrt()
		m.simplify()
		if m == 1:
			raise NotImplementedError("The computation of the critical exponent is not implemented for a number of absolute value 1.")
		if m < 1:
			m = 1/m
		if verb > 0:
			print("log(y)/log(%s) where y is the max root of %s, and %s is root of %s." % (m, QQbar(y).minpoly(), m, m.minpoly()))
		y = y.n(prec)
		# from sage.functions.log import log
		m = m.n(prec)
		if verb > 1:
			print("y=%s, m=%s" % (y, m))
		return log(y) / abs(log(m))

	def critical_exponent(self, prec=None, int algo_rel=3, bint verb=1):
		r"""
		Compute the critical exponent of the beta-adic set.
		If the beta-adic set is algebraic and conformal, then it is equal
		to the Hausdorff dimension of the limit set in the
		contracting space (R or C). If the beta-adic set is algebraic but not conformal,
		then this critical exponent is equal to the dimension of the limit set
		in the contracting space (product of R, C and p-adic spaces), for an appropriate notion of dimension.

		INPUT:

		- ``prec``- precision (default: ``None``)

		- ``algo_rel`` - int (default: ``2``)
		  Algorithm used for the computation of the relations automaton.

		- ``verb``- Bool (default: ``False``)
		  If >0, print informations.

		OUTPUT:

		A real number.

		EXAMPLES::

			#. Hausdorff dimension of limit set of 3-adic expansion with numerals set {0, 1, 3}::

				sage: from badic.beta_adic import BetaAdicSet
				sage: m = BetaAdicSet(3, [0,1,3])
				sage: m.critical_exponent()
				log(y)/log(3) where y is the max root of x^2 - 3*x + 1, and 3 is root of x - 3.
				0.8760357589718848

			#. Hausdorff dimension of limit set of phi-adic expansion with numerals set {0, 1}::

				sage: from badic.beta_adic import BetaAdicSet
				sage: m = BetaAdicSet((1+sqrt(5))/2, [0,1])
				sage: m.critical_exponent()
				log(y)/log(1.618033988749895?) where y is the max root of x^2 - x - 1, and 1.618033988749895? is root of x^2 - x - 1.
				1.0

			#. A non-conformal example::

				sage: from badic.beta_adic import BetaAdicSet
				sage: P = x^7 - 2*x^6 + x^3 - 2*x^2 + 2*x - 1
				sage: b = P.roots(ring=QQbar)[3][0]
				sage: m = BetaAdicSet(b, [0,1])
				sage: m.critical_exponent()					# long time
				log(y)/log(1.225816904767619?) where y is the max root of x^11 - 2*x^10 - 4*x^2 + 8*x + 2, and 1.225816904767619? is root of x^42 - 2*x^40 + 2*x^38 - 3*x^36 + 2*x^34 + x^32 - 8*x^30 - 3*x^28 + 6*x^26 + 10*x^24 + 4*x^22 + 4*x^20 + 14*x^18 + 6*x^16 - 11*x^14 - 21*x^12 + 20*x^10 - 9*x^8 + 2*x^6 + x^4 - 1.
				3.3994454205...

		.. SEEALSO::

			#. See more examples with :ref:'../../../thematic_tutorials/beta_adic_set.html'
			critical_exponent_free()

		"""
		if verb > 1:
			print("Computation of reduce words' automata")
		m = self.reduced(algo_rel=algo_rel, verb=verb-1)
		if verb > 1:
			print("%s"%m.a)
		return m.critical_exponent_free(prec=prec, verb=verb)

	def proj(self, other=None, pl=None, pls=None, plo=None, arel=None, arel0=None, t=0, m=1, bint closure=False, int algo=1, float margin=00000001, int verb=False):
		r"""
		Project m*self+t onto other.

		INPUT:

			- ``other`` - BetaAdicSet or DetAutomaton (default: ``None``) - 
		If arel and pl are not None, arel is assumed to be relations of pl.

			- ``pl`` - BetaAdicSet or DetAutomaton (default: ``None``) - projection language
						Allows to make the computation easier if pl is simple enough.

			- ``pls`` - BetaAdicSet or DetAutomaton (default: ``None``) - projection language for left side (self).
						Allows to make the computation easier if pls is simple enough.

			- ``plo`` - BetaAdicSet or DetAutomaton (default: ``None``) - projection language for right side (other).
						Allows to make the computation easier if plo is simple enough.

			- ``arel`` - DetAutomaton (default: ``None``) - relations automaton

			- ``arel0`` - DetAutomaton (default: ``None``) - relations automaton for t=0 and without languages. States are assumed to be labeled by algebraic numbers.

			- ``t`` - algebraic number (default: ``0``) - translation to do to self

			- ``m`` - algebraic number (default: ``1``) - multiplication to do to self

			- ``closure`` - bool (default: ``False``) - if True, compute words of other that can be prolongated infinitely often to words near m*self + t.

			- ``algo`` - int (default: ``1``) - algo used for computing relations automata

			- ``verb`` - int (default: ``False``) - if >0, print informations.

		OUTPUT:
			A BetaAdicSet.

		EXAMPLES::

			sage: from badic import *
			sage: mh = DumontThomas(WordMorphism('a->ab,b->c,c->d,d->e,e->a')).mirror()
			sage: m = DumontThomas(WordMorphism('a->b,b->c,c->ab')).mirror()
			sage: mp = m.proj(mh, m=m.b^8); mp
			b-adic set with b root of x^3 - x - 1, and an automaton of 202 states and 2 letters
			sage: mp.plot()				# not tested
			sage: mp.interior_op(mh)
			sage: mp.plot()				# random

		"""
		if other is None:
			other = self
		aa = self.a.concat_zero_star()
		ab = getDetAutomaton(self, other).concat_zero_star()
		if arel is None:
			if pl is None and pls is None and plo is None:
				arel = BetaAdicSet(self.b, aa).relations_automaton(BetaAdicSet(self.b, ab),
										  t=t, m=m, arel0=arel0, ext=closure, algo=algo, margin=margin, verb=verb-1)
				if verb > 0:
					print("arel = %s" % arel)
				r = arel.proji(1)
				if verb > 1:
					print("zero complete...")
				r.zero_complete_op()
				return BetaAdicSet(self.b, r)
			if pl is None:
				if pls is None:
					pls = self
				if plo is None:
					plo = other
			else:
				if pls is None:
					pls = pl
				if plo is None:
					plo = pl
			arel = get_beta_adic(self.b, pls).relations_automaton(get_beta_adic(self.b, plo), t=t, m=m,
									  arel0=arel0, ext=closure, algo=algo, margin=margin, verb=verb-1)
		if verb > 0:
			print("arel = %s" % arel)
		# browse the result
		A = aa.alphabet
		B = ab.alphabet
		d = dict()
		for i,a in enumerate(A):
			for j,b in enumerate(B):
				d[(i,j)] = arel.alphabet.index((a,b))
		i0 = (aa.initial_state, ab.initial_state, arel.initial_state)
		to_see = [i0]
		seen = set(to_see)
		R = []
		while len(to_see) > 0:
			i1, i2, i3 = to_see.pop()
			for j1 in range(aa.n_letters):
				k1 = aa.succ(i1, j1)
				if k1 == -1:
					continue
				for j2 in range(ab.n_letters):
					k2 = ab.succ(i2, j2)
					if k2 == -1:
						continue
					k3 = arel.succ(i3, d[(j1,j2)])
					if k3 == -1:
						continue
					e = (k1, k2, k3)
					if e not in seen:
						seen.add(e)
						to_see.append(e)
					R.append(((i1,i2,i3), (A[j1], B[j2]), e))
		r = DetAutomaton(R, A=[(a,b) for a in A for b in B], avoidDiGraph=True, i=i0)
		r.set_final_states([i for i in range(r.n_states) if aa.is_final(r.states[i][0]) and ab.is_final(r.states[i][1]) and arel.is_final(r.states[i][2])])
		if verb > 0:
			print("before prune: %s" % r)
		r = r.prune()
		if verb > 0:
			print("after prune: %s" % r)
		r =  r.proji(1)
		if verb > 1:
			print("zero complete or prune_inf...")
		if closure:
			r = r.prune_inf()
			r.set_all_final()
		else:
			r.zero_complete_op()
		return BetaAdicSet(self.b, r.minimize())

	def shift_op(self, w):
		"""
		Shift the automaton of self by w ON PLACE.

		INPUT:

		- ``w`` list (word to shift) or letter

		OUTPUT:

		Return the shifted BetaAdicSet

		EXAMPLES::
			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(3, [0,1,3])
			sage: m.shift_op([0,1,0])
			sage: m
			b-adic set with b root of x - 3, and an automaton of 1 state and 3 letters

		"""
		try:
			w = list(w)
			self.a.shift_list_op(w)
		except Exception:
			self.a.shift_op(w)

	def shift(self, w):
		"""
		Shift the automaton of self by w.

		INPUT:

		- ``w`` list (word to shift), or letter


		OUTPUT:

		Return the shifted BetaAdicSet

		EXAMPLES::
			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(3, [0,1,3])
			sage: m.shift([0, 1, 0])
			b-adic set with b root of x - 3, and an automaton of 1 state and 3 letters

		"""
		m = self.copy()
		m.shift_op(w)
		return m

	# used by Approx
	def _approx_rec(self, DetAutomaton a, test, f, x, int n, int n2):
		r"""
		used by approx

		INPUT:

		- ``a``  DetAutomaton
		- ``test``
		- ``f``
		- ``x``
		- ``n``  int
		- ``n2``  int


		OUTPUT:

		number of state or -1

		TESTS::

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: n = 13
			sage: pm = m.b.parent().places()[1]
			sage: test = lambda x: (pm(x).real())^2 + (pm(x).imag())^2 < .4
			sage: from badic.cautomata import DetAutomaton
			sage: a = DetAutomaton(None, A=m.a.alphabet)
			sage: f = a.add_state(1)
			sage: e = m._approx_rec(a, test, f, 0, n, n)
			sage: e
			3537

		"""
		if n == 0:
			if test(x):
				return f
			else:
				return -1
		else:
			e = dict()
			add = False
			for t in a.A:
				e[t] = self._approx_rec(a, test, f, x+t*self.b**(n2-n), n-1, n2)
				if e[t] != -1:
					add = True
			if add:
				e3 = a.add_state(0)
				for t in self.a.A:
					if e[t] != -1:
						a.add_transition(e3, t, e[t])
				return e3
			return -1

	def approx(self, n, test, bint get_aut=False, bint simplify=True):
		"""
		Gives a BetaAdicSet describing an approximation of a set defined by the
		characteritic function test, with the alphabet of the automaton of self.
		Rk: could be improved by drawing with the automaton of self
		.. see `thematic_tutorials  beta adic <../../../../thematic_tutorials/beta_adic_set.html>`_

		INPUT:

		- ``n`` -- int - number of iterations/depth of the approximation
		- ``test`` -- test function - function that associated
			to any element of the beta-adic-set, a Boolean
		- ``get_aut``  Bool -- (default ``False``)
		  if ``True`` return only a DetAutomaton
		- ``simplify``  Bool -- (default ``True``) set
		  to ``True`` to minimize and prune the automaton of the result

		OUTPUT:

		Return a DetAutomaton or a BetaAdicSet

		EXAMPLES::

			#. BetaAdicSet approximating a disk
				sage: from badic.beta_adic import BetaAdicSet
				sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
				sage: pm = m.b.parent().places()[1]
				sage: a = m.approx(13, lambda x: (pm(x).real())^2 + (pm(x).imag())^2 < .4 )
				sage: print(a)
				b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 201 states and 2 letters
				sage: a.plot()  # not tested

			#. BetaAdicSet approximating a square
				sage: from badic.beta_adic import DumontThomas
				sage: m = DumontThomas(WordMorphism('a->ab,b->ac,c->a')).mirror()
				sage: pm = m.b.parent().places()[1]
				sage: a = m.approx(14, lambda x: (pm(x).real())^2 < .3 and (pm(x).imag())^2 < .3 )
				sage: print(a)
				b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 236 states and 2 letters
				sage: m.plot_list([a])  # not tested

			#. Slide of the dragon fractal
				sage: from badic.beta_adic import BetaAdicSet
				sage: m = BetaAdicSet(1/(1.+I), [0,1])
				sage: m2 = m.approx(12, lambda x: x.real()^2 < .1)
				sage: m2
				(0.500000000000000 - 0.500000000000000*I)-adic set with an automaton of 32 states and 2 letters
				sage: m.plot_list([m2])	 # random

			#. BetaAdicSet approximating an image 
				sage: from badic.beta_adic import DumontThomas
				sage: m = DumontThomas(WordMorphism('1->12,2->13,3->1')).mirror()
				sage: from badic.beta_adic import ImageIn
				sage: im = ImageIn("SomeImage.png")									 # not tested
				sage: w = im.width()													# not tested
				sage: h = im.height()												   # not tested
				sage: ma = max(w,h)													 # not tested
				sage: pm = m.b.parent().places()[1]									 # not tested
				sage: m.approx(15, lambda x: (pm(x).conjugate()+.5*(1+I))*ma in im)	 # not tested
		"""
		cdef DetAutomaton a
		a = DetAutomaton(None, A=self.a.A)
		f = a.add_state(1)
		e = self._approx_rec(a, test, f, 0, n, n)
		for t in self.a.A:
			a.add_transition(f, t, f)
		a.a.i = e
		if simplify:
			a = a.minimize()
		if get_aut:
			return a
		else:
			return BetaAdicSet(self.b, a)

	def union(self, a):
		"""
		Return the union of BetaAdicSet and automaton or BetaAdicSet a

		INPUT:

		- ``a`` - automaton or BetaAdicSet

		OUTPUT:

		Return the BetaAdicSet union of ``a`` and ``self.a``

		EXAMPLE::

			sage: from badic.beta_adic import BetaAdicSet
			sage: from badic.cautomata_generators import *
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: a = dag.AnyWord([0, 1, 2, 4])
			sage: m.union(a)
			b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 1 state and 4 letters
			
			#. Disjoint union of two Rauzy fractals with same beta

			sage: from badic.beta_adic import DumontThomas
			sage: s = WordMorphism('1->12,2->13,3->1')
			sage: t = WordMorphism('1->12,2->31,3->1')
			sage: a = DumontThomas(s).mirror().unshift([0,0])
			sage: b = DumontThomas(t).mirror().unshift([1,0,0,0,0])
			sage: m = a.union(b); m
			b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 13 states and 3 letters
			sage: m.plot()			  # not tested
			sage: m.substitution()
			WordMorphism: a->ekgs, b->gnau, c->jmis, d->infr, e->jpbxy, f->eknzs, g->hlxqt, h->bxvbw, i->xqmjt, j->xqmis, k->dod, l->doc, m->jpb, n->hlxq, o->bxvb, p->xqmi, q->mis, r->ek, s->hl, t->jp, u->jm, v->mi, w->xqm, x->xq, y->m, z->t
		"""
		a = getDetAutomaton(self, a)
		return BetaAdicSet(self.b, self.a.union(a))

	def complementary(self, a):
		"""
		Compute the complementary of the BetaAdicSet in the BetaAdicSet or automaton a.

		INPUT:

		- ``a`` -- :class:`BetaAdicSet`
		  or :class:`sage.combinat.words.cautomata.DetAutomaton`
		  in which we take the complementary

		OUTPUT:

		A BetaAdicSet.

		EXAMPLES::

			#. The Rauzy fractal with a hole

				sage: from badic.beta_adic import DumontThomas
				sage: m = DumontThomas(WordMorphism('a->ab,b->ac,c->a')).mirror()
				sage: m = m.unshift([1,0,0,0]).complementary(m); m
				b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 7 states and 2 letters
				sage: m.plot()	  # not tested

			#. Complementary of a Rauzy fractal in another (for the same beta)

				sage: from badic.beta_adic import DumontThomas
				sage: s = WordMorphism('1->12,2->13,3->1')
				sage: t = WordMorphism('1->12,2->31,3->1')
				sage: a = DumontThomas(s).mirror()
				sage: b = DumontThomas(t).mirror()
				sage: m = b.complementary(a)
				sage: m
				b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 99 states and 2 letters
				sage: m.plot()	  # random
				sage: m = a.complementary(b)
				sage: m
				b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 42 states and 3 letters
				sage: m.plot()	  # random

		"""
		a = getDetAutomaton(self, a)
		return BetaAdicSet(self.b, self.proj(a).a.complementary().intersection(a))

	def unshift(self, l):
		"""
		Return a BetaAdicSet with a ``self.a`` unshifted by ``l``

		INPUT:

		- ``l``  list of indices of letters, or the index of a letter

		OUTPUT:

		Return a BetaAdicSet with an unshifted language

		EXAMPLE::

			sage: from badic.beta_adic import BetaAdicSet
			sage: from badic.cautomata_generators import *
			sage: m = BetaAdicSet(x^3-x^2-x-1, dag.AnyWord([0,1]))
			sage: m.unshift(1)
			b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 2 states and 2 letters
			sage: m = BetaAdicSet(x^3-x^2-x-1, dag.AnyWord([0,1]))
			sage: m.unshift([0,1])
			b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 3 states and 2 letters
		"""
		try:
			l = list(l)
			return BetaAdicSet(self.b, self.a.unshiftl(l))
		except:
			return BetaAdicSet(self.b, self.a.unshift(l))

	def diff(self, a):
		"""
		Compute the difference of two beta-adic sets.
		Return a beta-adic set describing the set of differences of the two beta-adic sets.

		INPUT:

		- ``a`` - a BetaAdicSet or an automaton

		OUTPUT:

		Return the difference of the two beta-adic sets.


		EXAMPLES::

			sage: from badic import *
			sage: m = BetaAdicSet(x^3-x^2-x-1, dag.AnyWord([0,1]))
			sage: a = dag.AnyWord([0, 1, 2, 4])
			sage: m.diff(a)
			b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 1 state and 6 letters

			#. Difference of a Rauzy fractal with itself

			sage: m = DumontThomas(WordMorphism('a->ab,b->ac,c->a')).mirror()
			sage: mdr = m.diff(m).reduced()
			sage: mdr
			b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 505 states and 3 letters
			sage: mdr.plot()		# random

			#. Covering of a Rauzy fractal by another

			sage: m = DumontThomas(WordMorphism('a->ab,b->ac,c->a')).mirror().unshift([0,0,0,0,0,0,0,0,0,0,0,0,0])
			sage: m2 = DumontThomas(WordMorphism('a->ab,b->ca,c->a')).mirror()
			sage: mdr = m.diff(m2).reduced()	# long time (8s)
			sage: mdr						   # long time
			b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 3344 states and 5 letters
			sage: mdr.plot()					# random

		"""
		a = getDetAutomaton(self, a)
		return BetaAdicSet(self.b, self.a.diff(a))

	def is_Pisot(self, bint verb=False):
		"""
		Test if the number b is the conjugate of a Pisot number or not.

		INPUT:

		- ``verb`` Bool -- (default : ``False``) set to ``True`` for verbose mode
		  If true, explains why we return False when it happens.

		OUTPUT:

		Return ``True`` or ``False``

		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(x^2-x-1, [0,1])
			sage: m.is_Pisot()
			True

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(x^4-2*x^3+x^2-2*x+1, [0,1])
			sage: m.is_Pisot()
			False

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(1+I, [0,1])
			sage: m.is_Pisot(verb=True)
			There is a conjugate of modulus greater than one which is not real.
			False

		"""
		try:
			if not self.b.is_integral():
				if verb:
					print("b is not an algebraic integer.")
				return False
			pi = self.b.minpoly()
			rr = [r[0] for r in pi.roots(ring=QQbar)]
			np = 0
			for r in rr:
				if abs(r) > 1:
					if np != 0:
						if verb:
							print("There are more than one conjugate of modulus > 1.")
						return False
					from sage.rings.qqbar import AA
					if r not in AA:
						if verb:
							print("There is a conjugate of modulus greater than one which is not real.")
						return False
					if r < 0:
						if verb:
							print("There is conjugate of modulus greater than one which is negative.")
						return False
					np = 1
				elif abs(r) == 1:
					if verb:
						print("There is a conjugate of modulus one.")
					return False
			if np == 0:
				if verb:
					print("There is no conjugate of modulus > 1.")
				return False
			return True
		except Exception:
			if verb:
				print("b is not an algebraic number.")
			return False

	def points(self, int n=1000, int npts=10000):
		"""
		Compute points (in the number field of b) corresponding to words of length k recognized by the automaton,
		where k is at most n, and the total number of points is approximatively npts.
		Return (k, list of couples (state, point))

		INPUT:

		- ``n`` - integer (default: 1000)
		  The maximum number of iterations.

		- ``npts`` - integer (default: 10000 )
		  Approximation of a bound on the number of points computed.

		OUTPUT:

		Return (k, list of couples (state, point)),
		where k is the number of iterations computed.

		EXAMPLES::

			#. The dragon fractal::
				sage: from badic.beta_adic import BetaAdicSet
				sage: m = BetaAdicSet(1/(1+I), [0, 1])
				sage: print(m)
				b-adic set with b root of x^2 - x + 1/2, and an automaton of 1 state and 2 letters
				sage: P = m.points()
				sage: P[0]
				13
				sage: len(P[1])
				8192
				sage: points([x.n() for i,x in P[1]], aspect_ratio=1)   # long time
				Graphics object consisting of 1 graphics primitive
		"""
		cdef int i, j, k, f, nA
		nA = self.a.a.na
		l = self.a.prune().spectral_radius()
		n = min(n, <int>(log(<double>npts)/log(<double>l)))
		r = [(self.a.a.i, 0)]
		bn = 1
		for i in range(n):
			rr = []
			for j, t in r:
				for k in range(nA):
					f = self.a.a.e[j].f[k]
					if f != -1:
						rr.append((f, t + bn*self.a.A[k]))
			bn = bn*self.b
			r = rr
		return (n, r)

	def zero_ball(self, p, int npts=1000):
		"""
		Compute the radius of a ball centered at 0 and that covers the BetaAdicSet for the place p.
		We assume that abs(p(self.b)) < 1.

		INPUT:

		- ``p`` - archimedian place

		- ``npts`` - integer (default: 10000 )
			Approximation of the number of points computed to find the bound.

		"""
		pts = self.points(npts=npts)
		M = abs(p(self.b**pts[0]))*max([abs(p(c))
										for c in self.a.A])/abs(1-abs(self.b))
		return max([abs(p(c[1]))+M for c in pts[1]])

	def diameter(self, p, int n=10, bint verb=False):
		"""
		Compute an upper bound of the diameter of the BetaAdicSet for the place p.
		The error has order p(self.b)^n.
		(The algorithm used here is not optimal.)

		INPUT:

		- ``p`` - archimedian place used to compute the diameter

		- ``n`` - integer (default: 10) - number of iterations

		- ``verb`` Bool -- (default : ``False``) set to ``True`` for verbose mode

		OUTPUT:

		double

		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: p = m.b.parent().places()[1]
			sage: m.diameter(p)
			2.93122910465427
		"""
		cdef int i, j, k, f, f2, nrr, nA
		cdef double d, dmm, dm2
		nA = self.a.a.na
		r = [(self.a.a.i, 0)]
		bn = 1
		M = max([abs(p(c)) for c in self.a.A])/abs(1-abs(self.b.n()))
		for i in range(n):
			rr = []
			for j, t in r:
				for k in range(nA):
					f = self.a.a.e[j].f[k]
					if f != -1:
						rr.append((f, t + bn*self.a.A[k]))
			bn = bn*self.b
			if verb:
				print("rr : %s elements" % len(rr))
			r = []
			# compute the diameter of the set rr (this could be improved)
			dmm = 0
			dm = np.zeros(len(rr), dtype=float)
			v = np.empty(len(rr), dtype=complex)
			for f, (j, t) in enumerate(rr):
				v[f] = p(t)
			nrr = len(rr)
			for f in range(nrr):
				dm2 = 0
				for f2 in range(nrr):
					d = abs(v[f] - v[f2])
					if d > dm2:
						dm2 = d
				dmm = fmax(dmm, dm2)
				dm[f] = dm2
			if verb:
				print("dmm = %s" % dmm)
			M2 = 2*abs(p(bn))*M
			if i == n-1:
				return dmm+M2
			for f, (j, t) in enumerate(rr):
				if dm[f]+M2 >= dmm:
					r.append((j, t))
			if verb:
				print("r : %s elements" % len(r))

	def translations_iterator(self, bint test_Pisot=True, int ndiam=20, bint verb=False):
		"""
		Compute a list of numbers containing the positive
		part of the BetaAdicSet, ordered in the expanding direction.
		Assume that self.b is the conjugate of a Pisot number.

		INPUT:

		- ``test_Pisot``  Bool -- (default : ``True``) test if b is the conjugate of a Pisot number as needed

		- ``verb`` Bool -- (default : ``False``) set to ``True`` for verbose mode

		- ``ndiam`` int  -- (default : 20): number of iterations
		  used for the estimation of the diameter

		OUTPUT:
		Return an iterator.


		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: from badic.cautomata_generators import *
			sage: m = BetaAdicSet((x^3-x^2-x-1).roots(ring=QQbar)[1][0], dag.AnyWord([0,1]))
			sage: next(m.translations_iterator())
			-b + 2

		"""
		cdef int n, i, j
		if test_Pisot:
			if not self.is_Pisot():
				raise ValueError("b must be the conjugate of a Pisot number")
		# take a basis of the lattice
		d = self.b.minpoly().degree()
		B = [self.b**i for i in range(d)]
		# compute the min of the differences for every place
		Bd = set([a-b for a in B for b in B if a != b])
		K = self.b.parent()
		n = -2147483648
		# from sage.functions.other import ceil
		# from sage.functions.log import log
		P = [p for p in K.places() if abs(p(self.b)) < 1]
		M = [self.diameter(p, n=ndiam) for p in P]

		for i, p in enumerate(P):
			m = min([abs(p(b)) for b in Bd])
			if verb:
				print("p=%s, m=%s, M=%s" % (p,m,M))
				print("%s" % (log(m/(2*M[i]))/log(abs(p(self.b)))))
			n = max(n, 1+<int>floor(log(m/(2*M[i]))/log(abs(p(self.b)))))
		if verb:
			print("n=%s" % n)
		# multiply the bound by this power of b
		bn = self.b**n
		M = [M[i]*abs(p(bn)) for i, p in enumerate(P)]
		# compute the matrix corresponding to the multiplication by M to the left
		from sage.matrix.constructor import identity_matrix
		I = identity_matrix(d)
		pi = self.b.minpoly()
		pi /= pi.leading_coefficient()
		from sage.matrix.constructor import matrix

		m = matrix(
			[I[i] for i in range(1, d)] +
			[[-c for c in pi.list()[:d]]]).transpose()

		if verb:
			print("m=%s" % m)
		# compute the Perron-Frobenius eigenvector
		from sage.modules.free_module_element import vector
		v = vector(max(
			[r[1][0] for r in m.right_eigenvectors()], key=lambda x: x[0]))
		v /= sum(v)
		vB = vector(B)
		if verb:
			print("v=%s" % v)
		r = []
		from itertools import count
		for j in count(start=1):
			vi = vector([<int> round(j * x) for x in v])
			t = vi * vB
			if t == 0:
				continue
			if verb:
				print("j=%s, t=%s" % (j, t))
			# test if t is in the domain
			keep = True
			for i, p in enumerate(P):
				if abs(p(t)) > M[i]:
					keep = False
					break
			if keep:
				yield t/bn

	def domain_translation_iterator (self, margin=.0000001, verb=False):
		r"""
		Compute the list of positive differences of points of the BetaAdicSet, in increasing order for the maximal expanding place.
		Assume that self.b is a Pisot number.

		INPUT:

		- ``margin``  - float (default : ``.0000001``) - margin used to compare places evaluations.

		- ``verb`` - int (default : ``False``) - if > 0, print informations.

		OUTPUT:
		Return an iterator.

		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: it = m.domain_translation_iterator()
			sage: next(it)
			b^2 - b - 1
			sage: next(it)
			b - 1

		"""
		a = self.a.copy()
		a.zero_complete_op()
		a = a.mirror().determinize().minimize()
		i0 = a.initial_state
		e0 = (0,i0,i0)
		to_see = [(0,e0)]
		seen = set([e0])
		b = self.b
		A = self.a.alphabet
		na = len(A)
		p = max(b.parent().places(), key=lambda p:p(b))
		if p(b) < 1:
			raise ValueError("self.b is not Pisot !")
		bb = max([p(t1-t2) for t1 in A for t2 in A])/(p(b)-1)
		if verb > 0:
			print("bb = %s" % bb)
		m = -bb - margin
		lt = set()
		first = True
		while len(to_see) > 0:
			if verb > 1:
				print([t for _,(t,_,_) in to_see])
			pt,(t,i1,i2) = to_see.pop()
			if a.is_final(i1) and a.is_final(i2):
				if pt > 0:
					if t not in lt:
						if verb > 1:
							print("t=%s, lt=%s" % (t,lt))
						if pt > bb + margin:
							if first:
								if verb > 1:
									print("first ! lt = %s" % lt)
								l = list(lt)
								l.sort(key=p)
								for t0 in l:
									yield t0
								first = False
							yield t
						lt.add(t)
			for j1 in range(na):
				k1 = a.succ(i1, j1)
				if k1 == -1:
					continue
				t1 = A[j1]
				for j2 in range(na):
					k2 = a.succ(i2, j2)
					if k2 == -1:
						continue
					t2 = A[j2]
					tt = b*t + (t1 - t2)
					ptt = p(tt)
					if ptt < m:
						continue
					e = (tt, k1, k2)
					if e not in seen:
						seen.add(e)
						to_see = insert((ptt,e), to_see)

	def translations_diff_iterator(self, bint test_Pisot=True, 
								   int ndiam=20, bint verb=False):
		"""
		Compute a list that contains the set of positive differences of points of the BetaAdicSet.
		The list is increasing for the expanding place.
		Assume that self.b is a Pisot number.

		INPUT:

		- ``test_Pisot``  Bool -- (default : ``True``) : test if b is 
		  the conjugate of a Pisot number as needed
		  B : basis of a lattice containing the BetaAdicSet

		- ``ndiam`` int -- (default : 20): number of iterations used
		  for the computation of the estimation of the diameter

		- ``verb`` Bool -- (default : ``False``) set to ``True`` for verbose mode

		OUTPUT:
		Return an iterator.

		EXAMPLES::

			sage: from badic.beta_adic import BetaAdicSet
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: it = m.translations_diff_iterator()
			sage: next(it)
			-b + 2
			sage: next(it)
			-b^2 + 2*b

		"""
		cdef int n, i, j
		if test_Pisot:
			if not self.is_Pisot():
				raise ValueError("b must be the conjugate of a Pisot number")
		# take a basis of the lattice
		d = self.b.minpoly().degree()
		B = [self.b**i for i in range(d)]
		# compute the min of the differences for every place
		Bd = set([a-b for a in B for b in B if a != b])
		K = self.b.parent()
		n = -2147483648
		# from sage.functions.other import ceil
		# from sage.functions.log import log
		P = [p for p in K.places() if abs(p(self.b)) < 1]
		M = [self.diameter(p, ndiam) for p in P]
		for i, p in enumerate(P):
			m = min([abs(p(b)) for b in Bd])
			if verb:
				print("p=%s, m=%s, M=%s" % (p, m,M))
				print("%s" % (log(m/(2*M[i]))/log(abs(p(self.b)))))
			n = max(n, 1+<int> floor(log(m/(2*M[i])) / log(abs(p(self.b)))))
		if verb:
			print("n=%s" % n)
		# multiply the bound by this power of b
		bn = self.b**n
		M = [M[i]*abs(p(bn)) for i, p in enumerate(P)]
		# compute the matrix corresponding to the multiplication by M to the left
		from sage.matrix.constructor import identity_matrix
		I = identity_matrix(d)
		pi = self.b.minpoly()
		pi /= pi.leading_coefficient()
		if verb:
			print("pi=%s" % pi)
		from sage.matrix.constructor import matrix

		m = matrix(
			[I[i] for i in range(1,d)] +
			[[-c for c in pi.list()[:d]]]).transpose()

		if verb:
			print("m=%s" % m)
		# compute the Perron-Frobenius eigenvector
		from sage.modules.free_module_element import vector
		v = vector(max([r for r in m.right_eigenvectors()],
						key=lambda x: abs(x[0]))[1][0])
		v /= sum(v)
		vB = vector(B)
		if verb:
			print("v=%s" % v)
		r = []
		from itertools import count
		seen = set()
		for j in count(start=1):
			vi = vector([<int>round(j * x) for x in v])
			t = vi*vB
			if t == 0 or t in seen:
				continue
			if verb:
				print("j=%s, t=%s"%(j,t))
			# test if t is in the domain
			keep = True
			for i, p in enumerate(P):
				if abs(p(t)) > M[i]:
					if verb:
						print("%s > %s"%(abs(p(t)), M[i]))
					keep = False
					break
			if keep:
				yield t/bn
			seen.add(t)

# TO BE ADDED LATER
#	def interior(self, verb=False):
#		r"""
#		We assume that self.b is a Pisot number.
#		Compute a BetaAdicSet describing the interior for the topology for which open sets are
#		sets of points of that are in the BetaAdicSet with same beta but with a language that recognize every words over the alphabet of self.a and that projects to an open set of P, for the natural projection on the contracting space (which is a product of copies of R, C and p-adic fields).
#		"""
#		def S(a, verb=False):
#			F = []
#			for e in a.states:
#				ok = True
#				for l in range(len(a.alphabet)):
#					if a.succ(e, l) != e:
#						ok = False
#						break
#					if ok:
#						F.append(e)
#						a2 = a.copy()
#						a2.set_final_states(F)
#						if verb:
#							print "F =",F
#						return a2
#		arel = self.relations_automaton(t=0,couples=True)
#		if verb:
#			print "arel =",arel
#			#arel.plot()
#		ap = dag.AnyWord(self.a.alphabet).product(self.a.concat_zero_star())
#		ai = ap.intersection(arel)
#		if verb:
#			print "ai =",ai
#		aip = ai.proji(0)
#		if verb:
#			print "aip =", aip
#		aip.zero_complete_op()
#		af = S(aip.minimize())
#		af.zero_complete_op()
#		if verb:
#			print "af =",af
#		af2 = af.minimize().intersection(self.a)
#		af2 = af2.prune()
#		if verb:
#			print "af2 =",af2
#			print af2.equals_langages(self.a)
#		return BetaAdicSet(self.b, af2) 
#

	def good_pl (self, nmax=2000, kmax=100, keep_self=False, pref=True, verb=False):
		r"""
		Find a good projection language for self.
		
		INPUT:

			- ``nmax`` - int (default: ``2000``) - maximal length of b-expansion
							in order to test its periodicity
	`
			- ``kmax`` - int (default: ``100``) - maximal k such that b^k*self is included in pl

			- ``keep_self`` - bool (default: ``False``) - if True, try to keep self

			- ``pref`` - bool (default: ``True``) - if True, allow to return a pl containing self up to closure

			- ``verb`` - int (default: ``False``) - if >0, print informations.


		OUTPUT:
			A couple of BetaAdicSet, the projection language and self*b^k projected on it.

		EXAMPLES::

			sage: from badic import *
			sage: m = BetaAdicSet(x^3-x-1, dag.Word([0]).concat(dag.AnyWord([0,1])))
			sage: m.good_pl(verb=1)
			periodic expansion [1, 0, 0, 0, 0]
			k = 9
			(b-adic set with b root of x^3 - x - 1, and an automaton of 5 states and 2 letters,
			 b-adic set with b root of x^3 - x - 1, and an automaton of 288 states and 2 letters)

			sage: m = BetaAdicSet(x^3-x-1, dag.AnyWord([0,1]))
			sage: m.good_pl(keep_self=True, verb=1)
			self is already a good projection language.
			(b-adic set with b root of x^3 - x - 1, and an automaton of 1 state and 2 letters,
			 b-adic set with b root of x^3 - x - 1, and an automaton of 1 state and 2 letters)

		"""
		cdef BetaAdicSet pl2
		if keep_self:
			# test if we can keep self
			a2 = self.a.concat_zero_star()
			a2.zero_complete_op()
			if a2.is_strongly_connected():
				if verb > 0:
					print("self is already a good projection language.")
				return BetaAdicSet(self.b, a2), BetaAdicSet(self.b, a2)
		# test if the expansion of b is periodic
		l = dev(self.b, self.b, nmax)
		if len(l) > 0:
			if verb > 0:
				print("periodic expansion %s" % l)
			d = dict()
			for i in range(len(l)-1):
				d[i] = [0 for j in range(l[i])]+[i+1]
			d[len(l)-1] = [0 for j in range(l[len(l)-1]+1)]
			s = WordMorphism(d)
			pl = DumontThomas(s).mirror()
			if verb > 1:
				print("pl = %s" % pl)
			#return pl
			# find k such that b^k*self is included in pl
			#from badic.cautomata_generators import dag
			#aw = dag.AnyWord(self.a.A)
			for k in range(kmax):
				if verb > 1:
					print("k = %s" % k)
				#pl2 = pl.proj(self, pls=pl, plo=aw, m=1/self.b**k)
				pl2 = pl.proj(self, m=1/self.b**k)
				if pref:
					pl2.a.set_all_final() # take the prefix closure of pl2
				if self.a.included(pl2.a):
					if verb > 0:
						print("k = %s" % k)
					#return pl, self.proj(pl, pls=aw, plo=pl, m=self.b**k)
					return pl, self.proj(pl, m=self.b**k)
		# by default, take pl = full shift with alphabet of self
		if verb:
			print("Take the default pl: full shift over alphabet %s" % self.alphabet)
		from badic.cautomata_generators import dag
		pl = dag.AnyWord(self.alphabet)
		return BetaAdicSet(self.b, pl), self.proj(pl)

	def domain_exchange (self, pl=None, n=None, ndiam=30, interior=True, testPisot=True, arel0=None, algo_inter=1, algo_iter=1, pref=True, verb=False):
		r"""
		Compute the domain exchange describing the BetaAdicSet. Assume that
		self.b is a Pisot number. Return a list of (translation,
		BetaAdicSet).

		INPUT:

			- ``pl`` - DetAutomaton or BetaAdicSet (default: ``None``) - projection language
					Assume that self is projected into pl.
					If pl is simple enough, it simplify the computation.

			- ``n`` - int -- (default: "None") - do only n steps.

			- ``algo_inter`` - int -- (default: 1)
				algorithm used to compute intersections of languages

			- ``algo_iter`` - int -- (default: 1)
				algorithm used to compute list of translations

			- ``ndiam`` - int (default: ``30``)

			- ``interior`` - bool (default: ``False``) - if True, compute only
							pieces with non-empty interior w.r.t. pl.

			- ``testPisot`` - bool (default: ``True``)

			- ``arel0`` - DetAutomaton (default: ``None``) - relations automaton
							with states labeled by algebraic numbers.

			- ``pref`` - bool (default: ``True``) - if True, allow to find a pl containing self up to closure.

			- ``verb`` - bool (default: ``False``) - if >0, print informations.

		OUTPUT:
			A list of (t,p) where t is the translation done in piece p.

		EXAMPLES::

			#. Domain exchange of the Tribonnacci substitution

			sage: from badic import *
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: l = m.domain_exchange(); l
			[(b^2 - b - 1,
			  b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 5 states and 2 letters),
			 (b - 1,
			  b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 4 states and 2 letters),
			 (1,
			  b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 3 states and 2 letters)]
			sage: m.plot_list([a for t,a in l])					  # not tested
			sage: m.plot_list([a.proj(m, t=t) for t,a in l])		 # random
			<PIL.Image.Image image mode=RGBA size=800x600 at 0x7F57DFF3BC10>

			#. A more complicated domain exchange

			sage: m = BetaAdicSet(x^3-x^2-x-1, dag.AnyWord([0]).concat(dag.Word([1,0,0])).concat(dag.AnyWord([0,1]))).reduced(); m
			b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 7 states and 2 letters
			sage: de = m.domain_exchange(); de
			[(b - 1,
			  b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 6 states and 2 letters),
			 (1,
			  b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 9 states and 2 letters),
			 (b^2 - b,
			  b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 7 states and 2 letters),
			 (b^2 - 1,
			  b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 10 states and 2 letters),
			 (b + 1,
			  b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 8 states and 2 letters),
			 (b^2,
			  b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 12 states and 2 letters),
			 (b + 2,
			  b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 9 states and 2 letters),
			 (b^2 + b - 1,
			  b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 11 states and 2 letters),
			 (b^2 + 1,
			  b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 11 states and 2 letters),
			 (b^2 + b,
			  b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 11 states and 2 letters),
			 (b^2 + 2,
			  b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 12 states and 2 letters)]
			sage: m.plot_list([a for t,a in l])					  # not tested
			sage: m.plot_list([a.proj(m, t=t) for t,a in l])		 # not tested

		"""
		if pl is None:
			#pl = getDetAutomaton(self, pl)
			pl, self = self.good_pl(pref=pref, verb=verb-1)
			if verb > 0:
				print("pl = %s" % pl)
				print("self = %s" % self)
		pl = getDetAutomaton(self, pl)
		if verb:
			print("compute translations with algo %s..." % algo_iter)
		if algo_iter == 1:
			it = self.domain_translation_iterator(verb=verb-1)
		else:
			it = self.translations_diff_iterator(test_Pisot=testPisot,
											 ndiam=ndiam, verb=verb)
		a = self.a.copy()
		a.zero_complete_op()
		if interior:
			a.interior_op(pl)
		if a.has_empty_language():
			raise ValueError("self is empty !")
		if arel0 is None:
			arel0 = BetaBase(self).relations_automaton(A=self.a.A, B=self.a.A, algo=1, keep_labels=True, prune=False)
		r = []
		if n is None:
			n = -1
		for t in it:
			if not t.is_integral():
				if verb:
					print("t=%s not integral", t)
				continue
			if verb > 0:
				print("t=%s" % t)
			#if pl is None:
			#	mi = self.proj(t=-t, arel0=arel0, verb=verb-1)
			#else:
			mi = self.proj(pl, t=-t, arel0=arel0, verb=verb-1)
			mia = mi.a.intersection(a)
			if interior: # pl is not None and
				mia.interior_op(pl)
				#mia.zero_complete_op()
			if not mia.has_empty_language():
				if verb:
					print("not empty ! mi.a=%s" % mia)
				mi = BetaAdicSet(self.b, mia)
				r.append((t, mi))
				a = a.intersection(mia.complementary(), algo=algo_inter)
				if interior: # pl is not None and
					a.interior_op(pl)
				if a.has_empty_language():
					return r
			n -= 1
			if n == 0:
				return r+[a]

	def first_return_map (self, list de, pl, list lm=None, dict darel=None, bint interior=True, int algo_inter=1, int n=0, int verb=False):
		"""
		Compute the first return map on self of the domain exchange de.

		INPUT:

			- ``de`` - list - domain exchange given as a list of (t,p) where p is a domain (given as a DetAutmaton) and t is an algebraic number, translation done in p.

			- ``pl`` - BetaAdicSet or DetAutomaton - projection language

			- ``lm`` - list (default: ``None``) - the result is a refinement of the partition lm.
				If lm is not None, the first number of each orbit is the index in lm.

			- ``darel`` - dict of DetAutomaton (default: ``None``) -
				relations automata for each translation of the domain exchange

			- ``interior`` - Bool (default: ``True``) -
				if True, compute only non-empty interior pieces with respect to pl.

			- ``algo_inter`` - int (default: ``1``) - algo used for computing intersections

			- ``n`` - int (default: ``0``) - stop after n steps if n > 0

			- ``verb`` - int (default: ``False``) - if >0, print informations.

		OUTPUT:
			A list of (li,p), p is a piece given as a DetAutomaton,
			and li is the orbit of p by the domain exchange, given as a list of indices.

		EXAMPLES::

			sage: from badic import *
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: de = m.domain_exchange(pl=m)
			sage: mp = m.proj(m, m=m.b)			# mutiply by beta
			sage: mp.first_return_map(de, m)
			[([2], DetAutomaton with 8 states and an alphabet of 2 letters),
			 ([2, 0], DetAutomaton with 4 states and an alphabet of 2 letters),
			 ([2, 1], DetAutomaton with 4 states and an alphabet of 2 letters)]

		"""
		cdef DetAutomaton ap, m, ai
		la = [getDetAutomaton(self, a) for t,a in de]
		lt = [t for t,a in de]
		if verb > 0:
			print("Domain exchange with %s pieces." % len(de))
		pl = getDetAutomaton(self, pl)
		lb = [self.a, pl.intersection(self.a.complementary(), algo=algo_inter)]
		if lm is None:
			to_see = [([], self.a)]
		else:
			to_see = [([i], getDetAutomaton(self, a)) for i,a in enumerate(lm)]
		R = []
		while len(to_see) > 0:
			tm, m = to_see.pop()
			if verb > 0:
				print(tm, m)
			for i,(t,a) in enumerate(zip(lt,la)):
				a = m.intersection(a, algo=algo_inter)
				if interior:
					a.interior_op(pl)
				if a.has_empty_language():
					continue
				if verb > 1:
					print("translate %s by %s" % (a,t))
				if darel:
					ap = BetaAdicSet(self.b, a).proj(pl, pl=pl, t=t, arel=darel[t]).a
				else:
					ap = BetaAdicSet(self.b, a).proj(pl, pl=pl, t=t).a
				if interior:
					ap.interior_op(pl)
				if ap.has_empty_language():
					print("Error !!!")
					return a
				a = ap
				ai = a.intersection(lb[0])
				if not ai.has_empty_language():
					if verb > 0:
						print("returned !")
					R.append((tm+[i], ai))
				ai = a.intersection(lb[1])
				if not ai.has_empty_language():
					if verb > 0:
						print("computation to continue")
					to_see.append((tm+[i], ai))
			n -= 1
			if n == 0:
				return lt,la,R
		return R

	def substitution (self, de=None, pl=None, bint interior=True, int algo_iter=1, int algo_inter=1, bint get_domains=False, int n=-1, bint proj=True, bint pref=True, int verb=False):
		r"""
		Compute a substitution whose Rauzy fractal is self.
		If interior is False, more precisely, a fixed point of the result substitution
		projects exactly to the countable set of points described by self.

		INPUT:

			- ``de`` - list (default: ``None``) - domain exchange on self,
						given as a list of (t,p), where p is a domain and t is the translation on p.

			- ``pl`` - BetaAdicSet or DetAutomaton (default: ``None``) - projection language
						If pl is simple enough, it allows to do the computation more efficiently.
						pl should be better zero_completed and strongly connected.

			- ``interior`` - bool (default: ``False``) - if True,
							   compute only pieces with non-empty interior w.r.t. pl.

			- ``algo_iter`` - int (default: ``1``) - algo used for computation of list of translations for the domain exchange

			- ``algo_inter`` - int (default: ``1``) - algo used for computation of intersections

			- ``get_domains`` - bool (default: ``False``) - if True, return also pieces of the Rauzy fractal,
								   given as a list of DetAutomaton.

			- ``n`` - int (default: ``-1``) - stop after n steps if n >= 0

			- ``proj`` - bool (default: ``True``) - if False, assume that self is projected onto pl.

			- ``pref`` - bool (default: ``True``) - if True, allow to find a pl containing self up to closure.

			- ``verb`` - int (default: ``False``) - if >0, print informations.

		OUTPUT:
			A WordMorphism (and a list of pieces if ``get_domains`` is True)

		EXAMPLES::

			#. Tribonnacci

			sage: from badic import *
			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: m.substitution()
			WordMorphism: a->c, b->ca, c->cb

			#. Example with infinitely many connected components and where zero is not an inner point

			sage: m = BetaAdicSet(x^3-x^2-x-1, dag.AnyWord([0]).concat(dag.Word([1,0,0,0])).concat(dag.AnyWord([0,1])))
			sage: m.substitution()
			WordMorphism: a->dbm, b->afm, c->de, d->gbm, e->ah, f->am, g->lbm, h->c, i->le, j->i, k->j, l->lm, m->k

			#. Substitution whose Rauzy fractal approximate a disk

			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,1])
			sage: pm = m.b.parent().places()[1]
			sage: a = m.approx(13, lambda x: (pm(x).real())^2 + (pm(x).imag())^2 < .4 )
			sage: s = a.substitution()   					   # long time (>30s)
			sage: s.rauzy_fractal_plot()					   # not tested

			#. Find a substitution whose Rauzy fractal is what the user draw

			sage: m = DumontThomas(WordMorphism('a->ab,b->ac,c->a')).mirror()
			sage: md = m.user_draw()						   # not tested
			sage: s = md.substitution(); s  				   # not tested

			#. The Tribonnacci Rauzy fractal with a hole

			sage: m = DumontThomas(WordMorphism('a->ab,b->ac,c->a')).mirror()
			sage: m2 = m.unshift([1,0,0,0]).complementary(m); m2
			b-adic set with b root of x^3 - x^2 - x - 1, and an automaton of 7 states and 2 letters
			sage: m2.substitution(pl=m, interior=True)
			WordMorphism: a->c, b->ca, c->db, d->eb, e->f, f->fca

			#. Disjoint union of two Rauzy fractals with same beta

			sage: s = WordMorphism('1->12,2->13,3->1')
			sage: t = WordMorphism('1->12,2->31,3->1')
			sage: a = DumontThomas(s).mirror().unshift([0,0])
			sage: b = DumontThomas(t).mirror().unshift([1,0,0,0,0])
			sage: m = a.union(b)
			sage: m.substitution()
			WordMorphism: a->ekgs, b->gnau, c->jmis, d->infr, e->jpbxy, f->eknzs, g->hlxqt, h->bxvbw, i->xqmjt, j->xqmis, k->dod, l->doc, m->jpb, n->hlxq, o->bxvb, p->xqmi, q->mis, r->ek, s->hl, t->jp, u->jm, v->mi, w->xqm, x->xq, y->m, z->t

			#. Countable union of Hokaiddo tiles with infinitely many holes

			sage: s = WordMorphism('a->ab,b->c,c->d,d->e,e->a')
			sage: n = 6; Hn = [(n,0,n),(n,1,n+1),(n+1,0,n+2),(n+2,0,n+3),(n+3,0,n+4),(n+4,0,n)]
			sage: a = DetAutomaton([(0,0,0),(0,1,1),(1,0,2),(2,0,3),(3,0,4),(4,1,5),(5,1,6)]+Hn, i=0, avoidDiGraph=True, final_states=range(n,n+5))
			sage: pl = DumontThomas(s).mirror()
			sage: m = BetaAdicSet(pl.b, a).proj(pl); m
			b-adic set with b root of x^3 - x - 1, and an automaton of 50 states and 2 letters
			sage: s = m.substitution(); s	# long time (>15s)
			WordMorphism: A->pt, B->E, C->D, D->Bv, E->Ff, F->Ia, G->Id, H->Jg, I->pH, J->Ka, K->BG, a->b, b->c, c->e, d->m, e->l, f->k, g->j, h->na, i->pa, j->x, k->w, l->v, m->u, n->s, o->r, p->q, q->hg, r->if, s->pd, t->C, u->B, v->A, w->z, x->y, y->hr, z->ov

			#. Union of two Rauzy fractals

			sage: m = BetaAdicSet(x^3-x^2-x-1, dag.Words([[0,0,0],[1,0,0]]).concat(dag.AnyWord([0,1])))
			sage: m.substitution()
			WordMorphism: a->ad, b->acadab, c->acadabadac, d->acadabadacad

			#. Intersection of two Rauzy fractals with same beta

			sage: s1 = WordMorphism('a->ab,b->ac,c->a')
			sage: s2 = WordMorphism('a->ab,b->ca,c->a')
			sage: m1 = DumontThomas(s1).mirror()
			sage: m2 = DumontThomas(s2).mirror()
			sage: mi = m2.proj(m1)
			sage: mi.substitution()
			WordMorphism: a->chgj, b->jea, c->jhb, d->jhhgj, e->ch, f->d, g->je, h->jf, i->jh, j->jk, k->i

			#. Make a hole in a Rauzy fractal

			sage: s = WordMorphism('a->aab,b->ac,c->a')
			sage: m = DumontThomas(s).mirror()
			sage: m2 = m.proj(m, t=1, m=m.b^3)
			sage: m3 = m2.complementary(m)
			sage: m3.substitution()
			WordMorphism: a->d, b->da, c->dcb, d->ecb, e->fb, f->fbdcb

			#. Complementary of a translated Rauzy fractal into another with same beta

			sage: s1 = WordMorphism('a->aab,b->ac,c->a')
			sage: s2 = WordMorphism('a->aab,b->ca,c->a')
			sage: m1 = DumontThomas(s1).mirror()
			sage: m2 = DumontThomas(s2).mirror().unshift([1,0,0])
			sage: mc = m2.complementary(m1)
			sage: mc.substitution()				# long time (> 20s)
			WordMorphism: a->ooiooinboohkskcpqgo, b->ooinlfjakskohkcpqgo, c->tiooinbooiooinboohk, d->ooinlfjcooinlfjakskooinlfjc, e->ooinlfjcooinlfjakskooiooinb, f->ooinlfjakskohkcpqgotiooinb, g->ordllfjctiooinbooioordllfjc, h->tiooinbooiooinboohktiooinb, i->tiooinbtiooinbooioordllfjc, j->ooiooinboohkskcpqgoooiooinboohkskcpqgpqm..., k->ooiooinboohkskcpqgpqmetiocqmetiocqmeoore..., l->ooinlfjakskohkcpqgotiooinbooiooinboohkti..., m->ordllfjctiooinbooioordllfjctiooinbooioor..., n->tiooinbooiooinboohktiooinbooiooinboohkti..., o->tiooinbooiooinboohktiooinbooiooinboohkti..., p->tiooinbooiooinboohktiooiocqmetiocqmeoore..., q->tiooinbooiooinboohktiooiocqmetiocqmetreo..., r->tiooinbtiooinbooioordllfjctiooinbooioord..., s->tiooinbooiooinboohktiooinbooiooinboohkti..., t->tiooinbooiooinboohktiooinbooiooinboohkti...

			#. A Rauzy fractal for the smallest Pisot number

			sage: m = BetaAdicSet(x^3-x^2-1, dag.Word([0]).concat(dag.AnyWord([0,1])))
			sage: s = m.substitution(); s
			WordMorphism: a->jnt, b->lou, c->nc, d->nhs, e->d, f->c, g->b, h->a, i->et, j->gs, k->hs, l->lr, m->k, n->j, o->i, p->f, q->e, r->q, s->p, t->n, u->m

			#. Substitution for a beta-adic set with an alphabet with negative element

			sage: m = BetaAdicSet(x^3-x^2-x-1, [0,-1,1])
			sage: m.substitution()				# long time (> 10s)
			WordMorphism: 0->35, 1->34, 10->33,4, 11->47, 12->46, 13->45, 14->7,44, 15->6,42, 16->5,17, 17->7,17, 18->8,41, 19->12,43, 2->32, 20->11,41, 21->12,16, 22->23,13, 23->24,10, 24->24,9, 25->36,11, 26->38,13, 27->37,8, 28->39,9, 29->36,6, 3->31, 30->68, 31->67, 32->66, 33->64, 34->62, 35->61, 36->60, 37->59, 38->58, 39->57, 4->30, 40->56, 41->51, 42->50, 43->49, 44->48, 45->35,6,32, 46->34,8,31, 47->35,11,31, 48->1,18,7,17, 49->4,40,7,21, 5->4,40, 50->1,52,14, 51->4,63,19, 52->8,41,1,18, 53->29,2,36,6, 54->25,3,67, 55->29,2,64, 56->25,3,51, 57->24,9,29,2, 58->22,9,33,4, 59->28,53,2, 6->0,20, 60->26,55,4, 61->25,70, 62->27,69, 63->56,1,18, 64->60,0,20, 65->61,0,20, 66->71,15, 67->72,20, 68->73, 69->31,4,35,6,32, 7->1,18, 70->31,4,65,30, 71->34,8,31,4,35, 72->30,54,4,35, 73->34,8,31,4,35,6,32, 8->25,3, 9->29,2

		"""
		cdef DetAutomaton pla, arel0
		cdef int c, k
		if pl is None:
			pl, self = self.good_pl(pref=pref, verb=verb-1)
			proj = False
			if verb > 0:
				print("pl = %s" % pl)
				print("self = %s" % self)
		pla = getDetAutomaton(self, pl)
		self = BetaAdicSet(self.b, self.a.concat_zero_star())
		self.a.zero_complete_op()
		if interior: # and pl is not None:
			self.interior_op(pla)
		k = self.find_invariance(pl=pl, proj=proj)
		if verb > 0:
			print("k = %s" % k)
		#if pl is None:
		#	arel0 = None
		#else:
		arel0 = BetaBase(pl).relations_automaton(A=pla.A, B=pla.A, algo=1, keep_labels=True, prune=False)
		if de is None:
			de = self.domain_exchange(pl=pl, arel0=arel0, interior=interior, algo_inter=algo_inter, algo_iter=algo_iter, pref=pref)
		if interior:
			ar2 = pla.concat_zero_star()
			ar2.zero_complete_op()
			if not ar2.is_strongly_connected():
				raise ValueError("pl is not zero-completed and strongly connected: I cannot compute the interior.")
		# precompute relation automata
		darel = {}
		for t,_ in de:
			darel[t] = get_beta_adic(self.b, pl).relations_automaton(t=t, arel0=arel0)
		if verb > 1:
			print("relations automata:")
			print(darel)
		#
		c = 1
		while True:
			if c-1 == n:
				return de
			if verb > 0:
				print("\n*** step %s ***" % c)
				print("Exchange with %s pieces" % len(de))
			c += 1
			lm = [a.proj(pl, pl=pl, m=self.b**k) for t,a in de]
			if verb > 1:
				print("lm = {}".format(lm))
			bR = self.proj(pl, pl=pl, m=self.b**k)
			if verb > 1:
				print("bR = %s" % bR)
			R = bR.first_return_map(de, pl, lm=lm, darel=darel, interior=interior, algo_inter=algo_inter, verb=verb-1)
			if verb > 1:
				print(R)
			if len(R) == len(de):
				if verb > 0:
					print("finished !")
				break
			elif verb > 0:
				print("%s new pieces: computation to continue" % (len(R)-len(de)))
			de2 = []
			lt = [t for t,a in de]
			for li,m in R:
				if verb > 2:
					print("%s = %s -> %s" % (lt.index(sum([lt[i] for i in li[1:]])/self.b**k), li[0], li[1:]))
				de2.append((lt[li[0]], BetaAdicSet(self.b, m).proj(pl, pl=pl, m=1/self.b**k, t=-lt[li[0]])))
			if verb > 2:
				print(de2)
			de = de2
		if len(de) < 63:
			A = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
		else:
			A = range(len(de))
		d = {}
		for li,m in R:
			d[A[li[0]]] = [A[i] for i in li[1:]]
		s = WordMorphism(d)
		if get_domains:
			return s, de
		return s

	def relations_automaton(self, other=None, t=0, m=1, arel0=None, int algo=1, bint ext=False, bint prune=True, bint minimize=True, float margin=.00000001, int verb=False):
		"""
		Compute the set of words (a,b) on product of languages self x other
		such that m(a_0...a_n)+t = b_0...b_n in basis 1/self.b.
		If other is None, take other=self.
		
		If ext is True, it describes the set of words that can be
		prolongated to an infinite relation in the contracting space (which
		is the product of copies of R, C and p-adic spaces corresponding to
		places of the number field for which beta has an absolute value
		less than one).

		INPUT:

			- ``other`` - DetAutomaton or BetaAdicSet (default: ``None``) - if None, take other=self.

			- ``t`` - algebraic number (default: ``0``) - the translation of self

			- ``m`` - algebraic number (default: ``1``) - the multiplicative factor of self

			- ``arel0`` - DetAutomaton (default: ``None``) - the relations automaton without languages and with t=0. States are assumed to be labeled by algebraic numbers.

			- ``algo`` - int (default: ``1``) - algo used to compute arel0 (if arel0 is None).
							May give incorrect results if not 1.

			- ``ext`` - bool (default: ``False``) - if True, keep any word that can be prolongated to an infinite relation in the contracting space.

			- ``prune`` - bool (default: ``True``) - if True, prune the result (it avoids labels of states).

			- ``minimize`` - bool (default: ``True``) - if True, minimize the result (it avoids labels of states).

			- ``margin`` - float (default: ``.000000001``) - margin used to compare absolute value with bounds

			- ``verb`` - int (default: ``False``) - if >0, print informations.

		OUTPUT:
			A DetAutomaton.

		EXAMPLES::

			#. Infinite relations in the dragon fractal

			sage: from badic import *
			sage: m = BetaAdicSet(1/(1+I), [0,1])
			sage: m.relations_automaton(ext=True)
			DetAutomaton with 7 states and an alphabet of 4 letters

			#. Relations with the smallest Pisot number

			sage: m = BetaAdicSet(x^3-x-1, [0,1])
			sage: m.relations_automaton()
			DetAutomaton with 179 states and an alphabet of 4 letters

		"""
		cdef int i1, i2, j1, j2, k1, k2
		cdef DetAutomaton a2
		b = self.b
		K = b.parent()
		bb = BetaBase(b)
		if verb > 0:
			print("K = %s" % K)
		if other is None:
			other = self
		else:
			other = get_beta_adic(self.b, other)
		a2 = other.a
		A = self.a.A
		B = other.a.alphabet
		Pe,P = get_places(b, {m*x - y for x in A for y in B})
		if verb > 0:
			print("bP = %s, bPe = %s" % ([bP for _,bP in P], [bP for _,bP in Pe]))
		if arel0 is None:
			for p,bo in Pe:
				if abs_val(K, p, t) > bo - margin:
					break
			else:
				if verb > 0:
					print("Could be computed directly with algo 1")
			arel0 = bb.relations_automaton(algo=algo, A=A, B=B, m=m, ext=ext, keep_labels=True, prune=False, margin=margin)
		if verb > 0:
			print("arel0 = %s" % arel0)
		S0 = set(arel0.states)
		if verb > 1:
			print(S0)
		i0 = (K(-t), self.a.a.i, a2.a.i)
		to_see = [i0]
		seen = set(to_see)
		R = []
		while len(to_see) > 0:
			x, i1, i2 = to_see.pop()
			#print("%s, %s, %s" % (x,i1,i2))
			for j1 in range(self.a.a.na):
				k1 = self.a.a.e[i1].f[j1]
				if k1 == -1:
					continue
				for j2 in range(a2.a.na):
					k2 = a2.a.e[i2].f[j2]
					if k2 == -1:
						continue
					z = (x - (m*A[j1]-B[j2]))/b
					#print(" -> %s, %s, %s" % (z, k1, k2))
					if not ext and z not in S0:
						for p,bo in Pe:
							if abs_val(K, p, z) > bo - margin:
								break
						else:
							if verb > 2:
								print("%s avoided" % z)
							continue # we can never reach 0 from z
					for p,bo in P:
						if abs_val(K, p, z) > bo + margin:
							break # we can never reach 0 from z
					else:
						e = (z,k1,k2)
						if e not in seen:
							seen.add(e)
							to_see.append(e)
						R.append(((x,i1,i2), (A[j1], B[j2]), e))
		r = DetAutomaton(R, A=[(a,b) for a in A for b in B], avoidDiGraph=True, i=i0)
		if verb > 0:
			print("before prune: %s" % r)
		if ext:
			r = r.prune_inf()
			r.set_final_states(list(range(r.n_states)))
		else:
			r.set_final_states([i for i in range(r.n_states) if r.states[i][0] == 0 and\
				   self.a.is_final(r.states[i][1]) and other.a.is_final(r.states[i][2])])
			if prune:
				r = r.prune()
		if minimize:
			return r.minimize()
		return r

def rauzy_fractal_projection(self, b=None, int verb=False):
	r"""
	Return a projection map Z^A --> QQ(b).
	
	INPUT:
	
	- ``b`` -- (default ``None``) - Number used

	- ``verb`` -- Bool (default ``False``) - If True, print informations for debugging

	OUTPUT:

	A map from Z^A to NumberField of b.

	EXAMPLE:

	sage: from badic import *
	sage: s = WordMorphism('a->aabab,b->ababb')
	sage: p = rauzy_fractal_projection(s)
	sage: p([1,2])
	3
	"""
	M = self.incidence_matrix()
	if b is None:
		#choose b
		vp = max(M.eigenvalues())
		pi = vp.minpoly()
		if verb:
			print(pi)
		lc = []
		lr = []
		from sage.rings.qqbar import AA
		for r in pi.roots(ring=QQbar):
			if abs(r[0]) < 1:
				if r[0] in AA:
					lr.append(r[0])
				else:
					lc.append(r[0])
		if lc != []:
			b = max(lc, key=lambda x:abs(x))
		elif lr != []:
			b = max(lr, key=lambda x:abs(x))
		else:
			for r in pi.roots(ring=QQbar):
				if r[0] in AA:
					lr.append(r[0])
				else:
					lc.append(r[0])
			if lc != []:
				b = min(lc, key=lambda x:abs(x))
			elif lr != []:
				b = min(lr, key=lambda x:abs(x))
			else:
				raise ValueError("Cannot find an eigenvalue for the projection.")
		if verb:
			print(b)
		from sage.rings.number_field.number_field import NumberField
		K = NumberField(b.minpoly(), 'b', embedding=b)
		b = K.gen()
	# Left eigenvector vb in the number field Q(b)
	vb = (M-b).kernel().basis()[0]
	if verb:
		print(vb)
	return lambda x:sum([x[i]*vb[i] for i in range(len(x))])

# gives a BetaAdicSet from a WordMorphism
def DumontThomas(self, initial_state=None, final_states=None, proj=True, projection=None, prefix=True, verb=False):
	r"""
	Give a beta-adic set describing the Rauzy fractal.
	It is the abelianized prefix automaton of the substitution. 
	If proj=True, return a BetaAdicSet corresponding to the Dumont-Thomas numeration of the substitution.
	If proj=False, return a DetAutomaton corresponding to the Dumont-Thomas numeration of the substitution
	(this is the abelianization of the prefix automaton).
	
	INPUT:
	
	- ``initial_state`` -- (default ``None``) - letter to take as initial state in the prefix automaton
	
	- ``final_states`` -- (default ``None``) - letters to take as final states in the prefix automaton
	
	- ``proj`` -- Bool (default ``True``) - If True, return a BetaAdicSet corresponding to the
											Dumont-Thomas numeration of the substitution.
											If False, return a DetAutomaton corresponding to the
											Dumont-Thomas numeration of the substitution

	- ``projection`` -- (default ``None``) - projection used if proj is True

	- ``prefix`` -- (default ``True``) - abelianized prefix automaton or abelianized suffix automaton

	- ``verb`` -- Bool (default ``False``) - If True, print informations for debugging

	OUTPUT:

	BetaAdicSet if proj is True
	DetAutomaton if proj is False

	EXAMPLE:

	sage: from badic.beta_adic import DumontThomas
	sage: s = WordMorphism('a->aabab,b->ababb')
	sage: a = DumontThomas(s, proj=False); a
	DetAutomaton with 2 states and an alphabet of 7 letters
	sage: a.plot()		  # random

	# Zoom in a complicated Rauzy fractal
	sage: from badic.beta_adic import DumontThomas
	sage: s = WordMorphism('1->2,2->3,3->12')
	sage: m = DumontThomas(s).mirror(); m
	b-adic set with b root of x^3 - x - 1, and an automaton of 4 states and 2 letters
	sage: m.draw_zoom()		 # not tested (need the intervention of the user)

	# Draw the Rauzy fractal of the Hokkaido substitution
	sage: from badic.beta_adic import DumontThomas
	sage: s = WordMorphism('1->12,2->3,3->4,4->5,5->1')
	sage: m = DumontThomas(s); m
	b-adic set with b root of x^3 - x - 1, and an automaton of 5 states and 2 letters
	sage: m.plot_list(mirror=True)	  # random

	"""
	A = self.domain().alphabet()
	nA = len(A)
	if proj:
		if projection is None:
			projection = rauzy_fractal_projection(self)
		b = projection([1 for i in A]).parent().gen()
		if verb:
			print("b=%s" % b)
	else:
		projection = lambda x: x
	#construct the automaton
	if initial_state is None:
		initial_state = A[0]
	if verb:
		print("initial state %s"%initial_state)
	dA = dict()
	for i,a in enumerate(A):
		dA[a] = i
	L = []
	from sage.matrix.special import identity_matrix
	from sage.modules.free_module_element import vector
	I = identity_matrix(nA)
	for c in A:
		t = projection(vector([0 for i in range(nA)]))
		imc = list(self(c))
		if not prefix:
			imc.reverse()
		if verb:
			print("s(%s) = %s" % (c,imc))
		for c2 in imc:
			if proj:
				L.append((c,c2,t))
			else:
				L.append((c,c2,tuple(t)))
			v = vector(I[A.index(c2)])
			if verb:
				print("v = %s" % v)
			if prefix:
				t += projection(v)
			else:
				t -= projection(v)
	if verb:
		print(L)
	from .cautomata import DetAutomaton
	if final_states is None:
		final_states = A
	a = DetAutomaton(L, i=initial_state, final_states=final_states)
	if verb:
		print(a)
	if proj:
		return BetaAdicSet(b, a)
	else:
		return a

