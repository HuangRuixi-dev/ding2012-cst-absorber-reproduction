import sys,json,time,traceback,os
from pathlib import Path
sys.path.insert(0,str(Path(os.environ.get('CST_INSTALL_DIR',r'E:\CST Studio Suite 2023'))/'AMD64'/'python_cst_libraries'))
import cst.interface
root=Path(__file__).resolve().parent
run=Path(os.environ.get('CST_REPRO_RUN',str(root/'tasks/ding2012/runs/run_001')))
project=run/'projects/Ding2012_20layer.cst'
def log(event,**kw):
 d=dict(time=time.strftime('%Y-%m-%d %H:%M:%S'),event=event,**kw)
 print(json.dumps(d),flush=True)
 with (run/'logs/solver.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(d)+'\n')
de=cst.interface.DesignEnvironment.new();log('connected',pid=de.pid())
p=de.open_project(str(project));log('opened')
try:
 p.modeler.start_solver(timeout=300);log('started')
 while p.modeler.is_solver_running(timeout=60):
  (run/'logs/progress.json').write_text(json.dumps(dict(time=time.strftime('%Y-%m-%d %H:%M:%S'),messages=str(p.get_messages()),info=p.modeler.get_solver_run_info()),default=str),encoding='utf-8')
  time.sleep(15)
 log('finished',info=p.modeler.get_solver_run_info(),messages=str(p.get_messages()))
 p.save()
 (run/'exports/tree.json').write_text(json.dumps(p.modeler.get_tree_items(),indent=2),encoding='utf-8')
 p.close();de.close();log('closed')
except Exception:
 log('error',traceback=traceback.format_exc())
 raise
