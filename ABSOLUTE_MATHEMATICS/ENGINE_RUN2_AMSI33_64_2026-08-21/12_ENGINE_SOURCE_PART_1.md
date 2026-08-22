# ENGINE SOURCE PART 1/4 — RUN2

## `__init__.py`

```python
from .models import *
from .pipeline import run_finite_markov
```

## `benchmarks.py`

```python
from __future__ import annotations
DEFAULT_BENCHMARKS=[
 {"id":"B01_POINT_SEPARATING_NO_GO","domain":"finite_context","expected":"NO_PROMOTION"},
 {"id":"B02_EXACT_LUMPABLE","domain":"markov","expected":"EXACT"},
 {"id":"B03_PERTURBED_LUMPABLE","domain":"markov","expected":"TOLERANCE_TRANSITION"},
 {"id":"B04_NONCONTRACTIVE_SMALL_ERROR","domain":"markov","expected":"LONG_HORIZON_FAIL"},
 {"id":"B05_HISTORY_CMI","domain":"symbolic","expected":"MISSING_HISTORY_DETECTED"},
 {"id":"B06_MICRO_CMI","domain":"symbolic","expected":"MISSING_MICRO_DETECTED"},
 {"id":"B07_NONREGULAR_GROWTH","domain":"language","expected":"NO_FINITE_STATE"},
 {"id":"B08_FLATTENABLE_HIERARCHY","domain":"construction","expected":"REJECT_INTRINSIC_DEPTH"},]
def registry(): return list(DEFAULT_BENCHMARKS)
```

## `closure.py`

```python
from __future__ import annotations
def total_variation(p,q): return 0.5*sum(abs(a-b) for a,b in zip(p,q))
def matvec(v,P): return [sum(v[i]*P[i][j] for i in range(len(v))) for j in range(len(P[0]))]
def dobrushin(P): return 0.5*max(sum(abs(P[i][k]-P[j][k]) for k in range(len(P[0]))) for i in range(len(P)) for j in range(len(P)))
def rollout_error(initial,true_P,approx_P,horizons=(1,2,4,8,16)):
 t=max(horizons); a=list(initial); b=list(initial); out={}
 for step in range(1,t+1):
  a=matvec(a,true_P); b=matvec(b,approx_P)
  if step in horizons: out[step]=total_variation(a,b)
 return out
def contractive_bound(epsilon,alpha,t):
 if alpha<0 or alpha>1: raise ValueError('alpha must be in [0,1]')
 if alpha==1: return epsilon*t
 return epsilon*(1-alpha**t)/(1-alpha)
def closure_contract(one_step_defect,metric,normalization,horizon,stability):
 return {'one_step_defect':float(one_step_defect),'metric':metric,'normalization':normalization,'validated_horizon':int(horizon),'stability':stability}
```

## `construction.py`

```python
from __future__ import annotations
from math import ceil,log
def locality_depth(distance,radius):
 if radius<=0: raise ValueError('radius must be >0')
 return ceil(distance/radius)
def arity_depth(n_inputs,arity):
 if n_inputs<=1:return 0
 if arity<2:raise ValueError('arity must be >=2')
 return ceil(log(n_inputs,arity))
def spectrum(*,n_inputs,distance,radius,arity,communication_bits=None,memory_bits=None,time_cost=None):
 return {'locality_depth_lb':locality_depth(distance,radius),'arity_depth_lb':arity_depth(n_inputs,arity),'combined_depth_lb':max(locality_depth(distance,radius),arity_depth(n_inputs,arity)),'communication_bits':communication_bits,'memory_bits':memory_bits,'time_cost':time_cost}
def pareto_dominates(a,b,keys): return all(a[k]<=b[k] for k in keys) and any(a[k]<b[k] for k in keys)
```

## `continuous_cmi.py`

```python
from __future__ import annotations
from math import log,sqrt
from .information import conditional_mutual_information
def _mean(x): return sum(x)/len(x)
def _cov(x,y):
 mx,my=_mean(x),_mean(y); return sum((a-mx)*(b-my) for a,b in zip(x,y))/len(x)
def _corr(x,y):
 vx=_cov(x,x);vy=_cov(y,y)
 if vx<=0 or vy<=0:return 0.0
 return _cov(x,y)/sqrt(vx*vy)
def gaussian_cmi_scalar(x,y,z):
 rxy=_corr(x,y);rxz=_corr(x,z);ryz=_corr(y,z);den=sqrt(max(1e-15,(1-rxz*rxz)*(1-ryz*ryz)));r=(rxy-rxz*ryz)/den;r=max(-.999999999,min(.999999999,r));return -0.5*log(max(1e-15,1-r*r))/log(2)
def discretize(xs,bins=8):
 lo=min(xs);hi=max(xs)
 if hi==lo:return [0]*len(xs)
 return [min(bins-1,int((x-lo)/(hi-lo)*bins)) for x in xs]
def benchmark_two_estimators(x,y,z,bins=8):
 return {'gaussian_cmi_bits':gaussian_cmi_scalar(x,y,z),'discrete_binned_cmi_bits':conditional_mutual_information(discretize(x,bins),discretize(y,bins),discretize(z,bins)),'status':'PARTIAL_TWO_ESTIMATORS_ONLY','missing':['kNN_CMI','neural_CMI']}
```

## `experiments.py`

```python
from __future__ import annotations
import hashlib,json,time
class ExperimentRegistry:
 def __init__(self):self.items={}
 def preregister(self,experiment_id,hypothesis,metrics,thresholds,fixtures,allowed_followups=None):
  if experiment_id in self.items:raise ValueError('DUPLICATE_EXPERIMENT_ID')
  payload={'experiment_id':experiment_id,'hypothesis':hypothesis,'metrics':metrics,'thresholds':thresholds,'fixtures':fixtures,'allowed_followups':list(allowed_followups or []),'status':'PREREGISTERED','created_at':time.time()};payload['prereg_hash']=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':')).encode()).hexdigest();self.items[experiment_id]=payload;return payload
 def record(self,experiment_id,results,deviations=None):
  item=self.items[experiment_id];item['results']=results;item['deviations']=list(deviations or []);item['status']='COMPLETED';return item
```

## `information.py`

```python
from __future__ import annotations
from collections import Counter
from math import log2
def entropy(xs):
 xs=list(xs);n=len(xs)
 if n==0:return 0.0
 c=Counter(xs);return -sum((v/n)*log2(v/n) for v in c.values())
def mutual_information(x,y):return entropy(x)+entropy(y)-entropy(zip(x,y))
def conditional_mutual_information(x,y,z):return entropy(zip(x,z))+entropy(zip(y,z))-entropy(z)-entropy(zip(x,y,z))
def sufficiency_gate(future,omitted,state,threshold_bits=0.01,gate_name='CONDITIONAL_INFORMATION'):
 value=conditional_mutual_information(future,omitted,state);return {'gate':gate_name,'passed':value<=threshold_bits,'metric_bits':value,'threshold_bits':threshold_bits}
```

## `metrics.py`

```python
from __future__ import annotations
from math import log,sqrt
def total_variation(p,q):return 0.5*sum(abs(a-b) for a,b in zip(p,q))
def kl_divergence(p,q):
 out=0.0
 for a,b in zip(p,q):
  if a>0:
   if b<=0:return float('inf')
   out+=a*log(a/b)
 return out
def js_divergence(p,q):
 m=[.5*(a+b) for a,b in zip(p,q)];return .5*kl_divergence(p,m)+.5*kl_divergence(q,m)
def rmse(x,y):
 if len(x)!=len(y) or not x:raise ValueError('BAD_LENGTH')
 return sqrt(sum((a-b)**2 for a,b in zip(x,y))/len(x))
def normalized_rmse(x,y,scale=None):
 r=rmse(x,y)
 if scale is None:
  mean=sum(x)/len(x);scale=sqrt(sum((a-mean)**2 for a in x)/len(x))
 if scale<=0:raise ValueError('ZERO_SCALE')
 return r/scale
def wasserstein_1d(x,y):
 if len(x)!=len(y) or not x:raise ValueError('EQUAL_NONEMPTY_SAMPLES_REQUIRED')
 a=sorted(x);b=sorted(y);return sum(abs(u-v) for u,v in zip(a,b))/len(a)
def row_tv_operator(P,Q):return max(total_variation(a,b) for a,b in zip(P,Q))
METRIC_REGISTRY={'TV':{'domain':'probability simplex','unit_invariant':True},'KL':{'domain':'probability simplex','unit_invariant':True},'JS':{'domain':'probability simplex','unit_invariant':True},'NRMSE':{'domain':'numeric observations','scalar_rescale_invariant_if_scale_covaries':True},'WASSERSTEIN_1D':{'domain':'metric numeric observations','requires_geometry':True},'ROW_TV_OPERATOR':{'domain':'Markov kernels','unit_invariant':True}}
def metric_contract(name,normalization=None,horizon=None):
 if name not in METRIC_REGISTRY:raise ValueError('UNKNOWN_METRIC')
 return {'name':name,'properties':METRIC_REGISTRY[name],'normalization':normalization,'horizon':horizon}
```

## `partition.py`

```python
from __future__ import annotations
def _parts(seq):
 seq=list(seq)
 if not seq:yield [];return
 first=seq[0]
 for rest in _parts(seq[1:]):
  yield [{first}]+[set(b) for b in rest]
  for i in range(len(rest)):
   out=[set(b) for b in rest];out[i].add(first);yield out
def canonical(part):return tuple(sorted(tuple(sorted(b)) for b in part))
def all_partitions(n):
 seen=set()
 for p in _parts(range(n)):
  c=canonical(p)
  if c not in seen:seen.add(c);yield [set(b) for b in c]
def output_consistent(part,labels):return all(len({labels[i] for i in block})==1 for block in part)
def markov_lumpability_defect(P,part):
 defect=0.0
 for block in part:
  for i in block:
   for j in block:
    for target in part:defect=max(defect,abs(sum(P[i][k] for k in target)-sum(P[j][k] for k in target)))
 return float(defect)
def learn_min_partition(P,labels,epsilon=0.0):
 candidates=[]
 for p in all_partitions(len(P)):
  if output_consistent(p,labels):
   d=markov_lumpability_defect(P,p)
   if d<=epsilon+1e-12:candidates.append((len(p),d,canonical(p)))
 if not candidates:return None
 candidates.sort(key=lambda x:(x[0],x[1],x[2]));k,d,c=candidates[0];return {'state_count':k,'defect':d,'blocks':[list(x) for x in c]}
```

## `recursive_update.py`

```python
def max_abs_diff(a,b):return max((abs(x-y) for x,y in zip(a,b)),default=0.0)
def recursive_consistency(model,actions,observations,atol=1e-12):
 online=list(model.initial);max_err=0.0;failures=[]
 for t,(a,o) in enumerate(zip(actions,observations),1):
  online=model.update(online,a,o);recomputed=model.history_filter(actions[:t],observations[:t])[-1];err=max_abs_diff(online,recomputed);max_err=max(max_err,err)
  if err>atol:failures.append({'t':t,'error':err})
 return {'passed':not failures,'max_error':max_err,'failures':failures,'atol':atol}
```

## `scalability.py`

```python
import time
from .partition import learn_min_partition
from .refinement import exact_markov_refinement
from .branch_bound import search_partition
def benchmark_solvers(P,labels,epsilon=0.0,run_exhaustive=True,node_budget=100000):
 out={}
 if run_exhaustive:
  t=time.perf_counter();a=learn_min_partition(P,labels,epsilon);out['exhaustive']={'seconds':time.perf_counter()-t,'result':a}
 t=time.perf_counter();b=exact_markov_refinement(P,labels);out['refinement']={'seconds':time.perf_counter()-t,'result':b,'applicability':'EXACT_ONLY'}
 t=time.perf_counter();c=search_partition(P,labels,epsilon,node_budget);out['branch_bound']={'seconds':time.perf_counter()-t,'result':c};return out
```

## `state_red_team.py`

```python
from itertools import product
def update_collision_witness(summary,alphabet=(0,1),max_history=5):
 histories=[]
 for L in range(1,max_history+1):histories.extend(product(alphabet,repeat=L))
 buckets={}
 for h in histories:buckets.setdefault(summary(h),[]).append(h)
 for z,hs in buckets.items():
  for i in range(len(hs)):
   for j in range(i+1,len(hs)):
    for a in alphabet:
     z1=summary(hs[i]+(a,));z2=summary(hs[j]+(a,))
     if z1!=z2:return {'recursive':False,'state':z,'h1':hs[i],'h2':hs[j],'append':a,'next1':z1,'next2':z2}
 return {'recursive':True,'reason':'NO_COLLISION_WITNESS_WITHIN_SEARCH'}
```
