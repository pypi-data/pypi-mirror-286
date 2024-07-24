# coding=utf8
"""
Miscellanious


AUTHORS:

- Paul Mercat (2013)- I2M AMU Aix-Marseille Universite - initial version

REFERENCES:

"""

# *****************************************************************************
#	   Copyright (C) 2014 Paul Mercat <paul.mercat@univ-amu.fr>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#	This code is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#	General Public License for more details.
#
#  The full text of the GPL is available at:
#
#				  http://www.gnu.org/licenses/
# *****************************************************************************
from __future__ import division, print_function, absolute_import

from libc.stdlib cimport malloc, free
from libc.stdint cimport int8_t

from cpython cimport bool as c_bool
from cysignals.signals cimport sig_on, sig_off, sig_check

from .cautomata cimport DetAutomaton, CAutomaton

cdef extern from "Automaton.h":
	cdef struct State:
		int* f
		int final

	cdef struct Automaton:
		State* e  # states
		int n   # number of states
		int na  # number of letters
		int i  # initial state

	cdef struct Transition:
		int l  # label
		int e  # arrival state

	cdef struct NState:
		Transition* a
		int n
		int final
		int initial

	cdef struct NAutomaton:
		NState* e  # states
		int n   # number of states
		int na  # number of letters

cdef extern from "automataC.h":
	NAutomaton CopyN(Automaton a, int verb)

cdef extern from "miscellanious.h":
	cdef struct Substitution:
		unsigned int *ls
		unsigned int *pos
		
	cdef struct SubstitutionsList:
		Substitution *s
		SubstitutionsList *next
		SubstitutionsList *last
	
	cdef struct SubstitutionGraphsList:
		Substitution *s
		unsigned int *le
		unsigned int ne
		SubstitutionGraphsList *next
		SubstitutionGraphsList *last
	
	cdef struct AutomataList:
		Automaton *a
		AutomataList *next
		AutomataList *last

	void CETn(double x, double *v, int nv, double tau, int niter, double **pr, int nd, double *res)
	SubstitutionsList *RauzyGraphs2 (int *le, int n, int8_t *lor, int ar)
	AutomataList *Unsubstitute (unsigned int *le, unsigned int n, int8_t *lor, unsigned int ar)
	void FreeSubstitutionGraphsList(SubstitutionGraphsList *sl)
	void FreeSubstitutionsList(SubstitutionsList *sl)
	void FreeAutomataList(AutomataList *sl)
	SubstitutionGraphsList DecomposeGraph (NAutomaton *a, unsigned int ar)

def decompose_graph (CAutomaton a, unsigned int ar):
	cdef SubstitutionGraphsList sl
	#cdef NAutomaton aa
	#aa = a.a
	sig_on()
	sl = DecomposeGraph(a.a, ar)
	sig_off()
	le = []
	for i in range(sl.ne):
		le.append((sl.le[2*i], sl.le[2*i+1]))
	d = dict()
	for i in range(len(le)):
		d[i] = []
		s = sl.s;
		for j in range(s.pos[i], s.pos[i+1]):
			d[i].append(s.ls[j])
	from sage.combinat.words.morphism import WordMorphism
	r = WordMorphism(d)
	return le,r

def unsubstitute (le, lor):
	"""
	Find minimized Rauzy graphs of order 2 of graph le with orientations of states lor.
	"""
	from sage.combinat.words.morphism import WordMorphism
	cdef unsigned int i
	cdef unsigned int *l = <unsigned int*>malloc(sizeof(int)*len(le)*2)
	cdef int8_t *lo = <int8_t *>malloc(sizeof(char)*len(lor))
	#cdef SubstitutionGraphsList *sl, *sl0
	cdef AutomataList *sl, *sl0
	cdef Substitution *s
	for i in range(len(le)):
		l[2*i] = le[i][0]
		l[2*i+1] = le[i][1]
	for i in range(len(lor)):
		lo[i] = lor[i]
	import sys
	#print("Unsubstitute...")
	#sys.stdout.flush()
	sig_on()
	sl0 = Unsubstitute (l, len(le), lo, len(le)//len(lor))
	sig_off()
	#print("...Unsubstituted")
	#sys.stdout.flush()
	ls = []
	sl = sl0
	while sl.next:
		#le = []
		#for i in range(sl.ne):
		#	le.append((sl.le[2*i], sl.le[2*i+1]))
		#d = dict()
		#for i in range(len(le)):
		#	d[i] = []
		#	s = sl.s;
		#	for j in range(s.pos[i], s.pos[i+1]):
		#		d[i].append(s.ls[j])
		#r = WordMorphism(d)
		a = DetAutomaton(None)
		a.a = sl.a
		a.A = list(range(len(le)))
		ls.append(a) #(le,r))
		sl = sl.next
	free(l)
	free(lo)
	FreeAutomataList(sl0)
	free(sl0)
	return ls

def rauzy_graphs2 (le, lor):
	"""
	Find minimized Rauzy graphs of order 2 of graph le with orientations of states lor.
	"""
	from sage.combinat.words.morphism import WordMorphism
	cdef int i
	cdef int *l = <int*>malloc(sizeof(int)*len(le)*2)
	cdef int8_t *lo = <int8_t *>malloc(sizeof(char)*len(lor))
	cdef SubstitutionsList *sl, *sl0
	cdef Substitution *s
	for i in range(len(le)):
		l[2*i] = le[i][0]
		l[2*i+1] = le[i][1]
	for i in range(len(lor)):
		lo[i] = lor[i];
	sl0 = RauzyGraphs2 (l, len(le), lo, len(le)//len(lor))
	ls = []
	sl = sl0
	while sl.next:
		d = dict()
		for i in range(len(le)):
			d[i] = []
			s = sl.s;
			for j in range(s.pos[i], s.pos[i+1]):
				d[i].append(s.ls[j])
		r = WordMorphism(d)
		ls.append(r)
		sl = sl.next
	free(l)
	free(lo)
	FreeSubstitutionsList(sl0)
	free(sl0)
	return ls

def iterate_CET (x, v, tau, V, niter=10000):
	r"""
	 - x real -- starting angle

	 - v list -- direction defining the CET

	 - tau real -- tau

	 - niter int (default: ``10000``) number of iterations
	"""
	cdef double *xm = <double *>malloc(sizeof(double)*V.nrows())
	cdef double *l = <double *>malloc(sizeof(double)*len(v))
	cdef double **proj = <double **>malloc(sizeof(double*)*len(v))
	cdef int i,j
	#print("v={}".format(v))
	for i in range(len(v)):
		l[i] = v[i]
		proj[i] = <double *>malloc(sizeof(double)*V.nrows())
		for j in range(V.nrows()):
			proj[i][j] = V[j,i]
	CETn(x, l, len(v), tau, niter, proj, V.nrows(), xm)
	for i in range(len(v)):
		free(proj[i])
	free(proj)
	free(l)
	res = []
	for i in range(V.nrows()):
		res.append(xm[i])
	free(xm)
	return res
	
	
	
	
	
