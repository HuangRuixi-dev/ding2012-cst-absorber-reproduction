from pathlib import Path
import json,re,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];c=R/'runs/C06_loss12_meshcheck'
raw=json.loads((c/'sparameters.json').read_text())
f=np.asarray(next(iter(raw.values()))['frequency_GHz']);ref=[];tra=[];co=None
for name,vals in raw.items():
 out,inc=re.findall(r'Z(?:max|min)\(\d+\)',name)
 assert inc=='Zmax(1)'
 s=np.asarray(vals['real'])+1j*np.asarray(vals['imag'])
 assert np.array_equal(f,np.asarray(vals['frequency_GHz']))
 if out.startswith('Zmax'):ref.append(abs(s)**2)
 else:tra.append(abs(s)**2)
 if out=='Zmax(1)':co=s
A=1-np.sum(ref,axis=0)-np.sum(tra,axis=0)
csv=np.loadtxt(c/'spectrum.csv',delimiter=',',skiprows=1)
assert len(csv)==len(f) and np.array_equal(f,csv[:,0])
above=np.flatnonzero(A>.9);splits=np.where(np.diff(above)>1)[0]+1
segments=np.split(above,splits);bands=[]
for seg in segments:
 if len(seg)==0:continue
 i,j=int(seg[0]),int(seg[-1]);lo=float(f[i]);hi=float(f[j])
 if i>0:lo=float(f[i-1]+(.9-A[i-1])/(A[i]-A[i-1])*(f[i]-f[i-1]))
 if j<len(f)-1:hi=float(f[j]+(.9-A[j])/(A[j+1]-A[j])*(f[j+1]-f[j]))
 bands.append({'lower_GHz':lo,'upper_GHz':hi,'RAB_percent':200*(hi-lo)/(hi+lo),'upper_is_scan_limit':j==len(f)-1})
mask=(f>=7.3)&(f<=26);gg=np.r_[7.3,f[mask & (f>7.3) & (f<26)],26];aa=np.interp(gg,f,A)
modelparams=json.loads((c/'absorber/Model/Parameters.json').read_text())
manifest=json.loads((R/'data/manifest.json').read_text(encoding='utf-8'))
hashes={k:hashlib.sha256((R/k).read_bytes()).hexdigest()==v for k,v in manifest['deliverables'].items()}
out={'native_channel_count':len(raw),'points':len(f),'scan_GHz':[float(f[0]),float(f[-1])],'spectrum_csv_absorption_difference':float(np.max(abs(csv[:,1]-A))),'continuous_A_above_90_percent':bands,'conservative_7p3_26_GHz':{'minimum_A':float(aa.min()),'frequency_average_A':float(np.trapezoid(aa,gg)/(26-7.3)),'max_copolar_S11_dB':float((20*np.log10(abs(co[mask]))).max()),'RAB_percent':200*(26-7.3)/(26+7.3)},'A_at_5GHz':float(A[0]),'first_air_diffraction_GHz':299.792458/11,'model_parameters':modelparams,'deliverable_hash_matches':hashes,'A_bounds':[float(A.min()),float(A.max())]}
(R/'audit').mkdir(exist_ok=True);(R/'audit/independent_metrics.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(out,indent=2,ensure_ascii=False))
