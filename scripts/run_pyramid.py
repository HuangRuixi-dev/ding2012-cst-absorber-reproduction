from pathlib import Path
import json,math,sys,time,traceback,re,csv
import cst.interface,cst.results
ROOT=Path(r'C:\Users\huzst\Desktop\senior\metamaterial\ding2012-cst-absorber-reproduction-main\course_design_absorber\pyramid_optimization_5_40GHz')
CASES={
'P01_geometry_FR4':dict(route=1,N=80,H=20,Wb=16,Wt=1.5,P=17,eps=4.4,loss=.02,law='linear'),
'P02_loss12':dict(route=2,N=80,H=20,Wb=16,Wt=1.5,P=17,eps=4.4,loss=.12,law='linear'),
'P03_log_profile':dict(route=3,N=80,H=20,Wb=16,Wt=1.5,P=17,eps=4.4,loss=.12,law='log'),
'P04_high_eps':dict(route=4,N=80,H=20,Wb=6.9,Wt=.65,P=7.2,eps=22,loss=.12,law='log'),
'P05_loss18':dict(route=4,N=80,H=20,Wb=6.9,Wt=.65,P=7.2,eps=22,loss=.18,law='log'),
'P06_critical_stability':dict(route=4,N=80,H=20,Wb=6.9,Wt=.65,P=7.2,eps=22,loss=.18,law='log')}
name=sys.argv[1];screen='_screen' in name;strict=('_strict' in name or name.startswith('P06'));cfg=CASES[name.replace("_direct","").replace("_screen","").replace("_full","").replace("_retry","").replace("_strict","")].copy();cfg.update(name=name,copper_sigma_Sm=5e7,tm_mm=.05,frequency_GHz=[5,40],normal_incidence=True,excitation='TE(0,0)',screening=screen,strict=strict,screening_frequencies_GHz=([5,10,11.5,12.4,13.5,20,30,40] if name.startswith('P05') else [5,10,20,30,40]) if screen else None,material_note='FR4 as paper' if name.startswith('P01_geometry_FR4') else 'engineered dielectric parameters; not paper FR4')
if name.startswith('P06'):cfg['screening_frequencies_GHz']=[12.23]
ROOT.mkdir(parents=True,exist_ok=True)
if screen and strict:
 prior=json.loads((ROOT/'P05_loss18_full/metrics.json').read_text());cfg['screening_frequencies_GHz']=sorted(set(cfg['screening_frequencies_GHz']+[prior['min_A_frequency_GHz']]))
D=ROOT/name;D.mkdir(exist_ok=False);(D/'history').mkdir()
ordermax=max(2 if strict else 1,int(math.floor(40*cfg['P']/299.792458)))
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
 add('01_units_parameters','\n'.join('StoreParameter "%s", "%s"'%(k,v) for k,v in pars.items())+'\nWith Units\n.Geometry "mm"\n.Frequency "GHz"\n.Time "ns"\nEnd With\nSolver.FrequencyRange "5", "40"\nChangeSolverType "HF Frequency Domain"')
 add('02_materials',block('Material',[('Reset',''),('Name','"Dielectric"'),('Type','"Normal"'),('Epsilon','"epsr"'),('Mue','"1"'),('TanD','"tand"'),('TanDFreq','"10"'),('TanDGiven','"True"'),('TanDModel','"ConstTanD"'),('Colour','"0.45", "0.3", "0.7"'),('Create','')])+'\n'+block('Material',[('Reset',''),('Name','"Copper"'),('Type','"Lossy metal"'),('Epsilon','"1"'),('Mue','"1"'),('Kappa','"5e7"'),('Colour','"0.9", "0.65", "0.2"'),('Create','')]))
 code=brick('ground','Copper','P','-0.05','0')
 for i in range(cfg['N']):
  frac='%d/(N-1)'%i
  w='Wb-(Wb-Wt)*('+frac+')' if cfg['law']=='linear' else 'Wb*(Wt/Wb)^('+frac+')'
  z='%d*(td+tm)'%i
  code+='\n'+brick('d_%03d'%i,'Dielectric',w,z,z+'+td')+'\n'+brick('cu_%03d'%i,'Copper',w,z+'+td',z+'+td+tm')
 add('03_geometry',code)
 add('04_boundary',block('Background',[('Type','"Normal"'),('Epsilon','"1"'),('Mue','"1"'),('XminSpace','"0"'),('XmaxSpace','"0"'),('YminSpace','"0"'),('YmaxSpace','"0"'),('ZminSpace','"3"'),('ZmaxSpace','"8"')])+'\n'+block('Boundary',[('Xmin','"unit cell"'),('Xmax','"unit cell"'),('Ymin','"unit cell"'),('Ymax','"unit cell"'),('Zmin','"open"'),('Zmax','"open"'),('Xsymmetry','"none"'),('Ysymmetry','"none"'),('Zsymmetry','"none"'),('SetPeriodicBoundaryAngles','"0", "0"'),('UnitCellFitToBoundingBox','"True"'),('UnitCellAngle','"90"')]))
 code='With FloquetPort\n.Reset\n.SetDialogFrequency "40"\n.SetDialogTheta "0"\n.SetDialogPhi "0"\n'
 for port in ['Zmin','Zmax']:
  code+='.Port "%s"\n.SetCustomizedListFlag "True"\n.SetNumberOfModesConsidered "%d"\n'%(port,len(modes))
  for mo in modes:code+='.AddMode "%s", "%d", "%d"\n'%(mo['type'],mo['m'],mo['n'])
 add('05_ports',code+'End With')
 add('06_solver',block('FDSolver',[('Reset',''),('SetMethod','"Tetrahedral", "General Purpose"'),('OrderTet','"Second"'),('Type','"Direct"'),('Stimulation','"List", "List"'),('ResetExcitationList',''),('AddToExcitationList','"Zmax", "TE(0,0)"'),('AccuracyTet','"1e-5"'),('MeshAdaptionTet','"True"'),('FrequencySamples','"220"'),('SetNumberOfResultDataSamples','"3501"'),('SetResultDataSamplingMode','"Frequency (linear)"'),('UseParallelization','"True"'),('MaxCPUs','"8"'),('SetStopSweepIfCriterionMet','"True"'),('SetSweepThreshold','"S-Parameters", "0.001"' if strict else '"S-Parameters", "0.003"'),('SweepErrorChecks','"3"'),('SweepMinimumSamples','"15"')])+'\n'+block('MeshAdaption3D',[('SetType','"HighFrequencyTet"'),('MinPasses','"4"' if strict else ('"2"' if screen else '"3"')),('MaxPasses','"7"' if strict else ('"3"' if screen else '"7"')),('MaxDeltaS','"0.003"' if strict else ('"0.02"' if screen else '"0.006"')),('NumberOfDeltaSChecks','"2"' if strict else ('"1"' if screen else '"2"')),('RemoveAllUserDefinedStopCriteria',''),('AddStopCriterion','"All S-Parameters", "0.003", "2", "True"' if strict else ('"All S-Parameters", "0.02", "1", "True"' if screen else '"All S-Parameters", "0.006", "2", "True"'))]))
 if name.startswith('P05') and not screen:
  add('07_valley_monitor',block('Monitor',[('Reset',''),('Name','\"E_12.4GHz\"'),('Dimension','\"Volume\"'),('Domain','\"Frequency\"'),('FieldType','\"Efield\"'),('Frequency','\"12.4\"'),('Create','')])+'\nWith FDSolver\n.AddMonitorSamples \"True\"\nEnd With')
 if name.startswith('P06'):
  add('07_critical_stability_samples','With FDSolver\n.SetMethod \"\", \"Discrete samples only\"\n.ResetSampleIntervals \"all\"\n.AddSampleInterval \"12.23\", \"12.23\", \"1\", \"Single\", \"True\"\nEnd With')
 elif screen:
  add('07_screening_samples','With FDSolver\n.ResetSampleIntervals \"all\"\n.AddSampleInterval \"40\", \"40\", \"1\", \"Single\", \"True\"\n'+''.join('.AddSampleInterval \"%s\", \"%s\", \"1\", \"Single\", \"False\"\n'%(f,f) for f in cfg['screening_frequencies_GHz'] if f!=40)+'End With')
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
