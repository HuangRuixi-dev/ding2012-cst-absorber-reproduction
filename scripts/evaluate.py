from pathlib import Path
import json,re,csv
import numpy as np
R=Path(__file__).resolve().parents[1]
def bands(x,a,threshold=.9):
 e=np.diff(np.r_[False,a>threshold,False].astype(int));out=[]
 for lo,hi in zip(np.where(e==1)[0],np.where(e==-1)[0]-1):
  l=x[lo] if lo==0 else x[lo-1]+(threshold-a[lo-1])*(x[lo]-x[lo-1])/(a[lo]-a[lo-1])
  u=x[hi] if hi==len(x)-1 else x[hi]+(threshold-a[hi])*(x[hi+1]-x[hi])/(a[hi+1]-a[hi])
  out.append({'lower_GHz':float(l),'upper_GHz':float(u),'width_GHz':float(u-l),'RAB_percent':float(200*(u-l)/(u+l)),'right_censored':bool(hi==len(x)-1),'left_censored':bool(lo==0)})
 return out
summary=[]
for c in sorted((R/'runs').iterdir()):
 if not (c/'sparameters.json').exists():continue
 raw=json.loads((c/'sparameters.json').read_text());sel={k:v for k,v in raw.items() if re.findall(r'Z(?:max|min)\(\d+\)',k)[-1]=='Zmax(1)'}
 f=np.array(next(iter(sel.values()))['frequency_GHz']);r=np.zeros_like(f);t=r.copy();cross=r.copy();s11=None
 for k,v in sel.items():
  assert np.allclose(np.asarray(v['frequency_GHz']),f,atol=1e-12,rtol=0), 'Channel frequency grids differ'
  a=np.array(v['real'])+1j*np.array(v['imag']);power=abs(a)**2;rx=re.findall(r'Z(?:max|min)\(\d+\)',k)[0]
  if rx.startswith('Zmax'):
   r+=power
   if rx=='Zmax(1)':s11=a
   else:cross+=power
  else:t+=power
 A=1-r-t; bb=bands(f,A);best=max(bb,key=lambda b:b['RAB_percent']) if bb else None
 assert np.all(np.diff(f)>0)
 assert np.all(A>=-.01) and np.all(A<=1.01), 'Non-passive power spectrum; inspect port normalization'
 np.savetxt(c/'spectrum.csv',np.c_[f,A,r,t,cross,20*np.log10(np.maximum(abs(s11),1e-150)),s11.real,s11.imag],delimiter=',',header='frequency_GHz,A,R,T,cross_reflection,S11_dB,S11_real,S11_imag',comments='')
 logpath=c/'absorber/Result/Model.log';log=logpath.read_text(errors='replace') if logpath.exists() else ''
 last=lambda p:re.findall(p,log)[-1] if re.findall(p,log) else None
 params=json.loads((c/'parameters.json').read_text())
 execution=json.loads((c/'execution.json').read_text())
 converged='All broadband sweep' in log and 'convergence criteria have been satisfied' in log
 errors=re.findall(r'\*\*\* Error \*\*\*',log)
 m={'case':c.name,'parameters':params,'bands':bb,'best':best,'passes_spec':bool(best and best['RAB_percent']>100 and converged and not errors and execution['exit_code']==0),'exit_code':execution['exit_code'],'broadband_converged':converged,'A_range':[float(A.min()),float(A.max())],'max_cross_reflection':float(cross.max()),'max_T':float(t.max()),'samples':len(f),'mesh_cells':last(r'Number of mesh cells\s*:\s*(\d+)'),'last_mesh_delta':last(r'All S-Parameters\s*:\s*([0-9.eE+-]+)'),'solver_errors':errors,'warning_count':log.count('*** Warning ***')}
 (c/'metrics.json').write_text(json.dumps(m,indent=2))
 summary.append(m)
(R/'data/summary.json').write_text(json.dumps(summary,indent=2))
with (R/'data/optimization_summary.csv').open('w',newline='',encoding='utf-8-sig') as out:
 writer=csv.writer(out);writer.writerow(['case','layers','height_mm','loss_tangent','lower_GHz','upper_GHz','RAB_percent','upper_is_scan_limit','passes_spec','mesh_cells','mesh_delta','broadband_converged'])
 for m in summary:
  b=m['best'] or {};p=m['parameters']
  writer.writerow([m['case'],p['layers'],p['height'],p['loss'],b.get('lower_GHz'),b.get('upper_GHz'),b.get('RAB_percent'),b.get('right_censored'),m['passes_spec'],m['mesh_cells'],m['last_mesh_delta'],m['broadband_converged']])
for m in summary:print(m['case'],m['best'],'PASS' if m['passes_spec'] else 'FAIL')
