from __future__ import print_function
import sys, os, json, time, traceback
from pathlib import Path
sys.path.insert(0, str(Path(os.environ.get('CST_INSTALL_DIR', r'E:\CST Studio Suite 2023')) / 'AMD64' / 'python_cst_libraries'))
import cst.interface
ROOT = Path(__file__).resolve().parent
RUN = Path(os.environ.get('CST_REPRO_RUN', str(ROOT / 'tasks' / 'ding2012' / 'runs' / 'run_001')))
for sub in ['projects','exports','logs','stages','analysis']:
    (RUN/sub).mkdir(parents=True, exist_ok=True)
PROJECT = RUN/'projects'/'Ding2012_20layer.cst'
def log(event, **kw):
    data=dict(time=time.strftime('%Y-%m-%d %H:%M:%S'),event=event,**kw)
    print(json.dumps(data),flush=True)
    with (RUN/'logs'/'execution.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(data)+'\n')
def block(obj, values):
    return 'With '+obj+'\n'+ '\n'.join('.'+k+' '+v for k,v in values)+'\nEnd With'
de=None
try:
    de=cst.interface.DesignEnvironment.new()
    log('connected',pid=de.pid())
    p=de.new_mws()
    def add(title,code):
        (RUN/'stages'/(title+'.vba')).write_text(code,encoding='utf-8')
        p.modeler.add_to_history(title,code,timeout=300)
        log('history',title=title)
    add('01_units', 'With Units\n.Geometry "mm"\n.Frequency "GHz"\n.Time "ns"\nEnd With\nSolver.FrequencyRange "6", "15"\nChangeSolverType "HF Frequency Domain"')
    add('02_materials',block('Material', [('Reset',''),('Name','"FR4_paper"'),('Type','"Normal"'),('Epsilon','"4.4"'),('Mue','"1"'),('TanD','"0.02"'),('TanDFreq','"10"'),('TanDGiven','"True"'),('TanDModel','"ConstTanD"'),('Colour','"0.5", "0.15", "0.3"'),('Create','')])+'\n'+block('Material',[('Reset',''),('Name','"Copper_paper"'),('Type','"Lossy metal"'),('Epsilon','"1"'),('Mue','"1"'),('Kappa','"5e7"'),('Colour','"1", "0.75", "0"'),('Create','')]))
    def brick(name,mat,w,z0,z1):
        return block('Brick',[('Reset',''),('Name','"'+name+'"'),('Component','"absorber"'),('Material','"'+mat+'"'),('Xrange','"{0}", "{1}"'.format(-w/2,w/2)),('Yrange','"{0}", "{1}"'.format(-w/2,w/2)),('Zrange','"{0}", "{1}"'.format(z0,z1)),('Create','')])
    code=brick('ground','Copper_paper',11,-0.05,0)
    for i in range(20):
        w=9.-4.*i/19.
        z=i*.25
        code+='\n'+brick('FR4_%02d'%i,'FR4_paper',w,z,z+.2)
        code+='\n'+brick('Cu_%02d'%i,'Copper_paper',w,z+.2,z+.25)
    add('03_geometry',code)
    add('04_boundaries',block('Background',[('Type','"Normal"'),('Epsilon','"1"'),('Mue','"1"'),('XminSpace','"0"'),('XmaxSpace','"0"'),('YminSpace','"0"'),('YmaxSpace','"0"'),('ZminSpace','"3"'),('ZmaxSpace','"8"')])+'\n'+block('Boundary',[('Xmin','"unit cell"'),('Xmax','"unit cell"'),('Ymin','"unit cell"'),('Ymax','"unit cell"'),('Zmin','"open"'),('Zmax','"open"'),('Xsymmetry','"none"'),('Ysymmetry','"none"'),('Zsymmetry','"none"'),('SetPeriodicBoundaryAngles','"0", "0"'),('UnitCellFitToBoundingBox','"True"'),('UnitCellAngle','"90"')]))
    add('05_floquet', 'With FloquetPort\n.Reset\n.SetDialogFrequency "10"\n.SetDialogTheta "0"\n.SetDialogPhi "0"\n.Port "Zmin"\n.SetNumberOfModesConsidered "2"\n.Port "Zmax"\n.SetNumberOfModesConsidered "2"\nEnd With')
    code=''
    for f in [8.3,10,12,14]:
        for field,typ in [('E','Efield'),('H','Hfield')]:
            code+='\n'+block('Monitor',[('Reset',''),('Name','"'+field+'_'+str(f)+'"'),('Dimension','"Volume"'),('Domain','"Frequency"'),('FieldType','"'+typ+'"'),('Frequency','"'+str(f)+'"'),('Create','')])
    add('06_monitors',code)
    add('07_solver',block('FDSolver',[('Reset',''),('SetMethod','"Tetrahedral", "General Purpose"'),('OrderTet','"Second"'),('AccuracyTet','"1e-4"'),('MeshAdaptionTet','"True"'),('ResetExcitationList',''),('AddToExcitationList','"Zmax", "TE(0,0)"'),('FrequencySamples','"80"'),('SetNumberOfResultDataSamples','"1801"'),('SetResultDataSamplingMode','"Equidistant"'),('UseParallelization','"True"'),('MaxCPUs','"8"')]))
    p.save(str(PROJECT))
    log('model_saved',project=str(PROJECT),tree=p.modeler.get_tree_items())
    (RUN/'stages'/'parameters.json').write_text(json.dumps(dict(period_mm=11,bottom_width_mm=9,top_width_mm=5,dielectric_thickness_mm=.2,copper_thickness_mm=.05,layers=20,epsilon_r=4.4,tan_delta=.02,conductivity_Sm=5e7,dielectric_shape='stepped square layers'),indent=2),encoding='utf-8')
    if '--build-only' not in sys.argv:
        log('solver_start')
        p.modeler.run_solver(timeout=86400)
        log('solver_complete',info=p.modeler.get_solver_run_info(),messages=str(p.get_messages()))
        p.save()
        (RUN/'exports'/'tree.json').write_text(json.dumps(p.modeler.get_tree_items(),indent=2),encoding='utf-8')
    p.close();de.close();de=None
    log('closed')
except Exception:
    log('error',traceback=traceback.format_exc())
    if de:
        try:p.save(str(PROJECT))
        except Exception:pass
    raise
