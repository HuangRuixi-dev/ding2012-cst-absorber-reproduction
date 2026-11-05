from pathlib import Path
import os
import json,math,sys,time,traceback,re,csv
from cst_runtime import bootstrap
bootstrap()
import cst.interface,cst.results
ROOT=Path(os.environ.get('CST_ABSORBER_RUN', str(Path(__file__).resolve().parents[1]/'cases')))
name=sys.argv[1];screen=True;strict=False
N=int(sys.argv[2]);H=float(sys.argv[3]);Wb=float(sys.argv[4]);P=float(sys.argv[5])
cfg=dict(name=name,N=N,H=H,Wb=Wb,Wt=.65,P=P,eps=4.4,loss=.02,law='log',copper_sigma_Sm=5e7,tm_mm=.05,frequency_GHz=[74,76],normal_incidence=True,excitation='TE(0,0)',screening=True,strict=False,screening_frequencies_GHz=[75],material_note='paper FR4 eps=4.4 tanD=0.02; finite copper conductivity; no measured dispersion; right-boundary discrete recheck; second-order adaptation at 75 GHz; 2-3 passes; delta S target 0.02; 50 Floquet modes retained')
ROOT.mkdir(parents=True,exist_ok=True)
if screen and strict:
 prior=json.loads((ROOT/'P05_loss18_full/metrics.json').read_text());cfg['screening_frequencies_GHz']=sorted(set(cfg['screening_frequencies_GHz']+[prior['min_A_frequency_GHz']]))
D=ROOT/name;D.mkdir(exist_ok=False);(D/'history').mkdir()
ordermax=max(2,int(math.floor(76*cfg['P']/299.792458)))
indices=sorted([(u,v) for u in range(-ordermax,ordermax+1) for v in range(-ordermax,ordermax+1)],key=lambda q:(q[0]**2+q[1]**2,q[0],q[1]))
modes=[dict(type=t,m=u,n=v,cutoff_GHz=299.792458/cfg['P']*math.sqrt(u*u+v*v)) for u,v in indices for t in ['TE','TM']]
cfg['modes']=modes;cfg['mode_count']=len(modes);cfg['td_mm']=cfg['H']/cfg['N']-.05
(D/'parameters.json').write_text(json.dumps(cfg,indent=2))
def log(event,**kw):
 rec=dict(time=time.strftime('%Y-%m-%d %H:%M:%S'),event=event,**kw);print(json.dumps(rec),flush=True)
 with (D/'execution.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
def block(obj,ls):return 'With '+obj+'\n'+'\n'.join('.'+k+' '+v for k,v in ls)+'\nEnd With'
de=cst.interface.DesignEnvironment.new();p=de.new_mws();log('owned_environment',pid=de.pid())
def add(n,code):
 (D/'history'/(n+'.vba')).write_text(code,encoding='utf-8');p.modeler.add_to_history(n,code,timeout=240);log(n)
def brick(n,mat,w,z0,z1):return block('Brick',[('Reset',''),('Name','"'+n+'"'),('Component','"pyramid"'),('Material','"'+mat+'"'),('Xrange','"-(%s)/2", "(%s)/2"'%(w,w)),('Yrange','"-(%s)/2", "(%s)/2"'%(w,w)),('Zrange','"%s", "%s"'%(z0,z1)),('Create','')])
try:
 pars={'P':cfg['P'],'Wb':cfg['Wb'],'Wt':cfg['Wt'],'H':cfg['H'],'N':cfg['N'],'tm':.05,'td':cfg['td_mm'],'epsr':cfg['eps'],'tand':cfg['loss']}
 add('01_units_parameters','\n'.join('StoreParameter "%s", "%s"'%(k,v) for k,v in pars.items())+'\nWith Units\n.Geometry "mm"\n.Frequency "GHz"\n.Time "ns"\nEnd With\nSolver.FrequencyRange "74", "76"\nChangeSolverType "HF Frequency Domain"')
 add('02_materials',block('Material',[('Reset',''),('Name','"Dielectric"'),('Type','"Normal"'),('Epsilon','"epsr"'),('Mue','"1"'),('TanD','"tand"'),('TanDFreq','"10"'),('TanDGiven','"True"'),('TanDModel','"ConstTanD"'),('Colour','"0.45", "0.3", "0.7"'),('Create','')])+'\n'+block('Material',[('Reset',''),('Name','"Copper"'),('Type','"Lossy metal"'),('Epsilon','"1"'),('Mue','"1"'),('Kappa','"5e7"'),('Colour','"0.9", "0.65", "0.2"'),('Create','')]))
 code=brick('ground','Copper','P','-0.05','0')
 for i in range(cfg['N']):
  frac='%d/(N-1)'%i
  w='Wb-(Wb-Wt)*('+frac+')' if cfg['law']=='linear' else 'Wb*(Wt/Wb)^('+frac+')'
  z='%d*(td+tm)'%i
  code+='\n'+brick('d_%03d'%i,'Dielectric',w,z,z+'+td')+'\n'+brick('cu_%03d'%i,'Copper',w,z+'+td',z+'+td+tm')
 add('03_geometry',code)
 add('04_boundary',block('Background',[('Type','"Normal"'),('Epsilon','"1"'),('Mue','"1"'),('XminSpace','"0"'),('XmaxSpace','"0"'),('YminSpace','"0"'),('YmaxSpace','"0"'),('ZminSpace','"3"'),('ZmaxSpace','"8"')])+'\n'+block('Boundary',[('Xmin','"unit cell"'),('Xmax','"unit cell"'),('Ymin','"unit cell"'),('Ymax','"unit cell"'),('Zmin','"open"'),('Zmax','"open"'),('Xsymmetry','"none"'),('Ysymmetry','"none"'),('Zsymmetry','"none"'),('SetPeriodicBoundaryAngles','"0", "0"'),('UnitCellFitToBoundingBox','"True"'),('UnitCellAngle','"90"')]))
 code='With FloquetPort\n.Reset\n.SetDialogFrequency "76"\n.SetDialogTheta "0"\n.SetDialogPhi "0"\n'
 for port in ['Zmin','Zmax']:
  code+='.Port "%s"\n.SetCustomizedListFlag "True"\n.SetNumberOfModesConsidered "%d"\n'%(port,len(modes))
  for mo in modes:code+='.AddMode "%s", "%d", "%d"\n'%(mo['type'],mo['m'],mo['n'])
 add('05_ports',code+'End With')
 add('06_solver',block('FDSolver',[('Reset',''),('SetMethod','"Tetrahedral", "General Purpose"'),('OrderTet','"Second"'),('Type','"Direct"'),('Stimulation','"List", "List"'),('ResetExcitationList',''),('AddToExcitationList','"Zmax", "TE(0,0)"'),('AccuracyTet','"1e-5"'),('MeshAdaptionTet','"True"'),('FrequencySamples','"220"'),('SetNumberOfResultDataSamples','"2951"'),('SetResultDataSamplingMode','"Frequency (linear)"'),('UseParallelization','"True"'),('MaxCPUs','"8"'),('SetStopSweepIfCriterionMet','"True"'),('SetSweepThreshold','"S-Parameters", "0.001"' if strict else '"S-Parameters", "0.01"'),('SweepErrorChecks','"3"'),('SweepMinimumSamples','"15"')])+'\n'+block('MeshAdaption3D',[('SetType','"HighFrequencyTet"'),('MinPasses','"4"' if strict else ('"2"' if screen else '"3"')),('MaxPasses','"7"' if strict else ('"3"' if screen else '"7"')),('MaxDeltaS','"0.01"' if strict else ('"0.02"' if screen else '"0.015"')),('NumberOfDeltaSChecks','"2"' if strict else ('"1"' if screen else '"2"')),('RemoveAllUserDefinedStopCriteria',''),('AddStopCriterion','"All S-Parameters", "0.01", "2", "True"' if strict else ('"All S-Parameters", "0.02", "1", "True"' if screen else '"All S-Parameters", "0.015", "2", "True"'))]))
 if False:
  add('07_valley_monitor',block('Monitor',[('Reset',''),('Name','\"E_12.4GHz\"'),('Dimension','\"Volume\"'),('Domain','\"Frequency\"'),('FieldType','\"Efield\"'),('Frequency','\"12.4\"'),('Create','')])+'\nWith FDSolver\n.AddMonitorSamples \"True\"\nEnd With')
 if name.startswith('P06'):
  add('07_critical_stability_samples','With FDSolver\n.SetMethod \"\", \"Discrete samples only\"\n.ResetSampleIntervals \"all\"\n.AddSampleInterval \"12.23\", \"12.23\", \"1\", \"Single\", \"True\"\nEnd With')
 elif screen:
  add('07_screening_samples','With FDSolver\n.SetMethod "", "Discrete samples only"\n.ResetSampleIntervals "all"\n'+''.join('.AddSampleInterval "%s", "%s", "1", "Single", "%s"\n'%(f,f,'True' if f==75 else 'False') for f in cfg['screening_frequencies_GHz'])+'End With')
 p.save(str(D/'absorber.cst'));log('saved_solver_start')
 p.modeler.run_solver(timeout=24000);info=p.modeler.get_solver_run_info();log('solver_returned',info=info,messages=str(p.get_messages()))
 if info['state']!='SUCCESS':raise RuntimeError('Solver did not succeed: '+str(info))
 p.save();p.close();de.close();log('closed')
 # Native complex result extraction, all channels preserved.
 pf=cst.results.ProjectFile(str(D/'absorber.cst'));res=pf.get_3d();raw={}
 for key in res.get_tree_items():
  if not key.startswith('1D Results\\S-Parameters\\'):continue
  ids=list(res.get_run_ids(key));it=res.get_result_item(key,run_id=ids[-1]);yy=it.get_ydata();yy=[yy] if isinstance(yy,(int,float,complex)) else yy;y=[complex(v) for v in yy]
  xx=it.get_xdata();xx=list(xx) if hasattr(xx,'__iter__') else [];xx=xx if xx else ([12.23] if name.startswith('P06') and len(y)==1 else [])
  raw[key]=dict(run_id=ids[-1],frequency_GHz=xx,real=[z.real for z in y],imag=[z.imag for z in y])
 (D/'sparameters.json').write_text(json.dumps(raw),encoding='utf-8')
 cutoffs={}
 for key in res.get_tree_items():
  if key.startswith('1D Results\\Port Information\\Cutoff Frequency\\'):
   it=res.get_result_item(key,run_id=res.get_run_ids(key)[-1]);cutoffs[key.rsplit('\\',1)[-1]]=float(it.get_ydata())
 (D/'port_cutoffs.json').write_text(json.dumps(cutoffs,indent=2))
 log('native_exported',channels=len(raw))
except Exception:
 log('error',traceback=traceback.format_exc())
 try:p.save(str(D/'absorber.cst'))
 except Exception:pass
 raise
