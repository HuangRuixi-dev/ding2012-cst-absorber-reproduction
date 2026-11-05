from pathlib import Path
import os
import json,re,csv,sys
import numpy as np
ROOT=Path(os.environ.get('CST_ABSORBER_RUN', str(Path(__file__).resolve().parents[1]/'cases')))
def getbands(f,A):
 sw=np.diff(np.r_[False,A>.9,False].astype(int));out=[]
 for i,j in zip(np.where(sw==1)[0],np.where(sw==-1)[0]-1):
  lo=f[i] if i==0 else f[i-1]+(.9-A[i-1])*(f[i]-f[i-1])/(A[i]-A[i-1])
  hi=f[j] if j==len(f)-1 else f[j]+(.9-A[j])*(f[j+1]-f[j])/(A[j+1]-A[j])
  out.append(dict(lower_GHz=float(lo),upper_GHz=float(hi),RAB_percent=float(200*(hi-lo)/(hi+lo)),lower_censored=bool(i==0),upper_censored=bool(j==len(f)-1)))
 return out
for name in sys.argv[1:]:
 D=ROOT/name;cutoffs=json.loads((D/'port_cutoffs.json').read_text()) if (D/'port_cutoffs.json').exists() else {};cfg=json.loads((D/'parameters.json').read_text());raw=json.loads((D/'sparameters.json').read_text());f=np.array(next(iter(raw.values()))['frequency_GHz']);R=np.zeros_like(f);T=R.copy();R0=R.copy();cross=R.copy();higher=R.copy();s11=None;seen=[]
 for key,v in raw.items():
  tokens=re.findall(r'Z(?:max|min)\((\d+)\)',key)
  if tokens[-1]!='1':continue
  dest=int(tokens[0]);mo=cfg['modes'][dest-1];fc=mo['cutoff_GHz'];port='Zmax' if 'SZmax' in key else 'Zmin'
  assert abs(cutoffs.get(port+'(%d)'%dest,fc)-fc)<1e-6,'Native cutoff differs from declared custom mode mapping'
  z=np.array(v['real'])+1j*np.array(v['imag']);power=abs(z)**2
  assert np.allclose(f,np.asarray(v['frequency_GHz']),rtol=0,atol=1e-10)
  # Custom mode list is inserted in the exact order in parameters.json. Only
  # propagating air Floquet modes transport real power. Exclude at cutoff.
  prop=f>fc+1e-8;pw=np.where(prop,power,0.)
  if 'SZmax' in key:
   R+=pw
   if dest==1:s11=z;R0=pw
   elif dest==2:cross=pw
   else:higher+=pw
  else:T+=pw
  seen.append((port,dest))
 assert s11 is not None
 assert set(seen)==set((port,i) for port in ['Zmax','Zmin'] for i in range(1,cfg['mode_count']+1)),'Incomplete outgoing mode dataset'
 A=1-R-T;sdb=20*np.log10(np.maximum(abs(s11),1e-150))
 screen=cfg.get('screening',False)
 if screen:
  ix=[int(np.argmin(abs(f-fj))) for fj in cfg['screening_frequencies_GHz']]
  assert all(abs(f[i]-fj)<1e-7 for i,fj in zip(ix,cfg['screening_frequencies_GHz']))
  f,A,R,T,R0,cross,higher,sdb=[arr[ix] for arr in [f,A,R,T,R0,cross,higher,sdb]]
 bands=[] if screen else getbands(f,A);best=max(bands,key=lambda x:x['RAB_percent']) if bands else None
 np.savetxt(D/'spectrum.csv',np.c_[f,A,R,T,R0,cross,higher,sdb],delimiter=',',header='frequency_GHz,A,R,T,R_copolar,R_cross,R_higher,S11_dB',comments='')
 log=(D/'absorber/Result/output.txt').read_text(errors='replace');mlog=(D/'absorber/Result/Model.log').read_text(errors='replace');mc=re.findall(r'Number of mesh cells\s*:\s*(\d+)',mlog);delta=re.findall(r'All S-Parameters\s*=\s*([0-9.eE+-]+)',log)
 m=dict(name=name,screening=screen,mode_count=cfg['mode_count'],first_diffraction_GHz=299.792458/cfg['P'],samples=len(f),min_A=float(A.min()),min_A_frequency_GHz=float(f[A.argmin()]),max_copolar_S11_dB=float(sdb.max()),max_higher_reflection=float(higher.max()),max_T=float(T.max()),bands=bands,best=best,screening_points_pass=bool(np.all(A>.9) and np.all(sdb<-10)),full_5_40_pass=None if screen else bool(np.all(A>.9) and np.all(sdb<-10) and f[0]<=5 and f[-1]>=40),power_sanity=bool(A.min()>-.01 and A.max()<1.01),mesh_converged='Mesh adaptation terminated because the desired accuracy limit is reached' in log,broadband_converged='All broadband sweep convergence criteria have been satisfied' in log,mesh_cells=int(mc[-1]) if mc else None,last_delta_S=float(delta[-1]) if delta else None,solver_errors=re.findall(r'\*\*\* Error \*\*\*',mlog),warning_count=log.count('WARNING:'),at_5=[float(A[np.argmin(abs(f-5))]),float(sdb[np.argmin(abs(f-5))])] if np.min(abs(f-5))<1e-7 else None,at_40=[float(A[np.argmin(abs(f-40))]),float(sdb[np.argmin(abs(f-40))])] if np.min(abs(f-40))<1e-7 else None)
 (D/'metrics.json').write_text(json.dumps(m,indent=2),encoding='utf-8');print(json.dumps(m,indent=2),flush=True)
