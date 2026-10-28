from pathlib import Path
import json,sys
import cst.results
R=Path(__file__).resolve().parents[1]
for name in sys.argv[1:]:
 c=R/'runs'/name
 pf=cst.results.ProjectFile(str(c/'absorber.cst'))
 res=pf.get_3d();tree=res.get_tree_items();raw={}
 for path in tree:
  if path.startswith('1D Results\\S-Parameters\\'):
   ids=res.get_run_ids(path); item=res.get_result_item(path,run_id=ids[-1]);y=[complex(v) for v in item.get_ydata()]
   raw[path]={'frequency_GHz':list(item.get_xdata()),'real':[v.real for v in y],'imag':[v.imag for v in y],'run_id':ids[-1]}
 if not raw:raise RuntimeError('No S parameters in '+name)
 (c/'sparameters.json').write_text(json.dumps(raw),encoding='utf-8')
 print(name,len(raw),'channels exported')
