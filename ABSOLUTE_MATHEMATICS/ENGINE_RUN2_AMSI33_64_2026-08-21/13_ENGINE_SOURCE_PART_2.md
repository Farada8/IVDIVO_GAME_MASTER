# ENGINE SOURCE PART 2/4 — RUN2

## `admissibility_audit.py`
```python
from __future__ import annotations
def posthoc_risk(metadata):
 flags=[]
 if not metadata.get('declared_before_target_evaluation',False):flags.append('NOT_PREREGISTERED')
 if metadata.get('forbids_only_target_direct_map',False):flags.append('TARGET_SPECIFIC_FORBIDDANCE')
 if not metadata.get('external_resource_or_physical_grounding'):flags.append('NO_EXTERNAL_GROUNDING')
 if metadata.get('symmetry_test_passed') is False:flags.append('SYMMETRY_FAILURE')
 return {'risk':'HIGH' if len(flags)>=2 else ('MEDIUM' if flags else 'LOW'),'flags':flags,'note':'This is an engineering audit heuristic, not a theorem about researcher intent.'}
```

## `branch_bound.py`
```python
from __future__ import annotations
from collections import defaultdict
from .partition import markov_lumpability_defect,canonical
def _partitions_of_group(items):
 items=list(items)
 if not items:yield [];return
 first=items[0]
 for rest in _partitions_of_group(items[1:]):
  yield [{first}]+[set(b) for b in rest]
  for i in range(len(rest)):
   p=[set(b) for b in rest];p[i].add(first);yield p
def search_partition(P,labels,epsilon=0.0,node_budget=100000):
 groups=defaultdict(list)
 for i,l in enumerate(labels):groups[l].append(i)
 group_parts=[list(_partitions_of_group(v)) for v in groups.values()];visited=0;best=None
 def rec(k,acc):
  nonlocal visited,best
  if visited>=node_budget:return
  if k==len(group_parts):
   visited+=1;p=[set(x) for x in acc]
   if best is not None and len(p)>best[0]:return
   d=markov_lumpability_defect(P,p)
   if d<=epsilon+1e-12:
    cand=(len(p),d,canonical(p))
    if best is None or cand<best:best=cand
   return
  for gp in sorted(group_parts[k],key=len):
   if visited>=node_budget:break
   lb=len(acc)+len(gp)+(len(group_parts)-k-1)
   if best is not None and lb>best[0]:continue
   rec(k+1,acc+gp)
 rec(0,[])
 if best is None:return {'status':'BUDGET_EXHAUSTED_OR_INFEASIBLE','visited':visited,'budget':node_budget}
 return {'status':'FOUND','state_count':best[0],'defect':best[1],'blocks':[list(x) for x in best[2]],'visited':visited,'budget':node_budget}
```

## `cmi_uncertainty.py`
```python
from __future__ import annotations
import random
from .information import conditional_mutual_information
def permutation_test_cmi(x,y,z,n_perm=200,seed=0):
 obs=conditional_mutual_information(x,y,z);rng=random.Random(seed);yp=list(y);strata={}
 for i,zz in enumerate(z):strata.setdefault(zz,[]).append(i)
 exceed=0;null=[]
 for _ in range(n_perm):
  perm=yp[:]
  for ids in strata.values():
   vals=[yp[i] for i in ids];rng.shuffle(vals)
   for i,vv in zip(ids,vals):perm[i]=vv
  v=conditional_mutual_information(x,perm,z);null.append(v);exceed+=v>=obs-1e-15
 p=(exceed+1)/(n_perm+1);return {'observed_bits':obs,'p_value':p,'n_perm':n_perm,'null_mean':sum(null)/len(null) if null else None}
def bootstrap_cmi(x,y,z,n_boot=200,seed=0,alpha=0.05):
 if not(len(x)==len(y)==len(z)):raise ValueError('LENGTH_MISMATCH')
 n=len(x);rng=random.Random(seed);vals=[]
 for _ in range(n_boot):
  idx=[rng.randrange(n) for _ in range(n)];vals.append(conditional_mutual_information([x[i] for i in idx],[y[i] for i in idx],[z[i] for i in idx]))
 vals.sort();lo=vals[int((alpha/2)*(n_boot-1))];hi=vals[int((1-alpha/2)*(n_boot-1))]
 return {'estimate_bits':conditional_mutual_information(x,y,z),'ci':[lo,hi],'alpha':alpha,'n_boot':n_boot}
```

## `construction_report.py`
```python
from .pareto import pareto_front
DEFAULT_KEYS=['depth','communication_bits','memory_bits','time_cost']
def normalize_candidate(c):
 out=dict(c)
 for k in DEFAULT_KEYS:
  if out.get(k) is None:out[k]=float('inf')
 return out
def report_construction_spectrum(candidates,keys=None):
 keys=keys or DEFAULT_KEYS;norm=[normalize_candidate(c) for c in candidates];front=pareto_front(norm,keys);return {'keys':keys,'candidates':norm,'pareto_front':front,'total':len(norm),'non_dominated':len(front)}
```

## `controlled_psr.py`
```python
from itertools import product
from .belief_state import FinitePOMDP
def enumerate_tests(n_actions,n_observations,max_len=2):
 tests=[tuple()];atoms=list(product(range(n_actions),range(n_observations)))
 for L in range(1,max_len+1):tests.extend(product(atoms,repeat=L))
 return tests
def predictive_vector(model,belief,tests):return [model.test_probability(belief,t) for t in tests]
def controlled_system_matrix(model,beliefs,tests):return [predictive_vector(model,b,tests) for b in beliefs]
def numeric_rank(matrix,tol=1e-10):
 A=[list(map(float,row)) for row in matrix]
 if not A:return 0
 m=len(A);n=len(A[0]);r=0
 for c in range(n):
  pivot=max(range(r,m),key=lambda i:abs(A[i][c]),default=None)
  if pivot is None or abs(A[pivot][c])<=tol:continue
  A[r],A[pivot]=A[pivot],A[r];pv=A[r][c];A[r]=[x/pv for x in A[r]]
  for i in range(m):
   if i==r:continue
   f=A[i][c]
   if abs(f)>tol:A[i]=[A[i][j]-f*A[r][j] for j in range(n)]
  r+=1
  if r==m:break
 return r
def controlled_predictive_rank(model,beliefs,max_test_len=2,tol=1e-10):
 tests=enumerate_tests(model.n_actions,model.n_observations,max_test_len);M=controlled_system_matrix(model,beliefs,tests);return {'rank':numeric_rank(M,tol),'tests':tests,'matrix':M}
```

## `graph_depth.py`
```python
from collections import deque
from math import ceil
def all_pairs_shortest_paths(adj):
 D={}
 for s in adj:
  dist={s:0};q=deque([s])
  while q:
   u=q.popleft()
   for v in adj[u]:
    if v not in dist:dist[v]=dist[u]+1;q.append(v)
  if len(dist)!=len(adj):raise ValueError('DISCONNECTED_GRAPH')
  D[s]=dist
 return D
def diameter(adj):return max(max(row.values()) for row in all_pairs_shortest_paths(adj).values())
def locality_lower_bound(adj,radius):
 if radius<=0:raise ValueError('radius<=0')
 return ceil(diameter(adj)/radius)
def source_target_lower_bound(adj,source,target,radius):return ceil(all_pairs_shortest_paths(adj)[source][target]/radius)
```

## `kblock_feasibility.py`
```python
from .branch_bound import search_partition
def finite_kblock_feasibility(P,labels,k,epsilon=0.0,node_budget=100000):
 out=search_partition(P,labels,epsilon,node_budget)
 if out.get('status')!='FOUND':return {'verdict':'INCONCLUSIVE','backend':'BOUNDED_COMBINATORIAL','details':out}
 if out['state_count']<=k:return {'verdict':'FEASIBLE_AT_MOST_K','k':k,'witness':out,'backend':'BOUNDED_COMBINATORIAL'}
 return {'verdict':'NO_WITNESS_WITHIN_SEARCH','k':k,'best':out,'backend':'BOUNDED_COMBINATORIAL'}
```

## `models.py`
```python
from dataclasses import dataclass,field,asdict
from typing import Any,Literal
Verdict=Literal['NO_PROMOTION','NO_FINITE_STATE','EXACT','APPROXIMATE','RESOURCE_ONLY','INCONCLUSIVE','HOLD','PASS','FAIL']
@dataclass(frozen=True)
class ContextContract:
 context_id:str;kind:str;description:str;required_exact:bool=True;tolerance:float=0.0
@dataclass
class PromotionProblem:
 problem_id:str;micro_states:list[Any];contexts:list[ContextContract];tolerance:float=0.0;admissibility:dict[str,Any]=field(default_factory=dict);metadata:dict[str,Any]=field(default_factory=dict)
@dataclass
class CandidateRepresentation:
 candidate_id:str;blocks:list[list[int]];description:str='';generator:Any|None=None;metadata:dict[str,Any]=field(default_factory=dict)
@dataclass
class GateResult:
 gate:str;passed:bool;metric:float|None=None;threshold:float|None=None;reason:str='';evidence:dict[str,Any]=field(default_factory=dict)
@dataclass
class PromotionDecision:
 verdict:Verdict;candidate_id:str|None;gates:list[GateResult];semantic_state_count:int|None=None;notes:list[str]=field(default_factory=list)
 def to_dict(self):return {'verdict':self.verdict,'candidate_id':self.candidate_id,'semantic_state_count':self.semantic_state_count,'gates':[asdict(g) for g in self.gates],'notes':list(self.notes)}
@dataclass
class EvidenceRecord:
 evidence_id:str;claim_id:str;evidence_class:str;source_ref:str;supports:bool;payload:dict[str,Any];cannot_prove:list[str]=field(default_factory=list)
@dataclass
class ImprovementProposal:
 proposal_id:str;parent_revision:str;hypothesis:str;mutation_scope:list[str];target_metrics:dict[str,float];forbidden_mutations:list[str];benchmark_ids:list[str];rollback_ref:str;status:str='PROPOSED';metadata:dict[str,Any]=field(default_factory=dict)
```

## `phase_boundary.py`
```python
from .partition import all_partitions,output_consistent,markov_lumpability_defect,canonical
def finite_phase_boundaries(P,labels):
 candidates=[]
 for p in all_partitions(len(P)):
  if output_consistent(p,labels):candidates.append({'blocks':[list(x) for x in canonical(p)],'state_count':len(p),'defect':markov_lumpability_defect(P,p)})
 epsilons=sorted({round(c['defect'],15) for c in candidates});segments=[]
 for eps in epsilons:
  feasible=[c for c in candidates if c['defect']<=eps+1e-12];best=min(feasible,key=lambda c:(c['state_count'],c['defect'],c['blocks']))
  if not segments or best['state_count']!=segments[-1]['state_count']:segments.append({'epsilon':eps,'state_count':best['state_count'],'witness':best['blocks']})
 return {'breakpoints':segments,'all_defect_values':epsilons,'candidate_count':len(candidates)}
```

## `refinement.py`
```python
from collections import defaultdict
def _initial_blocks(labels):
 g=defaultdict(list)
 for i,l in enumerate(labels):g[l].append(i)
 return [sorted(v) for _,v in sorted(g.items(),key=lambda kv:str(kv[0]))]
def exact_markov_refinement(P,labels,tol=1e-12,max_rounds=100):
 blocks=_initial_blocks(labels);rounds=0
 while rounds<max_rounds:
  rounds+=1;new=[];changed=False
  for block in blocks:
   groups=[];signatures=[]
   for s in block:
    sig=tuple(round(sum(P[s][j] for j in target)/tol)*tol if tol>0 else sum(P[s][j] for j in target) for target in blocks);found=None
    for k,ss in enumerate(signatures):
     if max(abs(a-b) for a,b in zip(sig,ss))<=tol:found=k;break
    if found is None:signatures.append(sig);groups.append([s])
    else:groups[found].append(s)
   changed|=len(groups)>1;new.extend(groups)
  blocks=[sorted(b) for b in new]
  if not changed:return {'blocks':blocks,'state_count':len(blocks),'rounds':rounds,'converged':True}
 return {'blocks':blocks,'state_count':len(blocks),'rounds':rounds,'converged':False}
```

## `self_improvement.py`
```python
from dataclasses import asdict
from .models import ImprovementProposal
class ImprovementArchive:
 def __init__(self):self.nodes={}
 def add(self,proposal,parent_id=None,metrics=None,verdict='HOLD'):
  if proposal.proposal_id in self.nodes:raise ValueError('DUPLICATE_PROPOSAL_ID')
  self.nodes[proposal.proposal_id]={'proposal':asdict(proposal),'parent_id':parent_id,'metrics':dict(metrics or {}),'verdict':verdict,'children':[]}
  if parent_id:
   if parent_id not in self.nodes:raise ValueError('UNKNOWN_PARENT')
   self.nodes[parent_id]['children'].append(proposal.proposal_id)
def promotion_gate(*,baseline,candidate,regression_floor=0.0,min_primary_gain=0.0):
 primary_gain=candidate.get('primary',0)-baseline.get('primary',0);regression=min((candidate.get(k,0)-baseline.get(k,0) for k in baseline if k!='primary'),default=0.0);passed=primary_gain>=min_primary_gain and regression>=-regression_floor;return {'passed':passed,'primary_gain':primary_gain,'worst_regression':regression,'reason':'PASS' if passed else 'HOLD_OR_REJECT'}
def lineage_potential(node,archive,depth=2):
 seen=set();frontier=[(node,0)];vals=[]
 while frontier:
  nid,d=frontier.pop()
  if nid in seen or nid not in archive.nodes or d>depth:continue
  seen.add(nid);n=archive.nodes[nid]
  if n['metrics']:vals.append(n['metrics'].get('primary',0.0))
  for c in n['children']:frontier.append((c,d+1))
 return sum(vals)/len(vals) if vals else 0.0
def parent_priority(node_id,archive,novelty=0.0,descendant_weight=.25,novelty_weight=.15):return archive.nodes[node_id]['metrics'].get('primary',0.0)+descendant_weight*lineage_potential(node_id,archive)+novelty_weight*novelty
```

## `stochastic_bounds.py`
```python
from .metrics import row_tv_operator
def dobrushin(P):return .5*max(sum(abs(P[i][k]-P[j][k]) for k in range(len(P[0]))) for i in range(len(P)) for j in range(len(P)))
def recursive_tv_bound(true_P,approx_P,t):
 delta=row_tv_operator(true_P,approx_P);alpha=dobrushin(true_P)
 if alpha>=1:return {'status':'NONCONTRACTIVE','alpha':alpha,'delta':delta,'linear_bound':min(1.0,t*delta)}
 bound=delta*(1-alpha**t)/(1-alpha);return {'status':'CONTRACTIVE','alpha':alpha,'delta':delta,'bound':min(1.0,bound)}
```
