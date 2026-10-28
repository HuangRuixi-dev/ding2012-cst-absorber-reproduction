from pathlib import Path
import json
import cst.results
R=Path(__file__).resolve().parents[1]
c=R/'runs/C06_loss12_meshcheck'
saved=json.loads((c/'sparameters.json').read_text())
pf=cst.results.ProjectFile(str(c/'absorber.cst'))
res=pf.get_3d()
out={}
for key in res.get_tree_items():
 if not key.startswith('1D Results\\S-Parameters\\'):continue
 ids=list(res.get_run_ids(key)); expected=saved[key]; run=expected['run_id']
 if run not in ids:raise RuntimeError('Saved run not present: '+key)
 item=res.get_result_item(key,run_id=run)
 f=list(item.get_xdata()); y=[complex(v) for v in item.get_ydata()]
 errf=max(abs(a-b) for a,b in zip(f,expected['frequency_GHz']))
 erry=max(abs(a-complex(b,d)) for a,b,d in zip(y,expected['real'],expected['imag']))
 out[key]={'run_ids':ids,'verified_run_id':run,'points':len(f),'frequency_range_GHz':[min(f),max(f)],'frequency_difference':errf,'complex_value_difference':erry,'same_length':len(f)==len(expected['frequency_GHz'])}
if set(out)!=set(saved):raise RuntimeError('Exported result tree differs from CST')
a=R/'audit';a.mkdir(exist_ok=True)
(a/'native_result_check.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
