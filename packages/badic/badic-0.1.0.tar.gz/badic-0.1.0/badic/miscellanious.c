#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include "Automaton.h"
#include "automataC.h"
#include "miscellanious.h"

#define VERB	0
#define TEST	0

AutomataList *appendAut (AutomataList *l, Automaton *a)
{
	AutomataList *r = malloc(sizeof(AutomataList));
	r->next = l;
	r->a = a;
	return r;
}

SubstitutionGraphsList *appendGL (SubstitutionGraphsList *l, Substitution *s, unsigned int *le, unsigned int ne)
{
	SubstitutionGraphsList *r = malloc(sizeof(SubstitutionGraphsList));
	r->next = l;
	r->s = s;
	r->le = le;
	r->ne = ne;
	return r;
}

void print_NAutomaton (NAutomaton *a)
{
	printf("NAutomaton with %d state and %d letters\n", a->n, a->na);
	for (int i=0;i<a->n;i++)
	{
		for (int j=0;j<a->e[i].n;j++)
		{
			printf("%d --%d--> %d\n", i, a->e[i].a[j].l, a->e[i].a[j].e);
		}
	}
}

void print_Aut (Automaton *a)
{
	printf("DetAutomaton([");
	for (int i=0;i<a->n;i++)
	{
		for (int j=0;j<a->na;j++)
		{
			int k = a->e[i].f[j];
			if (k != -1)
				printf("(%d, %d, %d),", i, j, a->e[i].f[j]);
		}
	}
	printf("])\n");
}

// decompose an Automaton as a coboundary graph and a substitution
SubstitutionGraphsList DecomposeGraph (NAutomaton *a, unsigned int ar)
{
#if VERB
	print_NAutomaton(a);
#endif
	unsigned int i, j, k, c, ne, pos;
	SubstitutionGraphsList r;
	uint8_t *seen = calloc(a->n, sizeof(uint8_t)); // seen states
	unsigned int *stack = malloc(a->n*sizeof(unsigned int)); // states to see
	unsigned int n = 1; // position in stack
	// find a starting state
	for (i=0;i<a->n;i++)
	{
		if (a->e[i].n > 1)
		{
			stack[0] = i; // start with state i
			seen[i] = 1;
			break;
		}
	}
#if VERB
	printf("starting state %d\n", i);
#endif
	// count states of result
	c = 0;
	for (i=0;i<a->n;i++)
	{
		if (a->e[i].n > 1)
		{
			c++;
		}
	}
#if VERB
	printf("result graph has %d states\n", c);
#endif
	// allocate memory for the result
	r.ne = c*ar;
	r.le = malloc(2*r.ne*sizeof(unsigned int));
	r.s = new_subst(r.ne, r.ne + a->n-c);
	r.s->pos[0] = 0;
	ne = 0;
	//
	c = 0; // count the number of edges of the new graph
	while (n > 0)
	{
#if VERB
		printf("stack = [ ");
		for (j=0;j<n;j++)
		{
			printf("%d ", stack[j]);
		}
		printf("]\n");
#endif
		// pop a state i
		n--;
		i = stack[n];
		//
		for (j=0;j<a->e[i].n;j++)
		{
#if VERB
			printf("j = %d, edge %d --%d--> %d\n", j, i, a->e[i].a[j].l, a->e[i].a[j].e);
#endif
			pos = r.s->pos[c];
			r.s->ls[pos] = a->e[i].a[j].l;
			k = a->e[i].a[j].e;
			pos++;
			while (a->e[k].n == 1)
			{
				r.s->ls[pos] = a->e[k].a[0].l;
				k = a->e[k].a[0].e;
				pos++;
			}
#if VERB
			printf("s(%d) = ", c);
			for (int o=r.s->pos[c];o<pos;o++)
			{
				printf("%d ", r.s->ls[o]);
			}
			printf(" (%d - %d) arrival state %d \n", r.s->pos[c], pos, k);
#endif
			c++;
			r.s->pos[c] = pos;
			// add edge (i,k)
#if TEST
			if (2*ne+1 >= r.ne)
			{
				printf("Error ne = %d > %d = r.ne !!!\n", ne, r.ne);
				return r;
			}
#endif
			r.le[2*ne] = i;
			r.le[2*ne+1] = k;
#if VERB
			printf("add edge (%d,%d)\n", i, k);
#endif
			ne++;
			//
#if TEST
			if (k >= a->n)
			{
				printf("Error k=%d > %d = a->n !!!\n", k, a->n);
				return r;
			}
			if (n >= a->n)
			{
				printf("Error n=%d > %d = a->n !!!\n", n, a->n);
				return r;
			}
#endif
			if (!seen[k])
			{
#if VERB
				printf("Add state %d to stack\n", k);
#endif
				seen[k] = 1;
				stack[n] = k;
				n++;
			}
		}
	}
	free(seen);
	free(stack);
	return r;
}

// a : automaton currently in construction
// le : list of edges of the initial graph
// n : length of le
// lor : list of orientations for each state
// ar : arity (length of lor is n/ar)
// vsuc : vsuc[i] is the list (of length ar) of possible successors from letter i
// letter1 : letter1[i] is the first letter of state i
// letter2 : letter2[i] is the last letter of state i
// seen : seen[i] encode which edges of the Rauzy graph have already been seen
// pile : stack
// np : current position in stack
// ma : such that (pile[i] >> ma, pile[i] % (1 << ma)) is the state of Rauzy graph in the pile at position i
void unsubstitute_rec (Automaton *a, const unsigned int *le, const unsigned int n, const int8_t *lor, const unsigned int ar,
		const unsigned int *letter1, const unsigned int *letter2, uint8_t *seen, uint8_t *seen_state,
		unsigned int *pile, unsigned int np, AutomataList **res)
{
	int i;
	unsigned int j, k, b, c;
#if VERB
	printf("uns_rec pile=[ ");
	for (i=0;i<np;i++)
	{
		printf("%d ", pile[i]);
	}
	printf("] seen = [");
	for (i=0;i<n;i++)
	{
		if (lor[le[2*i]] == lor[le[2*i+1]])
			printf(" %d", seen[i]);
		else
			printf(" (%d %d)", seen[i] & 1, (seen[i] & (1<<1)) >> 1);
	}
	printf(" ]\n");
	fflush(stdout);
#endif
	while (np > 0)
	{
		// unstack a state b
		np--;
		b = pile[np];
#if VERB
		printf("unstack %d\n", b);
#endif
		//
		if (lor[le[2*letter2[b]]] == lor[le[2*letter2[b]+1]])
		{ // constant sign
#if VERB
			printf("cste sign\n");
#endif
			for (i=0;i<ar;i++)
			{
				c = letter2[b]*ar + i; // next state
				a->e[b].f[letter2[c]] = c; // add the edge to the automaton
#if VERB
				printf("Add edge %d --%d--> %d\n", b, letter2[c], c);
#endif
				if (!seen_state[c])
				{
					pile[np] = c; // add the state to the stack
					np++;
					seen_state[c] = 1; // set as seen
				}
				//seen[letter2[b]] |= 
			}
		}else
		{ // different signs
#if VERB
			printf("diff signs\n");
#endif
			// find the last possibility of connexion
			for (i=ar-1;i>=0;i--)
			{
				if (!(seen[letter2[b]] & (1 << i)))
					break;
			}
			//
#if VERB
			printf("last poss of conn : %d\n", i);
#endif
			if (i < 0)
				return; // impossible to connect
			
			for (k=0;k<i;k++)
			{
				if (!(seen[letter2[b]] & (1 << k)))
				{
#if VERB
					printf("k = %d\n", k);
#endif
					unsigned int np2 = np;
					// copy
#if VERB
					printf("Allocate a2 of size %d, pile2 of size %d, seens2 of size %d, seen_state2 of size %d\n", sizeof(Automaton), a->n, n, a->n);
#endif
					Automaton *a2 = malloc(sizeof(Automaton));
					*a2 = CopyAutomaton(*a, a->n, a->na);
					unsigned int *pile2 = malloc(a->n*sizeof(unsigned int));
					for (j=0;j<np;j++)
					{
						pile2[j] = pile[j];
					}
					uint8_t *seen2 = malloc(n*sizeof(uint8_t));
					uint8_t *seen_state2 = malloc(a->n*sizeof(uint8_t));
					for (j=0;j<n;j++)
					{
						seen2[j] = seen[j];
					}
					seen2[letter2[b]] |= (1 << k);
					for (j=0;j<a->n;j++)
					{
						seen_state2[j] = seen_state[j];
					}
					//
					c = letter2[b]*ar + k; // next state
					a2->e[b].f[letter2[c]] = c; // add the edge to the automaton
#if VERB
					printf("Add edge %d --%d--> %d\n", b, letter2[c], c);
#endif
					if (!seen_state[c])
					{
						pile2[np] = c; // add the state to the stack
						np2++;
						seen_state2[c] = 1; // set as seen
					}
					unsubstitute_rec(a2, le, n, lor, ar, letter1, letter2, seen2, seen_state2, pile2, np2, res);
#if VERB
					printf("Free after rec, k=%d\n", k);
#endif
					free(seen2);
					free(seen_state2);
					free(pile2);
					FreeAutomaton(a2);
					free(a2);
				}
			}
			
			// last choice of connexion
			seen[letter2[b]] |= (1 << i); // indicate it has been seen
			c = letter2[b]*ar + i; // next state
			a->e[b].f[letter2[c]] = c; // add the edge to the automaton
#if VERB
			printf("come back to i=%d\n", i);
			printf("Add edge %d --%d--> %d\n", b, letter2[c], c);
#endif
			if (!seen_state[c])
			{
				pile[np] = c; // add the state to the stack
				np++;
				seen_state[c] = 1; // set as seen
			}
		}
	}
	// test if strongly connected
	for (i=0;i<a->n;i++)
	{
		if (!seen_state[i])
		{
#if VERB
			printf("Not strongly connected: state %d not seen.\n", i);
#endif
			return;
		}
	}
#if VERB
	printf("*** Add a new result: DetAutomaton with %d states and %d letters. ***\n", a->n, a->na);
#endif
	// save the result
	Automaton *a2 = malloc(sizeof(Automaton));
	*a2 = CopyAutomaton(*a, a->n, a->na);
	for (i=0;i<a->n;i++)
	{
		a2->e[i].final = 1;
	}
	a2->i = -1;
	// append found automaton to the chained list
	*res = appendAut(*res, a2);
	return;
	
	//////////////////////////////////////////////////

/*
	print_Aut(a);
	return; //////////////////////////////////////////////////////////////////////////////////////////////
	Automaton a2 = Minimise(*a, 1); // minimize
#if VERB
	printf("Min aut with %s states\n", a2.n);
#endif
	return; /////////////////////////////////////////////////////////////////////////////////////////////
	//NAutomaton a3 = NewNAutomaton(a2.n, a2.na);
	//CopyDN(&a2, &a3, 0); // convert to a NAutomaton
	NAutomaton a3 = CopyN(a2, 0);
	FreeAutomaton(&a2);
	SubstitutionGraphsList r = DecomposeGraph(&a3, ar);
#if VERB
	printf("Free after decomposition...\n");
#endif
	FreeNAutomaton(&a3);
	// append found substitution and graph to the chained list
//	res->last->s = r.s;
//	res->last->le = r.le;
//	res->last->ne = r.ne;
//	res->last->next = malloc(sizeof(SubstitutionGraphsList));
//	res->last = res->last->next;
//	res->last->next = NULL;
	//
#if VERB
	printf("...freed\n");
#endif
*/
}

// Find quotiented Rauzy graphs of order 2 from list of edges le and orientations lor
// edges are (le[2*i], le[2*i+1])
// states are assumed to be from 0 to k-1
AutomataList *Unsubstitute (unsigned int *le, unsigned int n, int8_t *lor, unsigned int ar)
{
	unsigned int i, j, k;
	AutomataList *res = malloc(sizeof(AutomataList));
	res->next = NULL;
#if VERB
	printf("le = [");
	for (i=0;i<n;i++)
	{
		printf("(%d, %d) ", le[2*i], le[2*i+1]);
	}
	printf("]\n");
	printf("lor = [");
	for (i=0;i<n/ar;i++)
	{
		printf("%d ", lor[i]);
	}
	printf("]\n");
	fflush(stdout);
#endif
	// find list of possible successors for each vertex
	k = n/ar;
	List *vsuc = malloc(sizeof(List)*k);
	for (i=0;i<k;i++)
	{
		vsuc[i].l = malloc(ar*sizeof(unsigned int));
		vsuc[i].n = 0;
	}
	for (j=0;j<n;j++)
	{
		i = le[2*j];
		vsuc[i].l[vsuc[i].n] = j;
		vsuc[i].n++;
	}
#if VERB
	for (i=0;i<k;i++)
	{
		printf("vsuc[%d] = ", i);
		for (j=0;j<ar;j++)
			printf("%d ", vsuc[i].l[j]);
		printf("\n");
	}
	fflush(stdout);
#endif
	// seen[i] & (1<<j) is whether the jth possibility from letter i has been already taken
	uint8_t *seen = calloc(n, sizeof(uint8_t));
	Automaton *a = malloc(sizeof(Automaton));
	*a = NewAutomaton(n*ar, n);
#if TEST
	printf("Allocate DetAutomaton a with %d states and %d letters.\n", a->n, a->na);
#endif
	uint8_t *seen_state = calloc(a->n, sizeof(uint8_t));
	unsigned int *letter1 = malloc(a->n*sizeof(unsigned int));
	unsigned int *letter2 = malloc(a->n*sizeof(unsigned int));
	//unsigned int **next_state = malloc(a.n*sizeof(unsigned int *));
	for (i=0;i<n;i++)
	{
		for (j=0;j<ar;j++)
		{
			letter1[i*ar+j] = i;
			letter2[i*ar+j] = vsuc[le[2*i+1]].l[j];
		}
	}
#if VERB
	for (i=0;i<a->n;i++)
	{
		printf("%d : %d %d\n", i, letter1[i], letter2[i]);
	}
	fflush(stdout);
#endif
	/*
	for (i=0;i<a.n;i++)
	{
		next_state[i] = malloc(ar*sizeof(unsigned int));
		b = state2[i];
		for (j=0;j<ar;j++)
		{
			next_state[i][j] = b*ar+j;
		}
	}
	*/
	//Substitution *s = new_subst(n, n*ar);
	unsigned int *pile = malloc(sizeof(unsigned int)*n*ar);
	pile[0] = 0; // start by state 0
	seen_state[0] = 1;
	unsubstitute_rec(a, le, n, lor, ar, letter1, letter2, seen, seen_state, pile, 1, &res);
#if VERB
	printf("Free memory...\n");
	fflush(stdout);
#endif
	for (i=0;i<k;i++)
	{
		free(vsuc[i].l);
	}
	free(vsuc);
	free(letter1);
	free(letter2);
	free(seen);
	free(seen_state);
	free(pile);
	//FreeAutomaton(&a);
	//free(a);
	return res;
}

// allocate a new substitution with n letters and sum of lengths of images N
Substitution *new_subst (int n, int N)
{
	Substitution *s = malloc(sizeof(Substitution));
	s->ls = calloc(N, sizeof(unsigned int));
	s->pos = calloc(n+1, sizeof(unsigned int));
	return s;
}

// copy substitution with n letters and sum of lengths of images N
Substitution *copy_subst (const Substitution *s, int n, int N)
{
	Substitution *r = malloc(sizeof(Substitution));
	r->ls = malloc(N*sizeof(unsigned int));
	r->pos = malloc((n+1)*sizeof(unsigned int));
	memcpy(r->ls, s->ls, N*sizeof(unsigned int));
	memcpy(r->pos, s->pos, (n+1)*sizeof(unsigned int));
	return r;
}

// free a substitution
void free_subst (Substitution *s)
{
	free(s->ls);
	free(s->pos);
	free(s);
}

void FreeSubstitutionsList(SubstitutionsList *sl)
{
	if (sl->next != NULL)
	{
		FreeSubstitutionsList(sl->next);
		free_subst(sl->s);
		free(sl->next);
	}
}

void FreeSubstitutionGraphsList(SubstitutionGraphsList *sl)
{
	if (sl->next != NULL)
	{
		FreeSubstitutionGraphsList(sl->next);
		free_subst(sl->s);
		free(sl->le);
		free(sl->next);
	}
}

void FreeAutomataList(AutomataList *sl)
{
	if (sl->next != NULL)
	{
		FreeAutomataList(sl->next);
		//FreeAutomaton(sl->a);
		//free(sl->a);
		free(sl->next);
	}
}

void RauzyGraphs2_rec (Substitution *s, const int *le, const unsigned int n, const int8_t *lor, const unsigned int ar, const List *vsuc, uint8_t *seen, unsigned int ci, unsigned int cpos, SubstitutionsList *res)
{
	unsigned int i, cl, k, ci0 = ci;
	//bool ok;
#if VERB
	printf("RG2 ci=%d, cpos=%d seen = [", ci, cpos);
	fflush(stdout);
	for (i=0;i<n;i++)
	{
		if (lor[le[2*i]] == lor[le[2*i+1]])
			printf(" %d", seen[i]);
		else
			printf(" (%d %d)", seen[i] & 1, (seen[i] & (1<<1)) >> 1);
	}
	printf(" ]\n");
#endif
	//s : current substitution
	//ci : current letter
	//cpos : current position in ls
	
	while (ci < n && lor[le[2*ci]] == lor[le[2*ci+1]])
	{
		s->ls[cpos] = ci;
#if VERB
		printf("lettre forcée %d\n", ci);
#endif
		//printf("incr seen[%d]\n", ci);
		//seen[ci]++;
		cpos++;
		ci++;
/*
		if (ci < n)
		{
			// test if there is a remaining spot
			ok = false;
			for (k=0;k<n;k++)
			{
				if (lor[le[2*k]] == lor[le[2*k+1]] && seen[k] != ar && seen[k] != 0)
				{
					ok = true;
					break;
				}
			}
			if (!ok)
			{
#if VERB
				printf("Not strongly connected !!!\n");
#endif
				for (k=ci0;k<ci;k++)
				{
					//printf("decr seen %d-%d\n", ci0, ci);
					//printf("decr seen[%d]\n", s->ls[s->pos[k+1]-1]);
					seen[s->ls[s->pos[k+1]-1]]--;
				}
				return;
			}
			//
		}
*/
#if VERB
		printf("ci = %d\n", ci);
#endif
		s->pos[ci] = cpos;
	}
	if (ci == n)
	{
		if (cpos == n*ar) // check that strongly connected
		{
			// append found substitution to the chained list
			//res->last->s = copy_subst(s, n, n*ar);
			//res->last->next = malloc(sizeof(SubstitutionsList)); //////////////////////////////////////////
			//res->last = res->last->next;
			//res->last->next = NULL;
#if VERB
			printf("strongly connected component added.\n");
#endif
		}else
		{
#if VERB
			printf("not strongly connected\n");
#endif
		}
	}else
	{
		if (s->pos[ci] == cpos)
		{ // seen for the first time: the image starts by ci
			s->ls[cpos] = ci;
#if VERB
			printf("add forced letter %d\n", ci);
#endif
			cpos++;
		}
		// make a choice for the following letter
		cl = s->ls[cpos-1]; // current letter
		for (i=0;i<ar;i++)
		{
			if (!(seen[cl] & (1 << i)))
			{ // this choice has not yet been made
				unsigned int ci2 = ci, cpos2 = cpos;
				seen[cl] |= (1 << i);
				s->ls[cpos] = vsuc[le[cl*2+1]].l[i];
#if VERB
				printf("%d->", ci);
				for (k=s->pos[ci];k<cpos;k++)
				{
					printf("%d", s->ls[k]);
				}
				printf(": choose letter %d (%d-%d)\n", s->ls[cpos], s->pos[ci], cpos);
#endif
				if (lor[le[s->ls[cpos]*2]] == lor[le[s->ls[cpos]*2+1]])
				{ // the new letter chosen has constant orientation
					//printf("incr seen[%d]\n", s->ls[cpos]);
					//seen[s->ls[cpos]]++;
					ci2++;
					s->pos[ci2] = cpos+1;
/*
					if (ci2 < n)
					{
						// test if there is a remaining spot
						ok = false;
						for (k=0;k<ci2;k++)
						{
							if (lor[le[2*k]] == lor[le[2*k+1]] && seen[k] != ar && seen[k] != 0)
							{
								ok = true;
								break;
							}
						}
						if (!ok)
						{
#if VERB
							printf("Not strongly connected !!!\n");
#endif
							seen[cl] &= ~(1 << i);
							for (k=ci;k<ci2;k++)
							{
								//printf("decr seen %d-%d\n", ci0, ci);
								//printf("decr seen[%d]\n", s->ls[s->pos[k+1]-1]);
								seen[s->ls[s->pos[k+1]-1]]--;
							}
							continue;
						}
						//
					}
*/
#if VERB
					printf("change ci to %d\n", ci2);
#endif
				}
				cpos2++;
				RauzyGraphs2_rec(s, le, n, lor, ar, vsuc, seen, ci2, cpos2, res);
				seen[cl] &= ~(1 << i);
/*
				for (k=ci;k<ci2;k++)
				{
					//printf("decr seen %d-%d\n", ci, ci2);
					//printf("decr seen[%d]\n", s->ls[s->pos[k+1]-1]);
					seen[s->ls[s->pos[k+1]-1]]--;
				}
*/
			}
		}
	}
/*
	for (k=ci0;k<ci;k++)
	{
		//printf("decr seen %d-%d\n", ci0, ci);
		//printf("decr seen[%d]\n", s->ls[s->pos[k+1]-1]);
		seen[s->ls[s->pos[k+1]-1]]--;
	}
*/
#if VERB
	fflush(stdout);
#endif
}

// Find quotiented Rauzy graphs of order 2 from list of edges le and orientations lor
// edges are (le[2*i], le[2*i+1])
// states are assumed to be from 0 to k-1
SubstitutionsList *RauzyGraphs2 (int *le, int n, int8_t *lor, int ar)
{
	int i,j,k;
#if VERB
	printf("le = [");
	for (i=0;i<n;i++)
	{
		printf("(%d, %d) ", le[2*i], le[2*i+1]);
	}
	printf("]\n");
	printf("lor = [");
	for (i=0;i<n/ar;i++)
	{
		printf("%d ", lor[i]);
	}
	printf("]\n");
#endif
	// compute orientation of edges
	int8_t *vor = (int8_t *)malloc(sizeof(int8_t)*n);
	for (i=0;i<n;i++)
	{
		vor[i] = lor[le[2*i+1]];
	}
	// find list of possible successors for each vertex
	k = n/ar;
	List *vsuc = malloc(sizeof(List)*k);
	for (i=0;i<k;i++)
	{
		vsuc[i].l = malloc(ar*sizeof(unsigned int));
		vsuc[i].n = 0;
	}
	for (j=0;j<n;j++)
	{
		i = le[2*j];
		vsuc[i].l[vsuc[i].n] = j;
		vsuc[i].n++;
	}
/*
	// find list of possible predecessors for each vertex
	List *vpred = malloc(sizeof(List)*k);
	for (i=0;i<k;i++)
	{
		vpred[i].l = malloc(arity*sizeof(unsigned int));
		vpred[i].n = 0;
	}
	for (j=0;j<n;j++)
	{
		i = le[2*j+1];
		vpred[i].l[vpred[i].n] = j;
		vpred[i].n++;
	}
*/
	// seen[i] & (1<<j) is whether the jth possibility from letter i has been already taken
	uint8_t *seen = calloc(n, sizeof(uint8_t));
	Substitution *s = new_subst(n, n*ar);
	SubstitutionsList *res = malloc(sizeof(SubstitutionsList));
	res->next = NULL;
	//res->last = res;
	RauzyGraphs2_rec(s, le, n, lor, ar, vsuc, seen, 0, 0, res);
	for (i=0;i<k;i++)
	{
		free(vsuc[i].l);
		//free(vpred[i].l);
	}
	free(vsuc);
	//free(vpred);
	free(vor);
	return res;
}

int which_int (double x, double *sv, int nv)
{
	int i;
	for (i=0;i<nv;i++)
	{
		if (x <= sv[i+1])
			return i;
	}
	return -1;
}
/*
// plot the Rauzy fractal of the word w in the numpy array im, for the projection V
void rauzy_fractal_plot (int *w, int n, PyArrayObject *V, PyArrayObject *im)
{
	// test that im has the correct dimensions
    if (im->nd != 2)
    {
        printf("Error: numpy array im must be two-dimensional (here %d-dimensional).", im->nd);
        return;
    }
    if (im->strides[1] != 4)
    {
        printf("Error: pixels must be stored with 4 bytes (RGBA format). Here %ld bytes/pixel.", im->strides[1]);
        return;
    }
    // test that V has correct dimensions
    if (V->nd != 2)
    {
        printf("Error: numpy array V must be two-dimensional (here %d-dimensional).", V->nd);
        return;
    }
    if (V->dimensions[0] != 2)
    {
    	printf("Error: the projection V must be to dimension 2 (here {}).", V->dimensions[0]);
    }
    
    int sx = im->dimensions[1];
    int sy = im->dimensions[0];
    int na = V->dimensions[1]; // taille de l'alphabet
    double *v = (double *)malloc(sizeof(double)*na);
    int i;
    for (i=0;i<na;i++)
    {
    	v[i] = 0;
    }
    //double *x = (double *)
    
    
    // TODO !!!!
    
}
*/

void CETn (double x, double *v, int nv, double tau, int niter, double **proj, int dp, double *xmp)
{
	double *sv = (double *)malloc(sizeof(double)*(nv+1));
	int i, j, k;
	double s = 0;
	//printf("[");
	for (i=0;i<nv;i++)
	{
		//printf("%lf, ", s);
		sv[i] = s;
		s += v[i];
	}
	//printf("%lf]\n", s);
	sv[nv] = s;
	int *p = (int *)malloc(sizeof(int)*nv);
	for (i=0;i<nv;i++)
	{
		p[i] = 0;
	}
	double *xp = (double *)malloc(sizeof(double)*dp); // current point
	//double *xmp = (double *)malloc(sizeof(double)*dp); // minimum point
	for (i=0;i<dp;i++)
	{
		xp[i] = 0;
		xmp[i] = 1./0.;
	}
	//printf("iterate...\n");
	// iterate the CETn
	for (i=0;i<niter;i++)
	{
		x = x - (int)x;
		//printf("x=%lf\n", x);
		j = which_int(x, sv, nv);
		//printf("j = %d\n", j);
		if (j < 0)
		{
			printf("Error : %ld is not in an intervalle !\n", x);
		}
		p[j]++;
		for (k=0;k<dp;k++)
		{
			xp[k] += proj[j][k];
			if (xp[k] < xmp[k])
				xmp[k] = xp[k];
		}
		x = sv[j]+sv[j+1] - x + tau;
	}
	//printf("free...\n");
	free(xp);
	free(p);
	free(sv);
}
