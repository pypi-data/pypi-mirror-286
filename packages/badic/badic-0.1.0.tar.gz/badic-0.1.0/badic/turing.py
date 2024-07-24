# coding=utf8
"""
Manipulation of Turing machines.

AUTHORS:

- Paul Mercat (2024)- I2M AMU Aix-Marseille Universite - initial version

"""

# *****************************************************************************
#	   Copyright (C) 2024 Paul Mercat <paul.mercat@univ-amu.fr>
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

from sage.combinat.words.word import Word
from sage.graphs.digraph import DiGraph
from sage.modules.free_module_element import zero_vector
from sage.groups.perm_gps.permgroup_named import SymmetricGroup
from sage.misc.prandom import choice
from sage.combinat.words.morphism import WordMorphism
from badic.cautomata import DetAutomaton
from sage.plot.graphics import Graphics
from sage.plot.text import text
from sage.plot.polygon import polygon2d
from sage.graphs.graph import Graph
from sage.rings.integer_ring import ZZ
from copy import copy
from sage.rings.infinity import Infinity

def plot_square (x, y, color="black", fill=True, size=10, thickness=1):
	if fill:
		return polygon2d([(x*size,y*size),(x*size,(y+1)*size),((x+1)*size,(y+1)*size),((x+1)*size,y*size)], fill=fill, color=color, thickness=thickness)
	else:
		return polygon2d([(x*size,y*size),(x*size,(y+1)*size),((x+1)*size,(y+1)*size),((x+1)*size,y*size)], fill=fill, color=color, thickness=thickness, zorder=10000)

def plot_rub(y, tape, pos, state, size=10, thickness=1, colors=None, fontsize=20):
	if colors is None:
		colors = ["white", "red", "green", "blue", "cyan", "magenta", "yellow"]
	g = Graphics()
	for x in range(len(tape)):
		g += plot_square(x, y, colors[tape[x]])
	g += plot_square(pos, y, "black", False)
	g += text(state, ((pos+.5)*size, (y+.5)*size), color="black", fontsize=fontsize, zorder=Infinity)
	g.axes(False)
	g.set_aspect_ratio(1)
	return g

class SignedGraph:
	r"""
	A signed graph is an oriented graph with a sign for each vertex.
	"""
	def __init__(self, le, lor, A=None):
		r"""
		A signed graph is an oriented graph with a sign for each vertex.

		INPUT:

			- ``le`` - iterable - list of edges (given as couples)
			- ``lor`` - iterable - list of signs of vertices (+1 or -1)
			- ``A`` - list (default: ``None``) - alphabet that gives a name to each edge

		OUTPUT:
			A SignedGraph.

		EXAMPLES::

			sage: from badic import *
			sage: SignedGraph([(0,0),(0,1),(1,1),(1,0)], [1,-1])
			Signed graph with 4 edges and 2 vertices (use .plot() to display the graph).

		"""
		self.le = list(le)
		self.lor = list(lor)
		S = {t[0] for t in le}.union({t[-1] for t in le})
		self.S = S # set of states
		if A is None:
			A = range(len(le))
		self.A = A # alphabet used for labeling transitions
		self.ds = dict() # dictionnary of succs
		for j,(i,_) in enumerate(self.le):
			if i not in self.ds:
				self.ds[i] = []
			self.ds[i].append(j)

	def __repr__(self):
		return "Signed graph with %s edges and %s vertices (use .plot() to display the graph)." % (len(self.le), len(self.S))

	def __eq__(self, other):
		r"""
		Compare two SignedGraph modulo permutation and inversion of signs.
		Return all possible permutations of edges that gives same SignedGraph.
		"""
		return are_equal_signed_graphs(self.le, other.le, self.lor, other.lor, li=1)
	
	def plot (self, file=None):
		r"""
		Plot the SignedGraph.
	
		INPUT:

			- ``file`` - string (default: ``None``) - filename where the dot file of the SignedGraph is saved.

		OUTPUT:
			A picture of the SignedGraph.

		EXAMPLES::

			sage: from badic import *
			sage: SignedGraph([(0,0),(0,1),(1,1),(1,0)], [1,-1]).plot()
			168x119px 32-bit RGBA image

		"""
		return graph_aut(self.le, lor=self.lor, A=self.A, F=[]).plot(file=file)

	def rand_rauzy_graph2 (self):
		r"""
		Return a random Rauzy graph of order 2 corresponding to this signed graph.

		OUTPUT:
			A DetAutomaton.

		EXAMPLES::

			sage: from badic import *
			sage: g = SignedGraph([(0,0),(0,1),(1,1),(1,0)], [1,-1])
			sage: g.rand_rauzy_graph2()
			DetAutomaton with 8 states and an alphabet of 4 letters

		"""
		return rand_rauzy_graph2(self.le, self.lor)
	
	def rauzy_graphs2 (self):
		r"""
		Return all possible connected Rauzy graphs of order 2 of self.

		OUTPUT:
			A list of DetAutomaton.

		EXAMPLES::

			sage: from badic import *
			sage: g = SignedGraph([(0,0),(0,1),(1,1),(1,0)], [1,-1])
			sage: g.rauzy_graphs2()
			[DetAutomaton with 8 states and an alphabet of 4 letters,
			 DetAutomaton with 8 states and an alphabet of 4 letters]

		"""
		from badic.misc import unsubstitute as rauzy_graphs
		return rauzy_graphs(self.le, self.lor)
	
	def substitutive_turing (self, verb=0):
		r"""
		Return all possible substitutive Turing machine corresponding to this signed graph.

		OUTPUT:
			A list of TuringMachine and their substitution as a WordMorphism.

		EXAMPLES::

			sage: from badic import *
			sage: g = SignedGraph([(0,0),(0,1),(1,1),(1,0)], [1,-1])
			sage: g.substitutive_turing()
			[(Turing machine with 4 transitions and 2 states (use .plot() to display the machine).,
			  WordMorphism: 0->0, 1->1312, 2->2, 3->30),
			 (Turing machine with 4 transitions and 2 states (use .plot() to display the machine).,
			  WordMorphism: 0->0, 1->12, 2->2, 3->3130)]

		"""
		R = substitutive_turing(self.le, self.lor, verb=verb)
		return [(TuringMachine(lt),s) for lt,s in R]
	
	def substitutive_turing_from_sft (self, a, verb=0):
		r"""
		Return all possible substitutive Turing machine corresponding to this signed graph
		and to the given sft. The sft is given as a DetAutomaton recognizing its language.

		OUTPUT:
			A list of TuringMachine and their associate substitution as a WordMorphism.

		EXAMPLES::

			sage: from badic import *
			sage: g = SignedGraph([(0,0),(0,1),(1,1),(1,0)], [1,-1])
			sage: a = g.rand_rauzy_graph2()
			sage: g.substitutive_turing_from_sft(a)		# random
			[]

		   """
		R = substitutive_turing_from_rauzy(a, self.le, self.lor, verb=verb)
		return [(TuringMachine(lt),s) for lt,s in R]
	
class TuringMachine:
	"""
	A Turing machine is given by a list of transitions of the form (s1, (r,w,d), s2)
	from state s1 to state s2, with read letter r, written letter w and move of the head d. 
	"""
	def __init__(self, lt, A=None):
		r"""
		A Turing machine is given by a list of transitions of the form (s1, (r,w,d), s2)
		from state s1 to state s2, with read letter r, written letter w and move of the head d.

		INPUT:

			- ``lt`` - iterable - list of transitions. A SignedGraph can also be given.
			- ``A`` - list (default: ``None``) - alphabet that gives a name to each transition

		OUTPUT:
			A TuringMachine.

		EXAMPLES::

			sage: from badic import *
			sage: TuringMachine([(0,(0,0,1),0), (0,(1,1,-1),1), (1,(1,0,-1),1), (1,(0,0,1),2), (2,(0,1,1),2), (2,(1,1,1),0)], A="abcdef")
			Turing machine with 6 transitions and 3 states (use .plot() to display the machine).
			

			# convertion from a SignedGraph
			sage: g = SignedGraph([(0,0),(0,1),(1,1),(1,0)], [1,-1])
			sage: TuringMachine(g)
			Turing machine with 4 transitions and 2 states (use .plot() to display the machine).

		"""
		if type(lt) == SignedGraph:
			lt = graph_to_turing(lt.le, lt.lor)
		self.lt = list(lt) # set of transitions
		S = {t[0] for t in lt}.union({t[-1] for t in lt})
		self.S = S # set of states
		if A is None:
			A = range(len(lt))
		self.A = list(A) # alphabet used for labeling transitions
		self.ds = dict() # dictionnary of succs
		for j,(i,_,_) in enumerate(self.lt):
			if i not in self.ds:
				self.ds[i] = []
			self.ds[i].append(j)

	def __repr__(self):
		return "Turing machine with %s transitions and %s states (use .plot() to display the machine)." % (len(self.lt), len(self.S))

	def __eq__(self, other):
		return are_equal_turing(self.lt, other.lt, li=1)
	
	def plot (self, file=None):
		r"""
		Plot the TuringMachine.

		INPUT:

			- ``file`` - string (default: ``None``) - filename where the dot file of the TuringMachine is saved.

		OUTPUT:
			A picture of the TuringMachine.

		EXAMPLES::

			sage: from badic import *
			sage: m = TuringMachine([(0,(0,0,1),0), (0,(1,1,-1),1), (1,(1,0,-1),1), (1,(0,0,1),2), (2,(0,1,1),2), (2,(1,1,1),0)], A="abcdef")
			sage: m.plot()
			455x167px 32-bit RGBA image

		"""
		return turing_aut(self.lt, A=self.A, F=[]).plot(file=file)
	
	def step(self, tape, pos, state, verb=False):
		r"""
		Compute one step of the Turing machine.

		INPUT:

			- ``tape`` - list
			- ``pos`` - int - position of the head
			- ``state`` - state of the Turing machine
			- ``verb`` - int (default: ``False``) - if > 0, print informations.

		OUTPUT:
			A couple (new pos, new state). The tape is modified in place.

		EXAMPLES::

			sage: from badic import *
			sage: m = TuringMachine([(0,(0,0,1),0), (0,(1,1,-1),1), (1,(1,0,-1),1), (1,(0,0,1),2), (2,(0,1,1),2), (2,(1,1,1),0)])
			sage: tape = [1,0,1,0,1]
			sage: m.step(tape, 2, 1)
			(1, 1)
			
			sage: tape
			[1, 0, 0, 0, 1]

		TESTS::

			sage: m = TuringMachine([(0,(0,0,1),0), (0,(1,1,-1),1), (1,(1,0,-1),1), (1,(0,0,1),2), (2,(0,1,1),2), (2,(1,1,1),0)])
			sage: tape = []
			sage: m.step(tape, 0, 0)
			Traceback (most recent call last):
			...
			RuntimeError: Out of the tape !

		"""
		if pos < 0 or pos >= len(tape):
			raise RuntimeError("Out of the tape !")
		l = tape[pos] # read
		lj = self.ds[state]
		for j in lj:
			if self.lt[j][1][0] == l:
				state2 = self.lt[j][-1]
				if verb:
					print("transition %s --%s--> %s" % (state, self.A[j], state2))
				tape[pos] = self.lt[j][1][1] # write
				state = state2 # change state
				pos += self.lt[j][1][-1] # move
				break
		else:
			raise ValueError("Can't find transition from state %s with letter %s" % (state, l))
		return pos, state

	def plot_trace (self, tape, pos=None, state=None, n=-1, size=10, thickness=1, colors=None, fontsize=12, verb=0):
		r"""
		Plot the trace of the Turing machine for n steps, or up to be out of tape.

		INPUT:

			- ``tape`` - list - the initial tape
			- ``pos`` - int - the initial position of the reading head
			- ``state`` - initial state
			- ``n`` - int - maximum number of steps
			- ``size`` - int - size of the drawing
			- ``thickness`` - int - thickness of borders
			- ``colors`` - list of names or tuples - list of colors used
			- ``fontsize`` - int - size of the font

		OUTPUT:
			A picture of the trace as a Graphics.

		EXAMPLES::

			sage: from badic import *
			sage: m = TuringMachine([(0,(0,0,1),0), (0,(1,1,-1),1), (1,(1,0,-1),1), (1,(0,0,1),2), (2,(0,1,1),2), (2,(1,1,1),0)])
			sage: m.plot_trace(10)			# random
			Graphics object consisting of 70 graphics primitives

		"""
		if type(tape) != list and type(tape) != tuple:
			try:
				ZZ(tape)
			except:
				raise ValueError("The tape is not of correct type: must be list or int.")
			mi = self.invert()
			w = mi.rand_word(tape)
			n = tape
			tape,pos,i = mi.rec_word(w, get_state=1)
			return self.plot_trace(tape, pos-mi.lt[w[-1]][1][-1], i, n=n, size=size, thickness=thickness, colors=colors, fontsize=fontsize, verb=verb)
		if pos is None:
			raise ValueError("You must give the initial position of the head.")
		if state is None:
			raise ValueError("You must give the initial state.")
		y = 0
		g = Graphics()
		while 1:
			if verb > 0:
				print("tape = %s, pos = %s, state=%s" % (tape, pos, state))
			g += plot_rub(y, tape, pos, state, size=size, thickness=thickness, colors=colors, fontsize=fontsize)
			try:
				pos, state = self.step(tape, pos, state)
			except:
				break
			y -= 1
			if y == -n:
				break
		g.axes(False)
		g.set_aspect_ratio(1)
		return g
	
	def apply_rels (self, rels):
		r"""
		Apply relations on letters of tape.

		INPUT:
			- ``rels`` - iterable - list of relations. Each relation is a couple of letters.

		OUTPUT:
			A new TuringMachine.

		EXAMPLES::

			sage: from badic import *
			sage: g = SignedGraph([(0,0),(0,1),(1,1),(1,0)], [1,-1])
			sage: m = TuringMachine(g)
			sage: m.apply_rels({(0,2),(4,3)})
			Turing machine with 4 transitions and 2 states (use .plot() to display the machine).

		"""
		return TuringMachine(apply_rels(self.lt, rels), A=self.A)
	
	def invert (self):
		r"""
		Return the inverse of the Turing machine if invertible.

		OUTPUT:
			A TuringMachine.

		EXAMPLES::

			sage: from badic import *
			sage: m = TuringMachine([(0,(0,0,1),0), (0,(1,1,-1),1), (1,(1,0,-1),1), (1,(0,1,1),0)])
			sage: m.invert()
			Turing machine with 4 transitions and 2 states (use .plot() to display the machine).

		"""
		return TuringMachine(invert_turing(self.lt), A=self.A)

	def is_deterministic (self):
		r"""
		Determine whether the Turing machine is deterministic.

		OUTPUT:
			A bool.

		EXAMPLES::

			sage: from badic import *
			sage: m = TuringMachine([(0,(0,0,1),0), (0,(1,1,-1),1), (1,(1,0,-1),1), (1,(0,1,1),0)])
			sage: m.is_deterministic()
			True
		"""
		return is_deterministic_turing(self.lt)

	def minimize (self, A=None):
		r"""
		Minimize a Turing machine.

		INPUT:

			- ``A`` - list (default: ``None``) - labels of edges for the new Turing machine

		OUTPUT:
			A new TuringMachine.

		EXAMPLES::

			sage: from badic import *
			sage: m = TuringMachine([(0,(0,0,1),0), (0,(1,1,-1),1), (1,(1,0,-1),1), (1,(0,1,1),0)])
			sage: m.minimize()
			Turing machine with 4 transitions and 2 states (use .plot() to display the machine).

		"""
		a = DetAutomaton(list(self.lt), avoidDiGraph=True)
		lt = [(i,t,k) for (i,k,t) in a.minimize().edges()]
		return TuringMachine(lt, A=A)
	
	def unsubstitute (self, A=None, verb=False):
		r"""
		Unsubstitute a Turing machine.
		Return the unsubstitued Turing machine with the substitution.

		INPUT:

			- ``A`` - list (default: ``None``) - labels of edges for the new Turing machine
			- ``verb`` - int (default: ``False``) - if > 0, print informations.

		OUTPUT:
			A couple (TuringMachine, WordMorphism).

		EXAMPLES::

			sage: from badic import *
			sage: m = TuringMachine([(0,(0,0,1),0), (0,(1,1,-1),1), (1,(1,0,-1),1), (1,(0,1,1),0)])
			sage: m.unsubstitute()
			(Turing machine with 4 transitions and 2 states (use .plot() to display the machine).,
			WordMorphism: 0->0, 1->1312, 2->2, 3->30)

		"""
		
		lt, s = turing_unsubstitute(self.lt, verb=verb)
		if A is None:
			A = s.domain().alphabet()
		s = WordMorphism({A[i]:[self.A[j] for j in s(i)] for i in s.domain().alphabet()})
		return TuringMachine(lt, A=A), s
	
	def unsubstitute_to_graph (self, minimize=False, A=None):
		r"""
		Return the unsubstitued graph with the substitution.

		INPUT:

			- ``A`` - list - labels of edges for the graph
			- ``minimize`` - bool (default: ``False``) - if True, minimize the Rauzy graph.

		OUTPUT:
			A couple (list of edges, WordMorphism).

		EXAMPLES::

			sage: from badic import *
			sage: m = TuringMachine([(0,(0,0,1),0), (0,(1,1,-1),1), (1,(1,0,-1),1), (1,(0,1,1),0)])
			sage: m.unsubstitute_to_graph()
			([(0, 0), (0, 1), (1, 1), (1, 0)], WordMorphism: 0->0, 1->1312, 2->2, 3->30)
		"""
		g,s = unsubstitute(self.lt, minimize=minimize)
		if A is None:
			A = s.domain().alphabet()
		s = WordMorphism({A[i]:[self.A[j] for j in s(i)] for i in s.domain().alphabet()})
		return g,s

	def language (self, n):
		r"""
		Return the list of words of length n recognized by the Turing machine.
		A word w is recognized if there exists a tape and a starting state such that
		w is the trace of length n from this initial configuration.

		INPUT:

			- ``n`` - int - length of words

		OUTPUT:
			A list of Word

		EXAMPLES::

			sage: from badic import *
			sage: m = TuringMachine([(0,(0,0,1),0), (0,(1,1,-1),1), (1,(1,0,-1),1), (1,(0,1,1),0)])
			sage: m.language(2)
			[word: 00,
			 word: 01,
			 word: 12,
			 word: 13,
			 word: 22,
			 word: 23,
			 word: 30,
			 word: 31]
		"""
		L = turing_language(self.lt, n)
		return [Word([self.A[i] for i in w], alphabet=self.A) for w in L]

	def rauzy_graph(self, n):
		r"""
		Return the Rauzy graph of order n of the Turing machine.

		INPUT:

			- ``n`` - int - order of the Rauzy graph

		OUTPUT:
			A DetAutomaton.

		EXAMPLES::

			sage: from badic import *
			sage: m = TuringMachine([(0,(0,0,1),0), (0,(1,1,-1),1), (1,(1,0,-1),1), (1,(0,1,1),0)])
			sage: m.rauzy_graph(2)
			DetAutomaton with 8 states and an alphabet of 4 letters

		"""
		return lang_to_rauzy_graph(self.language(n+1))

	def rauzy_graph2 (self, F=None):
		r"""
		Return the grouped Rauzy graph of the Turing machine.

		OUTPUT:
			A DetAutomaton.

		EXAMPLES::

			sage: from badic import *
			sage: m = TuringMachine([(0,(0,0,1),0), (0,(1,1,-1),1), (1,(1,0,-1),1), (1,(0,1,1),0)])
			sage: m.rauzy_graph2()
			DetAutomaton with 6 states and an alphabet of 4 letters

		"""
		return rauzy_graph2(self.lt, self.A, self.ds, F=F)
	
	def rand_word(self, n):
		r"""
		Return a random word of length n recognized by the Turing machine.
		A word w is recognized if there exists a tape and a starting state such that
		w is the trace of length n from this initial configuration.

		INPUT:

			- ``n`` - int - length of the word

		OUTPUT:
			A Word.

		EXAMPLES::

			sage: from badic import *
			sage: m = TuringMachine([(0,(0,0,1),0), (0,(1,1,-1),1), (1,(1,0,-1),1), (1,(0,1,1),0)])
			sage: m.rand_word(10)	# random
			word: 0131223001

		"""
		w = rand_word(self.lt, n)
		return Word([self.A[i] for i in w], alphabet=self.A)

	def rec_word(self, w, get_state=False, tape=None, pos=0, i=None, verb=0):
		r"""
		Determine whether the word w is recognized by the Turing machine.

		INPUT:

			- ``get_state`` - bool (default: ``False``) -  if True, return the known tape, the position and the state after trace w.
			- ``tape`` - list (default: ``None``) - initial tape
			- ``pos`` - int (default: ``0``) - initial position of reading head
			- ``i`` - initial state
			- ``verb`` - int (default: 0) - if >0, print informations

		OUTPUT:
			A bool.

		EXAMPLES::

			sage: from badic import *
			sage: m = TuringMachine([(0,(0,0,1),0), (0,(1,1,-1),1), (1,(1,0,-1),1), (1,(0,1,1),0)])
			sage: m.rec_word([0,1,1,0])
			False

		"""
		w = [self.A.index(j) for j in w] # convert the word from alphabet of self
		return rec_word(w, self.lt, get_state=get_state, i=i, tape=tape, pos=pos, verb=verb)

def rauzy_graph2 (lt, A, ds, F=None, verb=0):
	if F is None:
		F = []
	L = turing_language(lt, 2)
	R = set()
	for w in L:
		i = lt[w[-1]][-1]
		if verb > 0:
			print("i = %s" % i)
		o2 = lt[w[-1]][1][-1]
		if verb > 1:
			print("o2 = %s" % o2)
		if lt[w[-2]][1][-1] != o2:
			l = lt[w[-2]][1][1]
			if verb > 1:
				print("written letter : %s" % l)
			w = Word([A[k] for k in w], alphabet=A)
			for j in ds[i]:
				if verb > 1:
					print("lt[%s] = %s, l = %s" % (j, lt[j], l))
				if lt[j][1][0] == l:
					if o2 == lt[j][1][-1]:
						w2 = Word([A[j]], alphabet=A)
						R.add((w, A[j], w2))
						if verb > 0:
							print("Add %s --%s--> %s" % (w, A[j], w2))
					else:
						w2 = w[1:]+Word([A[j]], alphabet=A)
						R.add((w, A[j], w2))
						if verb > 0:
							print("Add %s --%s--> %s" % (w, A[j], w2))
		else:
			w = Word([A[l] for l in w], alphabet=A)
			for j in ds[i]:
				if o2 == lt[j][1][-1]:
					w2 = Word([A[j]], alphabet=A)
					R.add((w[-1:], A[j], w2))
					if verb > 0:
						print("Add %s --%s--> %s" % (w[-1:], A[j], w2))
				else:
					w2 = w[-1:]+Word([A[j]], alphabet=A)
					R.add((w[-1:], A[j], w2))
					if verb > 0:
						print("Add %s --%s--> %s" % (w[-1:], A[j], w2))
	return DetAutomaton(list(R), final_states=F, avoidDiGraph=1)

def apply_rels(lt, rels):
	"""
	Apply relations on letters of the alphabet of the tape to Turing machine
	"""
	g = Graph(list(rels)+[(i,i) for i in range(len(lt)*2)], loops=1)
	l = list(range(len(lt)*2))
	cc = g.connected_components()
	nc = len(cc)
	for i,c in enumerate(cc):
		for k in c:
			l[k] = i
	return [(i,(l[r],l[w],de),k) for i,(r,w,de),k in lt]

def rand_rauzy_graph2 (le, lor):
	"""
	Return a random Rauzy graph of order 2 with graph le and orientations lor.
	"""
	res = []
	d = dict()
	for j,(i,k) in enumerate(le):
		if i not in d:
			d[i] = []
		d[i].append(j)
	S = []
	dj = dict()
	for j,(i,k) in enumerate(le):
		dj[j] = []
		for j2 in d[k]:
			S.append((j,j2))
			dj[j].append(j2)
	#print(dj)
	i = (0, choice(dj[0])) # choose a word of length 2
	to_see = list(S)
	seen = set(to_see)
	while len(to_see) > 0:
		a,b = to_see.pop()
		#print((a,b))
		if lor[le[b][0]] != lor[le[b][1]]:
			#print("choisis")
			j = choice(dj[b])
			dj[b].remove(j)
			res.append(((a,b),j,(b,j)))
			if (b,j) not in seen:
				seen.add((b,j))
				to_see.append((b,j))
		else:
			for j in d[le[b][1]]:
				res.append(((a,b), j, (b,j)))
				#if (b,j) not in seen:
				#	seen.add((b,j))
				#	to_see.append((b,j))
		#if len(seen) < len(le)*len(le)//len(lor):
		#	to_see.append(())
	return DetAutomaton(res, avoidDiGraph=1)

def invert_turing(lt):
	"""
	invert the Turing machine
	"""
	a = DetAutomaton(lt, avoidDiGraph=1)
	am = a.mirror()
	A = a.alphabet
	L = [] # list of edges of the new automaton
	for i in range(a.n_states):
		# find moves toward this state
		sm = list(set([A[am.label(i,j)][2] for j in range(am.n_succs(i))]))
		if len(sm) != 1:
			raise ValueError("The Turing machine is not invertible: there are several moves toward state %s" % a.states[i])
		# browse outgoing transitions
		for j in range(len(A)):
			k = a.succ(i,j)
			if k != -1:
				L.append((a.states[k],(A[j][1],A[j][0],-sm[0]),a.states[i]))
	# if there is a warning that it is not deterministic, it means that the Turing machine is not invertible
	return L

def rand_word2 (lt, a, s, n, ia=None, tape=None, pos=0, i=None, l=None, verb=0):
	"""
	Find a random word of length n whose image by s is recognized by lt.
	
	a : automaton describing an SFT approximating the shift. 
	
	ia : initial state of a
	
	i : initial state of lt
	
	l : list of edges from a given state of lt
	"""
	if ia is None:
		ia = choice(range(a.n_states))
	if tape is None:
		tape = []
	if l is None:
		l = dict()
		for j,t in enumerate(lt):
			if t is None:
				continue
			if t[0] not in l:
				l[t[0]] = []
			l[t[0]].append(j)
		if verb > 1:
			print("l = %s" % l)
	r = []
	for _ in range(n):
		lc = a.succs(ia)
		while 1:
			ja = choice(lc) # choose a random edge in a from ia
			wj = s([ja])
			if i is None:
				i = lt[wj[0]][0]
			rw = rec_word(wj, lt, get_state=1, i=i, tape=copy(tape), pos=pos)
			if not rw:
				lc.remove(ja)
			else:
				break
		r.append(ja)
		tape, pos, i = rw
		ia = a.succ(ia, ja)
	return Word(r, alphabet=a.alphabet)

def is_deterministic_turing (lt):
	d = dict()
	for i,(a,_,_),_ in lt:
		if i not in d:
			d[i] = []
		elif a in d[i]:
			return False
		d[i].append(a)
	return True

def substitutive_turing (le, lor, verb=0):
	"""
	Find all substitutive Turing machines with graph le and orientations lor.
	"""
	if verb > 0:
		print("Find Rauzy graphs of order 2...")
	from badic.misc import unsubstitute as rauzy_graphs
	#R = RauzyGraphs(le, lor, 2, verb=verb)
	R = rauzy_graphs(le, lor)
	if verb > 0:
		print("%s Rauzy graphs found" % len(R))
	res = []
	for r in R:
		res += substitutive_turing_from_rauzy(r.minimize(), le, lor, verb)
	return res

def substitutive_turing_from_rauzy (a, le, lor, verb=0):
	"""
	Find Turing machines with graph le and signs of states lor,
	with a minimized Rauzy graph of order 2 a.
	"""
	g,s = unsubstitute(a)
	if verb > 0:
		print(s)
	#a = DetAutomaton([(i,j,k) for j,(i,k) in enumerate(g)], i=0, avoidDiGraph=True)
	#a.plot()
	lt = graph_to_turing(le, lor)
	lt2, rels = turing_unsubstitute_rels(lt, g, s)
	if verb > 0:
		print("relations needed to be unsubstituable: %s" % rels)
	# apply relations to Turing machines
	g = Graph(list(rels)+[(i,i) for i in range(len(le)*2)], loops=1)
	l = list(range(len(le)*2))
	cc = g.connected_components()
	nc = len(cc)
	for i,c in enumerate(cc):
		for k in c:
			l[k] = i
	lt = [(i,(l[r],l[w],de),k) for i,(r,w,de),k in lt]
	lt2 = [(i,(l[r],l[w],de),k) for i,(r,w,de),k in lt2]
	# find a isomorphism between Turing machines
	res = []
	r = are_equal_turing(lt, lt2, get_rels=1, li=1)
	if r:
		for rels, p in r:
			G = SymmetricGroup(domain=range(len(p)))
			g = G(p)
			#A = 'abcdefghijklmnopqrstuvwxyz'
			#s2 = WordMorphism({A[a]:[A[b] for b in s(g(a))] for a in s.domain().alphabet()})
			s2 = WordMorphism({i:s(g(i)) for i in s.domain().alphabet()})
			# apply new relations
			g = Graph(list(rels)+[(i,i) for i in range(nc)], loops=1)
			l = list(range(nc))
			for i,c in enumerate(g.connected_components()):
				for k in c:
					l[k] = i
			lt3 = [(i,(l[r],l[w],de),k) for i,(r,w,de),k in lt]
			if is_deterministic_turing(lt3):
				res.append((lt3,s2))
			elif verb > 1:
				print("Non deterministic automaton.")
	return res

def turing_unsubstitute(lt, verb=0):
	"""
	Unsubstitute the Turing machine into another Turing machine.
	"""
	R = []
	g,s = unsubstitute(lt)
	d = dict() # dictionnary of entering letters
	for k,(_,j) in enumerate(g):
		if j not in d:
			d[j] = []
		d[j].append(k)
	if verb > 0:
		print(d)
	for j in d:
		# check that last letters of each entering edges write and move identically
		l = set()
		for k in d[j]:
			l.add(lt[s(k)[-1]][1][1:])
		if verb > 0:
			print("%s : %s" % (j,l))
		if len(l) != 1:
			raise ValueError("Entering edges at %s disagree: %s" % (j, l))
		d[j] = l.pop()
	for k in range(len(g)):
		w = s(k)
		if verb > 0:
			print("k = %s" % k)
			print("w = %s" % w)
		i = g[k][0]
		tape = [d[i][0]]
		pos = d[i][1]
		if verb > 1:
			print("before : %s %s" % (tape, pos))
		tape, pos, i = rec_word(w, lt, 1, None, tape, pos)
		if verb > 1:
			print("after : %s %s %s" % (tape, pos, i))
			print("attendu : %s" % list(d[g[k][-1]]))
		if len(tape) != 2:
			raise RuntimeError("tape after execution was expected to have length 2, not %s !" % len(tape))
		de = d[g[k][-1]][-1]
		r = lt[w[0]][1][0]
		if pos < 0:
			w = tape[1]
		else:
			w = tape[0]
		if verb > 0:
			dep = ['-',0,'+']
			print("%s|%s%s" % (r,w,dep[de+1]))
		R.append((g[k][0],(r,w,de),g[k][1]))
	return R, s

def graph_to_turing (le, lor):
	"""
	Return a Turing machine corresponding to graph le and signs of states lor.
	"""
	return [(i,(j,j+len(le),lor[k]),k) for j,(i,k) in enumerate(le)]

def turing_unsubstitute_rels (lt, g, s, verb=0):
	"""
	Return relations that allow to unsubstitute the Turing machine into another Turing machine with graph g and substitution s.
	"""
	rels = set()
	R = []
	d = dict() # dictionnary of entering letters
	for k,(_,j) in enumerate(g):
		if j not in d:
			d[j] = []
		d[j].append(k)
	if verb > 0:
		print(d)
	for j in d:
		# check that last letters of each entering edges write and move identically
		l = set()
		for k in d[j]:
			l.add(lt[s(k)[-1]][1][1:])
		if verb > 0:
			print("%s : %s" % (j,l))
		if len(l) != 1:
			#raise ValueError("Entering edges at %s disagree: %s" % (j, l))
			l = list(l)
			for i,de in l:
				if de != l[0][-1]:
					raise ValueError("Different signs at state %s" % j)
				rels.add((l[0][0], i))
		d[j] = l.pop()
	for k in range(len(g)):
		w = s(k)
		if verb > 0:
			print("k = %s" % k)
			print("w = %s" % w)
		i = g[k][0]
		tape = [d[i][0]]
		pos = d[i][1]
		if verb > 1:
			print("before : %s %s" % (tape, pos))
		rels2, tape, pos, i = rec_word_rels(w, lt, 1, None, tape, pos)
		rels = rels.union(rels2)
		if verb > 1:
			print("after : %s %s %s" % (tape, pos, i))
			print("attendu : %s" % list(d[g[k][-1]]))
		if len(tape) != 2:
			raise RuntimeError("tape after execution was expected to have length 2, not %s !" % len(tape))
		de = d[g[k][-1]][-1]
		r = lt[w[0]][1][0]
		if pos < 0:
			w = tape[1]
		elif pos == 2:
			w = tape[0]
		else:
			raise ValueError("Position not permitted")
		if verb > 0:
			dep = ['-',0,'+']
			print("%s|%s%s" % (r,w,dep[de+1]))
		R.append((g[k][0],(r,w,de),g[k][1]))
	return R, rels

def turing_unsubstitute_ (lt, getL=1, nrg = 4, N=10000):
	"""
	Unsubstitute the Turing machine lt.
	
	nrg : order of Rauzy graph
	N : length of random chosen word
	"""
	G,s = unsubstitute(lt)
	L = turing_language2(lt, G, nrg, s)
	a = lang_to_rauzy_graph(L).minimize()
	w = rand_word2(lt, a, s, N)[1:]
	return turing_from_word(G, w, getL=getL), s

def turing_aut (lt, A=None, F=None):
	"""
	Return a DetAutomaton representing the Turing machine.
	"""
	lt2 = [(x,(i,j),y) for i,(x,j,y) in enumerate(lt)]
	at = DetAutomaton(lt2, final_states=F, avoidDiGraph=1)
	lp = ['0','+','-']
	if A is None:
		A = range(at.n_letters)
	at.set_alphabet(["%s|%s%s(%s)" % (x,y,lp[z],A[i]) for i,(x,y,z) in at.alphabet])
	return at

def graph_aut (le, A=None, F=None, lor=None):
	"""
	Return a DetAutomaton representing the graph.
	"""
	le2 = [(x,i,y) for i,(x,y) in enumerate(le)]
	at = DetAutomaton(le2, final_states=F, avoidDiGraph=1)
	if A is None:
		A = range(at.n_letters)
	at.set_alphabet(["%s" % A[i] for i in at.alphabet])
	if lor is not None:
		A = ['-',0,'+']
		at.set_states([A[i+1] for i in lor])
	return at

def simple_paths (a):
	"""
	Find simple words of length >=1 of a to a final state
	"""
	R = []
	for j in a.succs(a.initial_state):
		i = a.succ(a.initial_state, j)
		w = []
		w.append(j)
		while 1:
			lj = a.succs(i)
			if len(lj) != 1:
				break
			i = a.succ(i,lj[0])
			w.append(lj[0])
		R.append((a.initial_state, Word(w), i))
	return R

def unsubstitute (lt, minimize=False):
	"""
	Unsubstitute a Turing machine or a SFT graph.
	"""
	if type(lt) == list or type(lt) == tuple:
		#L = turing_language(lt, 3)
		#L = [Word(w) for w in L]
		#a = lang_to_rauzy_graph(L)
		a = TuringMachine(lt).rauzy_graph2()
		if minimize:
			a = a.minimize()
	else:
		a = lt
	# find states with several leaving edges
	ls = []
	for i in range(a.n_states):
		if len(a.succs(i)) > 1:
			ls.append(i)
	# find substitution and transitions of the new graph
	a.set_final_states(ls)
	ne = 0 # number of edges
	d = dict() # dictionnary of substitution
	G = [] # graph
	for i in ls:
		a.set_initial_state(i)
		for i,w,k in simple_paths(a):
			d[ne] = w
			G.append((i,k))
			ne += 1
	ds = dict() # dictionnary of states
	ns = 0
	for i,k in G:
		if i not in ds:
			ds[i] = ns
			ns += 1
		if k not in ds:
			ds[k] = ns
			ns += 1
	# relabel states
	G = [(ds[i], ds[k]) for i,k in G]
	return G, WordMorphism(d)

def are_equal_turing_rec (lt1, lt2, d1, d2, seen, to_see, l, ls, la, s, li, get_rels, rels, verb=0):
	"""
	l[j] is the letter of g2 corresponding to letter j of g1
	ls[i] is the state of g2 corresponding to state i of g1
	la[k] is the letter of the tape of g2 corresponding to letter k of tape of g1
	s : sign
	"""
	lr = []
	while len(to_see) > 0:
		i = to_see.pop()
		lj = d1[i]
		lj2 = d2[ls[i]]
		if len(lj) != len(lj2):
			if verb > 0:
				print("State %s of g1 has %s outgoing edges but state %s of g2 has %s outgoing edges." % (i,len(lj),ls[i],len(lj2)))
			return False
		ljN = [j for j in lj if l[j] is None] # edges of g1 with image not yet chosen
		ljl = {l[j] for j in lj if l[j] is not None}
		lj2N = [j for j in lj2 if j not in ljl] # edges of g2 with image not yet chosen
		if len(ljN) != len(lj2N):
			if verb > 0:
				print("Edges not chosen from %s do not correspond to edges not chosen from %s" % (i,ls[i]))
		for g in SymmetricGroup(domain=range(len(ljN))):
			# make a choice
			seen2 = copy(seen)
			to_see2 = copy(to_see)
			ls2 = copy(ls)
			l2 = copy(l)
			la2 = copy(la)
			rels2 = copy(rels)
			for jj,j in enumerate(ljN):
				l2[j] = lj2N[g(jj)]
				r,w,di = lt1[j][1]
				r2,w2,di2 = lt2[l2[j]][1]
				if di2*s != di:
					if verb > 1:
						print("incompatible signs for transitions %s in lt1 and %s in lt2" % (j, l2[j]))
					break
				if la2[r] is None:
					la2[r] = r2
				else:
					if la2[r] != r2:
						if get_rels:
							if verb > 1:
								print("Add relation %s=%s between reads" % (la2[r],r2))
							rels2.add((la2[r], r2))
						else:
							if verb > 1:
								print("incompatible reads for transitions %s in lt1 and %s in lt2" % (j, l2[j]))
							break
				if la2[w] is None:
					la2[w] = w2
				else:
					if la2[w] != w2:
						if get_rels:
							if verb > 1:
								print("Add relation %s=%s between writes" % (la2[w],w2))
							rels2.add((la2[w],w2))
						else:
							if verb > 1:
								print("incompatible writes for transitions %s in lt1 and %s in lt2" % (j, l2[j]))
							break
				k = lt1[j][-1]
				k2 = lt2[l2[j]][-1]
				if ls2[k] is None:
					ls2[k] = k2
				else:
					if ls2[k] != k2:
						if verb > 1:
							print("incompatible arrival states for transitions %s in lt1 and %s in lt2" % (j, l2[j]))
						break # impossible choice
				if k not in seen2:
					seen2.add(k)
					to_see2.append(k)
			else:
				r = are_equal_turing_rec(lt1, lt2, d1, d2, seen2, to_see2, l2, ls2, la2, s, li, get_rels, rels2, verb)
				if r:
					if li:
						lr += r
					else:
						return r
		if li:
			return lr
		return False
	if verb > 0:
		print("ls = %s" % ls)
		print("la = %s" % la)
		print("s = %s" % s)
		print("li = %s" % li)
		print("get_rels = %s" % get_rels)
		print("l = %s" % l)
	if li:
		if get_rels:
			return [(rels,l)]
		else:
			return [l]
	if get_rels:
		return rels,l
	else:
		return l
	
def are_equal_turing (lt1, lt2, li=0, get_rels=0, verb=0):
	"""
	Find if the two Turing machine are identical modulo relabeling.
	Return the map that send edges of lt1 to edges of lt2.
	
	g1,g2 : DetAutomaton
	li : if True, return the list of possibilities
	
	"""
	ls1 = {t[0] for t in lt1}.union({t[-1] for t in lt1})
	ls2 = {t[0] for t in lt2}.union({t[-1] for t in lt2})
	if len(ls1) != len(ls2):
		if verb > 0:
			print("The two Turing machine have different number of states.")
		return False
	if len(lt1) != len(lt2):
		if verb > 0:
			print("The two Turing machine have different number of edges.")
		return False
	d1 = dict()
	d2 = dict()
	for j,(t1,t2) in enumerate(zip(lt1, lt2)):
		if t1[0] not in d1:
			d1[t1[0]] = []
		d1[t1[0]].append(j)
		if t2[0] not in d2:
			d2[t2[0]] = []
		d2[t2[0]].append(j)
	nA = len({t[1][0] for t in lt1}.union({t[1][1] for t in lt1})) # length of alphabet of the tape of lt1
	lr = []
	for i2 in ls2:
		for s in [1,-1]:
			to_see = [0]
			seen = set(to_see)
			l = [None for _ in lt1]
			ls = [None for _ in ls1]
			la = [None for _ in range(nA)]
			ls[0] = i2
			if verb > 0:
				print("Test with initial states 0 and %s, and sign %s" % (i2,s))
			r = are_equal_turing_rec (lt1, lt2, d1, d2, seen, to_see, l, ls, la, s, li, get_rels, set(), verb)
			if r:
				if li:
					lr += r
				else:
					return r
	if li:
		return lr
	return False

def are_equal_graphs_rec (g1, g2, seen, to_see, l, ls, li, get_ls=0, verb=0):
	"""
	l[j] is the letter of g2 corresponding to letter j of g1
	ls[i] is the state of g2 corresponding to state i of g1
	"""
	if verb > 2:
		print("aegr: seen=%s" % seen)
		print("to_see=%s" % to_see)
		print("l = %s" % l)
		print("ls = %s" %ls)
	lr = []
	while len(to_see) > 0:
		i = to_see.pop()
		lj = g1.succs(i)
		lj2 = g2.succs(ls[i])
		if len(lj) != len(lj2):
			if verb > 0:
				print("State %s of g1 has %s outgoing edges but state %s of g2 has %s outgoing edges." % (i,len(lj),ls[i],len(lj2)))
			return False
		ljN = [j for j in lj if l[j] is None] # edges of g1 with image not yet chosen
		ljl = {l[j] for j in lj if l[j] is not None}
		lj2N = [j for j in lj2 if j not in ljl] # edges of g2 with image not yet chosen
		if len(ljN) != len(lj2N):
			if verb > 0:
				print("Edges not chosen from %s do not correspond to edges not chosen from %s" % (i,ls[i]))
		for g in SymmetricGroup(domain=range(len(ljN))):
			# make a choice
			seen2 = copy(seen)
			to_see2 = copy(to_see)
			ls2 = copy(ls)
			l2 = copy(l)
			for jj,j in enumerate(ljN):
				l2[j] = lj2N[g(jj)]
				k = g1.succ(i,j)
				k2 = g2.succ(ls[i], l2[j])
				if ls2[k] is None:
					ls2[k] = k2
				else:
					if ls2[k] != k2:
						break # impossible choice
				if k not in seen2:
					seen2.add(k)
					to_see2.append(k)
			else:
				r = are_equal_graphs_rec(g1, g2, seen2, to_see2, l2, ls2, li, get_ls, verb)
				if li:
					lr += r
				elif r:
					return r
		if li:
			return lr
		return False
	if verb > 0:
		print("ls = %s" % ls)
		print("l = %s" % l)
	if li:
		if get_ls:
			return [(l,ls)]
		else:
			return [l]
	if get_ls:
		return (l,ls)
	return l
	
def are_equal_graphs (g1, g2, li=False, get_ls=0, verb=0):
	"""
	Find if the two labeled graphs are identical modulo relabeling.
	Return the map that send alphabet of g1 to the alphabet of g2.
	
	g1,g2 : DetAutomaton
	li : if True, return the list of possibilities
	
	"""
	if type(g1) == list:
		g1 = graph_aut(g1)
	if type(g2) == list:
		g2 = graph_aut(g2)
	if g1.n_states != g2.n_states:
		if verb > 0:
			print("The two graphs have different number of states.")
		if li:
			return []
		return False
	if g1.n_letters != g2.n_letters:
		if verb > 0:
			print("The two graphs have different number of letters.")
		if li:
			return []
		return False
	lr = []
	for i2 in range(g2.n_states):
		to_see = [0]
		seen = set(to_see)
		l = [None for _ in g1.alphabet]
		ls = [None for _ in g1.states]
		ls[0] = i2
		if verb > 0:
			print("Test with initial states 0 and %s" % i2)
		r = are_equal_graphs_rec (g1,g2, seen, to_see, l, ls, li, get_ls, verb)
		if li:
			lr += r
		elif r:
			return r
	if li:
		return lr
	return False

def are_equal_signed_graphs_rec (g1, g2, lsi1, lsi2, seen, to_see, l, ls, li, get_ls=0, verb=0):
	"""
	l[j] is the letter of g2 corresponding to letter j of g1
	ls[i] is the state of g2 corresponding to state i of g1
	l1[i] is the sign of state i
	"""
	lr = []
	while len(to_see) > 0:
		i = to_see.pop()
		lj = g1.succs(i)
		lj2 = g2.succs(ls[i])
		if len(lj) != len(lj2):
			if verb > 0:
				print("State %s of g1 has %s outgoing edges but state %s of g2 has %s outgoing edges." % (i,len(lj),ls[i],len(lj2)))
			return False
		ljN = [j for j in lj if l[j] is None] # edges of g1 with image not yet chosen
		ljl = {l[j] for j in lj if l[j] is not None}
		lj2N = [j for j in lj2 if j not in ljl] # edges of g2 with image not yet chosen
		if len(ljN) != len(lj2N):
			if verb > 0:
				print("Edges not chosen from %s do not correspond to edges not chosen from %s" % (i,ls[i]))
		for g in SymmetricGroup(domain=range(len(ljN))):
			# make a choice
			seen2 = copy(seen)
			to_see2 = copy(to_see)
			ls2 = copy(ls)
			l2 = copy(l)
			for jj,j in enumerate(ljN):
				l2[j] = lj2N[g(jj)]
				k = g1.succ(i,j)
				k2 = g2.succ(ls[i], l2[j])
				if ls2[k] is None:
					if lsi1[k] != lsi2[k2]:
						if verb > 0:
							print("incompatible signs")
						break # choice incompatible with signs
					ls2[k] = k2
				else:
					if ls2[k] != k2:
						if verb > 0:
							print("incompatible graphs")
						break # impossible choice
				if k not in seen2:
					seen2.add(k)
					to_see2.append(k)
			else:
				r = are_equal_signed_graphs_rec(g1, g2, lsi1, lsi2, seen2, to_see2, l2, ls2, li, get_ls, verb)
				if li:
					lr += r
				elif r:
					return r
		if li:
			return lr
		return False
	if li:
		if get_ls:
			return [(l,ls)]
		else:
			return [l]
	if get_ls:
		return (l,ls)
	return l
	
def are_equal_signed_graphs (g1, g2, li1, li2, li=False, get_ls=0, verb=0):
	"""
	Find if the two labeled graphs are identical modulo relabeling.
	Return the map that send alphabet of g1 to the alphabet of g2.
	
	g1,g2 : DetAutomaton
	li : if True, return the list of possibilities
	li1 : list of signs of states of g1
	li2: list of signs of states of g2
	"""
	if type(g1) == list:
		g1 = graph_aut(g1)
	if type(g2) == list:
		g2 = graph_aut(g2)
	if g1.n_states != g2.n_states:
		if verb > 0:
			print("The two graphs have different number of states.")
		if li:
			return []
		return False
	if g1.n_letters != g2.n_letters:
		if verb > 0:
			print("The two graphs have different number of letters.")
		if li:
			return []
		return False
	lr = []
	for i2 in range(g2.n_states):
		to_see = [0]
		seen = set(to_see)
		l = [None for _ in g1.alphabet]
		ls = [None for _ in g1.states]
		ls[0] = i2
		if li1[0] != li2[i2]:
			li2 = [-s for s in li2]
		if verb > 0:
			print("Test with initial states 0 and %s" % i2)
		r = are_equal_signed_graphs_rec (g1,g2, li1, li2, seen, to_see, l, ls, li, get_ls, verb)
		if li:
			lr += r
		elif r:
			return r
	if li:
		return lr
	return False

def words (a, n):
	"""
	Return words of length n of DetAutomaton a.
	"""
	R = []
	to_see = [(a.initial_state,[])]
	while len(to_see) > 0:
		i,w = to_see.pop()
		if len(w) == n:
			if a.is_final(i):
				R.append(w)
			continue
		for j in a.succs(i):
			k = a.succ(i,j)
			to_see.append((k, Word(w+[j], alphabet=range(a.n_letters))))
	return R

def sft_words (a, n):
	"""
	Return words of length n of SFT with automaton a.
	"""
	R = set()
	for i in range(a.n_states):
		a.set_initial_state(i)
		R = R.union(words(a, n))
	return R

def sft_to_rauzy_graph (a, n):
	"""
	Return the Rauzy graph of order n of SFT with automaton a.
	"""
	L = sft_words(a, n)
	L = [Word(w) for w in L]
	rg = lang_to_rauzy_graph(L)
	return rg

def word_to_rauzy_graph (w, n):
	"""
	Return the Rauzy graph of order n from a word w.
	"""
	edges = set()
	for i in range(len(w)-n-1):
		edges.add((w[i:i+n], w[i+n], w[i+1:i+n+1]))
	return DetAutomaton(list(edges), avoidDiGraph=True)

def get_vor2 (a):
	"""
	Get the direction vector of the Turing machine from an SFT approximating its shift.
	"""
	rg = sft_to_rauzy_graph(a, 3)
	return get_vor(rg)

def turing_from_word (g, w, getL=0, vor=None, i=None, tape=None, pos=0, verb=0):
	"""
	Return a Turing machine with graph g recognizing word w.
	"""
	if len(w) < len(g):
		raise ValueError("Word is too short !")
	if vor is None:
		vor = get_vor2(word_to_rauzy_graph(w, 2))
		if verb > 0:
			print("vor = %s" % vor)
	if tape is None:
		tape = []
	# initial state
	if i is None:
		i = g[w[0]][0]
	lr = [j for j in range(len(g))]
	lw = [len(g)+j for j in range(len(g))]
	for j in w:
		if verb > 1:
			sign = ['-',0,'+']
			print("%s (%s1) %s %s %s" % (j, sign[vor[j]+1], tape, pos, i))
			print("lr = %s, lw = %s" % (lr, lw))
		if len(tape) <= pos:
			tape.append(lw[j])
		elif pos < 0:
			tape = [lw[j]]+tape
			pos += 1
		else:
			if tape[pos] != lr[j]:
				if verb > 1:
					print("%s == %s" % (tape[pos], lr[j]))
				# update lw and lr values
				for k in range(len(g)):
					if lw[k] == tape[pos]:
						lw[k] = lr[j]
					if lr[k] == tape[pos]:
						lr[k] = lr[j]
			tape[pos] = lw[j]
		pos += vor[j]
		i = g[j][-1]
	if verb > 0:
		print("lr = %s" % lr)
		print("lw = %s" % lw)
	# relabel letters in order to be consecutive integers from 0
	ls = set(lr).union(set(lw))
	ils = dict()
	for j,i in enumerate(ls):
		ils[i] = j
	lr = [ils[i] for i in lr]
	lw = [ils[i] for i in lw]
	if verb > 0:
		print("lr = %s" % lr)
		print("lw = %s" % lw)
	if getL:
		return [(g[i][0],(lr[i],lw[i],vor[i]),g[i][-1]) for i in range(len(g))]
	dir = ['-','0','+']
	L = [(g[i][0],"%s|%s%s"%(lr[i],lw[i],dir[vor[i]+1]),g[i][-1]) for i in range(len(g))]
	at = DetAutomaton(L, avoidDiGraph=1)
	return at

def turing_from_words (g, L, getL=0, vor=None, verb=0):
	"""
	Return a Turing machine with graph g recognizing words of L.
	"""
	if vor is None:
		vor = get_vor2(lang_to_rauzy_graph(L))
		if verb > 0:
			print("vor = %s" % vor)
	lr = [j for j in range(len(g))]
	lw = [len(g)+j for j in range(len(g))]
	for w in L:
		i = g[w[0]][0] # initial state
		tape = []
		pos = 0
		for j in w:
			if verb > 1:
				sign = ['-',0,'+']
				print("%s (%s1) %s %s %s" % (j, sign[vor[j]+1], tape, pos, i))
				print("lr = %s, lw = %s" % (lr, lw))
			if len(tape) <= pos:
				tape.append(lw[j])
			elif pos < 0:
				tape = [lw[j]]+tape
				pos += 1
			else:
				if tape[pos] != lr[j]:
					if verb > 1:
						print("%s == %s" % (tape[pos], lr[j]))
					# update lw and lr values
					for k in range(len(g)):
						if lw[k] == tape[pos]:
							lw[k] = lr[j]
						if lr[k] == tape[pos]:
							lr[k] = lr[j]
				tape[pos] = lw[j]
			pos += vor[j]
			i = g[j][-1]
	if verb > 0:
		print("lr = %s" % lr)
		print("lw = %s" % lw)
	# relabel letters in order to be consecutive integers from 0
	ls = set(lr).union(set(lw))
	ils = dict()
	for j,i in enumerate(ls):
		ils[i] = j
	lr = [ils[i] for i in lr]
	lw = [ils[i] for i in lw]
	if verb > 0:
		print("lr = %s" % lr)
		print("lw = %s" % lw)
	if getL:
		return [(g[i][0],(lr[i],lw[i],vor[i]),g[i][-1]) for i in range(len(g))]
	dir = ['-','0','+']
	L = [(g[i][0],"%s|%s%s"%(lr[i],lw[i],dir[vor[i]+1]),g[i][-1]) for i in range(len(g))]
	at = DetAutomaton(L, avoidDiGraph=1)
	return at	

def getTuring2 (g, a, N, getL=0, verb=0):
	"""
	Return the Turing machine with graph g and SFT of order N described by automaton a.
	
	g : a list of edges of a graph
	a : a DetAutomaton
	N : order
	"""
	rg = sft_to_rauzy_graph(a, 3)
	vor = get_vor2(rg)
	if verb > 0:
		print("vor = %s" % vor)
	raise NotImplemented("Not yet implemented, sorry...")

def prune2 (a):
	"""
	Remove every state without leaving or without entering edges.
	"""
	am = a.mirror()
	ls = []
	for i in range(a.n_states):
		if am.n_succs(i) != 0 and len(a.succs(i)) != 0:
			ls.append(i)
	return a.sub_automaton(ls)

def get_vor (rg, verb=0):
	"""
	Compute the orientation vector from the Rauzy graph of order 2
	or from the list words of length 3 of the language.
	"""
	if type(rg) == list:
		L = [Word(w) for w in rg]
		rg = lang_to_rauzy_graph(L)
	rg = prune2(rg)
	cc = rg.strongly_connected_components()
	to_see = [c[0] for c in cc]
	if verb > 0:
		print("to_see = %s" %to_see)
	seen = set(to_see)
	vor = zero_vector(len(rg.alphabet))
	S = rg.states
	vor[S[to_see[-1]][-2]] = 1 # choose an orientation
	while len(to_see) > 0:
		i = to_see.pop()
		a = S[i][-2]
		b = S[i][-1]
		if verb > 0:
			print("%s%s" % (a,b))
			print("vor = %s" % vor)
		if len(rg.succs(i)) == 1:
			# vor[a] != vor[b]
			if vor[a] != 0 and vor[b] != 0 and vor[b] != -vor[a]:
				raise ValueError("Incompatible %s%s has a single succ at state %s !" % (a,b, i))
			if vor[a]:
				vor[b] = -vor[a]
			else:
				vor[a] = -vor[b]
		else:
			# vor[a] == vor[b]
			if vor[a] != 0 and vor[b] != 0 and vor[b] != vor[a]:
				raise ValueError("Incompatible %s%s has %s succs at state %s !" % (a,b, len(rg.succs(i)), i))
			if vor[a]:
				vor[b] = vor[a]
			else:
				vor[a] = vor[b]
		for j in rg.succs(i):
			k = rg.succ(i,j)
			if k not in seen:
				seen.add(k)
				to_see.append(k)
	return vor

def language (self, n):
	r"""
	Return words of length n of the language of the substitution.
	"""
	if n == 0:
		return set(Word([], alphabet=self.codomain().alphabet()))
	if n == 1:
		return self.codomain().alphabet()
	# find words of length 2
	to_see = []
	for a in language(self, n-1): #self.domain().alphabet():
		sa = self(a)
		for i in range(len(sa)-n+1):
			to_see.append(sa[i:i+n])
	seen = set(to_see)
	while len(to_see) > 0:
		w = to_see.pop()
		sw = self(w)
		for i in range(len(sw)-n+1):
			ssw = sw[i:i+n]
			if ssw not in seen:
				to_see.append(ssw)
				seen.add(ssw)
	return seen

def lang_to_rauzy_graph (L, use_badic=None):
	"""
	Compute the Rauzy graph of order n from words of length n+1 of the language
	"""
	if use_badic is None:
		try:
			from badic.cautomata import DetAutomaton
			use_badic = True
		except:
			use_badic = False
	elif use_badic:
		from badic.cautomata import DetAutomaton
	R = []
	for w in L:
		if use_badic:
			R.append((w[:-1],w[-1],w[1:]))
		else:
			R.append((w[:-1],w[1:],w[-1]))
	if use_badic:
		return DetAutomaton(R, avoidDiGraph=True)
	else:
		return DiGraph(R, loops=True)
	
def rauzy_graph(s, n, use_badic=None):
	"""
	Compute the Rauzy graph of order n of s.
	"""
	L = s.language(n+1)
	return lang_to_rauzy_graph(L, use_badic)
	
def turing_language (lt, n, leq=0, i=None, l=None, ns=None, tape=[], pos=0, verb=0):
	"""
	Return all words of length n recognized by the Turing machine,
	with initial state i, or from every state if i is None.
	"""
	if n == 0:
		return [[]]
	if ns is None:
		ns = len(set([t[0] for t in lt if t is not None]))
		if verb > 1:
			print("ns = %s" % ns)
	if l is None:
		l = dict() #[[] for i in range(ns)]
		for j,t in enumerate(lt):
			if t is None:
				continue
			if t[0] not in l:
				l[t[0]] = []
			l[t[0]].append(j)
		if verb > 1:
			print("l = %s" % l)
	if i is None:
		ls = list({t[0] for t in lt if t is not None})
	else:
		ls = [i]
	if leq:
		R = [Word([], alphabet=range(len(lt)))]
	else:
		R = []
	if verb > 1:
		print(ls)
	for i in ls:
		if i not in l:
			continue
		for j in l[i]:
			r,w,d = lt[j][1]
			pos2 = pos
			if len(tape) <= pos:
				tape2 = tape+[w]
			elif pos < 0:
				tape2 = [w]+tape
				pos2 = pos+1
			else:
				if tape[pos] != r:
					if verb > 0:
						print("should have read %s rather than %s" % (tape[pos],r))
					continue
				tape2 = copy(tape)
				tape2[pos] = w
			pos2 = pos2+d
			R += [Word([j], alphabet=range(len(lt)))+w for w in turing_language(lt, n-1, leq, lt[j][2], l, ns, tape2, pos2, verb=verb)]
	#R = [Word(r, alphabet=range(len(lt))) for r in R] # fait tout crasher pour une raison inconnue !!!
	return R

def turing_language2 (lt, g, n, s, leq=0, i=None, l=None, ns=None, tape=None, pos=0, verb=0):
	"""
	Return all words of length n whose image by s is recognized by the Turing machine,
	with initial state i, or from every state if i is None.
	
	s : a WordMorphism
	l : dict that associate list of edges from each state
	ns : number of states
	i : initial state in g
	
	"""
	if verb > 1:
		print("tl2 %s %s %s" % (i, pos, tape))
	if tape is None:
		tape = []
#	if s is None:
#		s = WordMorphism({i:[i] for i in range(len(lt))})
	if n == 0:
		return [Word([], alphabet=range(len(g)))]
	ls = None
	if ns is None:
		ls = list(set([t[0] for t in g if t is not None]).union(set([t[-1] for t in g if t is not None])))
		ns = len(ls)
		if verb > 1:
			print("ns = %s" % ns)
	if l is None:
		l = dict() #[[] for i in range(ns)]
		for j,t in enumerate(g):
			if t is None:
				continue
			if t[0] not in l:
				l[t[0]] = []
			l[t[0]].append(j)
		if verb > 1:
			print("l = %s" % l)
	if i is None:
		if ls is None:
			ls = list(set([t[0] for t in g if t is not None]).union(set([t[-1] for t in g if t is not None])))
	else:
		ls = [i]
	if verb > 1:
		print("ls = %s" % ls)
	if leq:
		R = [[]]
	else:
		R = []
	if verb > 1:
		print(ls)
	for i in ls:
		if i not in l:
			continue
		for j in l[i]:
			wj = s(j)
			# test if word wj is recognized by the Turing machine
			if verb > 3:
				print("test rec s(%s) = %s with %s %s i=%s" % (j, wj, tape, pos, i))
			rw = rec_word(wj, lt, get_state=1, i=lt[wj[0]][0], pos=pos, tape=copy(tape))
			if not rw:
				if verb > 2:
					print("word s(%s) = %s not recognized !" % (j, s(j)))
				continue
			tape2, pos2, i2 = rw
			####
			# Faut-il écrire la dernière lettre à écrire ?
			####
			R += [Word([j], alphabet=range(len(g)))+w for w in turing_language2(lt, g, n-1, s, leq, g[j][-1], l, ns, tape2, pos2, verb=verb)]
	#R = [Word(r, alphabet=range(len(lt))) for r in R] # fait tout crasher pour une raison inconnue !!!
	return R

def rec_word (w, lt, get_state=0, i=None, tape=None, pos=0, verb=0):
	"""
	Test if word w is recognized by the Turing machine given by list of transitions lt.
	
	if get_state, return also the tape, position and state
	"""
	if tape is None:
		tape = []
	if len(w) == 0:
		if get_state:
			return [], 0, None
		return True
	# initial state
	if lt[w[0]] is None:
		return False
	if i is None:
		i = lt[w[0]][0]
	for j in w:
		if verb > 1:
			print(pos, tape)
			print(lt[j])
		if lt[j] is None:
			if verb > 0:
				print("this transition %s does not exists" % j)
			return False
		if i != lt[j][0]:
			if verb > 0:
				print("invalid sequence of transitions")
			return False
		r,w,d = lt[j][1]
		if len(tape) <= pos:
			tape.append(w)
		elif pos < 0:
			tape = [w]+tape
			pos += 1
		else:
			if tape[pos] != r:
				if verb > 0:
					print("should have read %s rather than %s" % (tape[pos],r))
				return False
			tape[pos] = w
		pos += d
		i = lt[j][2]
	if get_state:
		return tape, pos, i
	return True

def rec_word_rels (w, lt, get_state=0, i=None, tape=None, pos=0, verb=0):
	"""
	Test if word w is recognized by the Turing machine given by list of transitions lt.
	
	if get_state, return also the tape, position and state
	"""
	rels = set()
	if tape is None:
		tape = []
	if len(w) == 0:
		if get_state:
			return rels, [], 0, None
		return rels
	# initial state
	if lt[w[0]] is None:
		return False
	if i is None:
		i = lt[w[0]][0]
	for j in w:
		if verb > 1:
			print(pos, tape)
			print(lt[j])
		if lt[j] is None:
			if verb > 0:
				print("this transition %s does not exists" % j)
			return False
		if i != lt[j][0]:
			if verb > 0:
				print("invalid sequence of transitions")
			return False
		r,w,d = lt[j][1]
		if len(tape) <= pos:
			tape.append(w)
		elif pos < 0:
			tape = [w]+tape
			pos += 1
		else:
			if tape[pos] != r:
				rels.add((tape[pos],r))
			tape[pos] = w
		pos += d
		i = lt[j][2]
	if get_state:
		return rels,tape, pos, i
	return rels

def lor_to_vor (le, lor):
	"""
	Compute orientation of edges from orientation of states of le.
	"""
	vor = [0 for _ in range(len(le))]
	for j,(_,k) in enumerate(le):
		vor[j] = lor[k]
	return vor

def rand_word (lt, n, leq=0, A=None, ls=None, tape=None, pos=0, i=None, get_rel=0, verb=0):
	"""
	Return a word w of length n recognized by the Turing machine given by list of transitions lt.
	"""
	if tape is None:
		tape = []
	if ls is None:
		ls = list({t[0] for t in lt if t is not None}.union({t[2] for t in lt if t is not None})) # list of states
	ds = dict()
	for k,s in enumerate(ls):
		ds[s] = k
	if A is None: # tape alphabet
		A = list({t[1][0] for t in lt if t is not None}.union({t[1][1] for t in lt if t is not None}))
	#loe = [[None for _ in A] for _ in range(len(ls))] # list of outgoing edges for each state
	#for j,t in enumerate(lt):
	#	if t is not None:
	#		loe[ds[t[0]]][t[1][0]] = j
	loe = [[] for _ in range(len(ls))]
	for j,t in enumerate(lt):
		loe[ds[t[0]]].append(j)
	if verb > 0:
		print("loe = %s" % loe)
	# initial state
	R = []
	if i is None:
		i = choice(range(len(ls))) # choose a random initial state
	for k in range(n):
		if verb > 1:
			print(pos, tape)
		if len(tape) <= pos:
			if len(loe[i]) == 0:
				raise RuntimeError("No way to continue random word.")
			j = choice(loe[i])
			tape.append(lt[j][1][0])
		elif pos < 0:
			if len(loe[i]) == 0:
				raise RuntimeError("No way to continue random word.")
			j = choice(loe[i])
			tape = [lt[j][1][0]]+tape
			pos = 0
		else:
			for j in loe[i]:
				if lt[j][1][0] == tape[pos]:
					break
			else:
				if get_rel == 1:
					return (tape[pos], lt[choice(loe[i])][1][0])
				elif get_rel == 2:
					return (tape[pos], [lt[j][1][0] for j in loe[i]])
				else:
					raise ValueError("Incompatibility after %s letters !" % k)
		if verb > 1:
			print("i=%s, j=%s" % (ls[i],j))
		if j is None:
			if leq or len(R) == n:
				break
			raise RuntimeError("Random word not found after %s letters." % k)
		R.append(j)
		if lt[j] is None:
			if leq or len(R) == n:
				break
			raise RuntimeError("Random word not found after %s letters." % k)
		r,w,d = lt[j][1]
		tape[pos] = w
		pos += d
		i = ds[lt[j][2]]
	return Word(R, alphabet=range(len(lt)))

def more_than (u, v, A=None, order=None, verb=False):
	"""
	Return an automaton recognizing words less than or equal to uv^oo.
	"""
	if A is None:
		A = list(set(u).union(set(v)))
		A.sort()
		if verb:
			print("Choose A=%s" % A)
	if order is None:
		order = lambda x: x[0] > x[1]
	e = len(u)+len(v)
	L = [(e,i,e) for i in A]
	for i,a in enumerate(u):
		L.append((i,a,i+1))
		for b in A:
			if order((b,a)):
				L.append((i,b,e))
	for i,a in enumerate(v):
		L.append((len(u)+i, a, len(u)+(i+1)%len(v)))
		for b in A:
			if order((b,a)):
				L.append((len(u)+i,b,e))
	return DetAutomaton(L, i=0, avoidDiGraph=True)
 
def split_list(self, la, algo_inter=1):
	"""
	Split self with respect to list la.
	We assume that the union of la cover self.
	"""
	return [self.intersection(a, algo=algo_inter) for a in la]
