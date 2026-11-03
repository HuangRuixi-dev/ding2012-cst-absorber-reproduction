from pathlib import Path
import json,re
import cst.results
D=Path(r'C:\Users\huzst\Desktop\senior\metamaterial\ding2012-cst-absorber-reproduction-main\course_design_absorber\pyramid_optimization_5_40GHz/P06_critical_stability_screen');r=cst.results.ProjectFile(str(D/'absorber.cst')).get_3d();pre='1D Results\\Adaptive Meshing\\f=12.23\\';raw={};cells=None;delta=None
for k in r.get_tree_items():
 if not k.startswith(pre):continue
 it=r.get_result_item(k,run_id=r.get_run_ids(k)[-1]);yy=it.get_ydata();yy=[yy] if isinstance(yy,(int,float,complex)) else list(yy)
 if k.lower().endswith('meshcells'):cells=[int(v) for v in yy]
 if k.endswith('Delta\\All S-Parameters'):delta=[float(v) for v in yy]
 if '\\S-Parameters\\SZ' in k:
  raw[k]=dict(passes=list(it.get_xdata()),real=[complex(z).real for z in yy],imag=[complex(z).imag for z in yy])
n=min(len(v['real']) for v in raw.values());A=[1.]*n;R0=[0.]*n
for k,v in raw.items():
 ix=int(re.findall(r'Z(?:max|min)\((\d+)\)',k)[0])
 if ix>2:continue
 for j in range(n):
  pp=abs(complex(v['real'][j],v['imag'][j]))**2;A[j]-=pp
  if 'SZmax(1)' in k:R0[j]=pp
out=dict(frequency_GHz=12.23,A_by_pass=A,mesh_cells_by_pass=cells,delta_S=delta,mode_count=50,scope='independent adaptive mesh convergence at same physical frequency')
assert abs(A[-1]-json.loads((D/'metrics.json').read_text())['min_A'])<1e-6
(D/'adaptive_stability.json').write_text(json.dumps(out,indent=2));(D/'adaptive_complex.json').write_text(json.dumps(raw));print(json.dumps(out,indent=2))
