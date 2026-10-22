import sys, os, json, traceback
from pathlib import Path
sys.path.insert(0, str(Path(os.environ.get('CST_INSTALL_DIR', r'E:\CST Studio Suite 2023')) / 'AMD64' / 'python_cst_libraries'))
import cst.interface, cst.results

root = Path(__file__).resolve().parent
run = Path(os.environ['CST_REPRO_RUN'])
project = run/'projects'/'Ding2012_20layer.cst'
out = run/'exports'; out.mkdir(parents=True, exist_ok=True)

def field_max(path):
    maximum = 0.0
    with path.open(errors='replace') as source:
        next(source); next(source)
        for line in source:
            parts = line.split()
            if len(parts) >= 9:
                maximum = max(maximum, *(abs(float(v)) for v in parts[3:9]))
    return maximum

rf = cst.results.ProjectFile(str(project)).get_3d()
sparams = {}
for name in rf.get_tree_items():
    if not name.startswith('1D Results\\S-Parameters\\'):
        continue
    v = rf.get_result_item(name)
    y = [complex(x) for x in v.get_ydata()]
    sparams[name] = {'frequency_GHz': list(v.get_xdata()), 'real': [x.real for x in y], 'imag': [x.imag for x in y]}
(out/'sparameters.json').write_text(json.dumps(sparams),encoding='utf-8')
del rf

de = cst.interface.DesignEnvironment.new()
project_ui = de.open_project(str(project))
try:
    tree = project_ui.modeler.get_tree_items()
    (out/'tree_full.json').write_text(json.dumps(tree, indent=2),encoding='utf-8')
    for typ in 'EH':
        for freq in ('8.3','10','12','14'):
            name = '2D/3D Results\\{}-Field\\{}_{} [Zmax(1)]'.format(typ,typ,freq)
            if name not in tree: raise RuntimeError('Missing field result '+name)
            target = out/'{}_{}_x0.txt'.format(typ,freq)
            vba = '''Sub Main
SelectTreeItem "{name}"
With ASCIIExport
.Reset
.FileName "{path}"
.Mode "FixedNumber"
.UseSubvolume "True"
.SetSubvolume "0", "0.000001", "-5.5", "5.5", "0.001", "5.5"
.StepX "2"
.StepY "221"
.StepZ "221"
.Execute
End With
End Sub'''.format(name=name,path=str(target))
            print('EXPORTING',name,flush=True)
            project_ui.schematic.execute_vba_code(vba,timeout=600)
            mx = field_max(target)
            print('EXPORTED',str(target),target.stat().st_size,'MAX',mx,flush=True)
            if mx <= 0: raise RuntimeError('Zero-valued field: '+name)
    project_ui.close(); de.close()
    print('EXPORT_COMPLETE',flush=True)
except Exception:
    print(traceback.format_exc(),flush=True)
    try: project_ui.close(); de.close()
    except Exception: pass
    raise
