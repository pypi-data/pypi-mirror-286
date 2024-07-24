struct List
{
	unsigned int *l;
	unsigned int n;
};
typedef struct List List;

struct Substitution
{
	unsigned int *ls; // list of images
	unsigned int *pos; // list of positions of images
	// ls[pos[i]:pos[i+1]] is the image of letter i
};
typedef struct Substitution Substitution;

// chained list of substitutions and graphs
struct SubstitutionGraphsList
{
	Substitution *s;
	unsigned int *le; // list of edges
	unsigned int ne; // number of edges
	struct SubstitutionGraphsList *next;
};
typedef struct SubstitutionGraphsList SubstitutionGraphsList;

// chained list of automata
struct AutomataList
{
	Automaton *a; // an automaton
	struct AutomataList *next;
};
typedef struct AutomataList AutomataList;

// chained list of substitutions
struct SubstitutionsList
{
	Substitution *s;
	struct SubstitutionsList *next;
};
typedef struct SubstitutionsList SubstitutionsList;

SubstitutionGraphsList DecomposeGraph (NAutomaton *a, unsigned int ar);

void CETn(double x, double *v, int nv, double tau, int niter, double **proj, int nd, double *res);
SubstitutionsList *RauzyGraphs2 (int *le, int n, int8_t *lor, int ar);
void FreeSubstitutionsList(SubstitutionsList *sl);

AutomataList *appendAut (AutomataList *l, Automaton *a);
void FreeAutomataList(AutomataList *sl);

// Find quotiented Rauzy graphs of order 2 from list of edges le and orientations lor
// edges are (le[2*i], le[2*i+1])
// states are assumed to be from 0 to k-1
AutomataList *Unsubstitute (unsigned int *le, unsigned int n, int8_t *lor, unsigned int ar);
void FreeSubstitutionGraphsList(SubstitutionGraphsList *sl);

// allocate a new substitution with n letters and sum of lengths of images N
Substitution *new_subst (int n, int N);

