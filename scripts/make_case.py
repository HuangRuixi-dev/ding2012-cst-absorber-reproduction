from pathlib import Path
import argparse,json
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('--layers',type=int,default=40);p.add_argument('--height',type=float,default=10);p.add_argument('--bottom',type=float,default=10);p.add_argument('--top',type=float,default=2.5);p.add_argument('--loss',type=float,default=.02);p.add_argument('--period',type=float,default=11);p.add_argument('--fmax',type=float,default=26);p.add_argument('--modes',type=int,default=2);p.add_argument('--law',choices=['linear','reciprocal'],default='linear');p.add_argument('--strict',action='store_true');a=p.parse_args()
c=R/'runs'/a.name;c.mkdir(exist_ok=False);(c/'stages').mkdir()
cfg=vars(a);cfg.update(epsilon_r=4.4,conductivity_Sm=5e7,copper_fraction=.2,frequency_min_GHz=5)
(c/'parameters.json').write_text(json.dumps(cfg,indent=2))
def block(obj,lines):return 'With '+obj+'\n'+ '\n'.join('.'+k+' '+v for k,v in lines)+'\nEnd With'
def write(n,s):(c/'stages'/(n+'.vba')).write_text(s,encoding='utf-8')
params={'P':a.period,'Wl':a.bottom,'Wt':a.top,'N':a.layers,'H':a.height,'tm':a.height/a.layers*.2,'td':a.height/a.layers*.8,'eps_r':4.4,'loss_tan':a.loss}
write('01_units_parameters','\n'.join('StoreParameter "'+k+'", "'+str(v)+'"' for k,v in params.items())+'\nWith Units\n.Geometry "mm"\n.Frequency "GHz"\n.Time "ns"\nEnd With\nSolver.FrequencyRange "5", "'+str(a.fmax)+'"\nChangeSolverType "HF Frequency Domain"')
write('02_materials',block('Material',[('Reset',''),('Name','"Dielectric_design"'),('Type','"Normal"'),('Epsilon','"eps_r"'),('Mue','"1"'),('TanD','"loss_tan"'),('TanDFreq','"10"'),('TanDGiven','"True"'),('TanDModel','"ConstTanD"'),('Colour','"0.5", "0.2", "0.6"'),('Create','')])+'\n'+block('Material',[('Reset',''),('Name','"Copper_design"'),('Type','"Lossy metal"'),('Epsilon','"1"'),('Mue','"1"'),('Kappa','"5e7"'),('Colour','"0.9", "0.7", "0.2"'),('Create','')]))
def brick(name,mat,w,z0,z1):return block('Brick',[('Reset',''),('Name','"'+name+'"'),('Component','"absorber"'),('Material','"'+mat+'"'),('Xrange','"-('+w+')/2", "('+w+')/2"'),('Yrange','"-('+w+')/2", "('+w+')/2"'),('Zrange','"'+z0+'", "'+z1+'"'),('Create','')])
geo=brick('ground','Copper_design','P','-0.05','0')
for i in range(a.layers):
 w='Wl-(Wl-Wt)*{}/(N-1)'.format(i) if a.law=='linear' else '1/(1/Wl+(1/Wt-1/Wl)*{}/(N-1))'.format(i)
 z='{}*(td+tm)'.format(i)
 geo+='\n'+brick('d_%03d'%i,'Dielectric_design',w,z,z+'+td')+'\n'+brick('cu_%03d'%i,'Copper_design',w,z+'+td',z+'+td+tm')
write('03_geometry',geo)
write('04_boundaries',block('Background',[('Type','"Normal"'),('Epsilon','"1"'),('Mue','"1"'),('XminSpace','"0"'),('XmaxSpace','"0"'),('YminSpace','"0"'),('YmaxSpace','"0"'),('ZminSpace','"3"'),('ZmaxSpace','"6"')])+'\n'+block('Boundary',[('Xmin','"unit cell"'),('Xmax','"unit cell"'),('Ymin','"unit cell"'),('Ymax','"unit cell"'),('Zmin','"open"'),('Zmax','"open"'),('Xsymmetry','"none"'),('Ysymmetry','"none"'),('Zsymmetry','"none"'),('SetPeriodicBoundaryAngles','"0", "0"'),('UnitCellFitToBoundingBox','"True"'),('UnitCellAngle','"90"')]))
write('05_floquet','With FloquetPort\n.Reset\n.SetDialogFrequency "15"\n.SetDialogTheta "0"\n.SetDialogPhi "0"\n.Port "Zmin"\n.SetNumberOfModesConsidered "'+str(a.modes)+'"\n.Port "Zmax"\n.SetNumberOfModesConsidered "'+str(a.modes)+'"\nEnd With')
write('06_solver',block('FDSolver',[('Reset',''),('SetMethod','"Tetrahedral", "General Purpose"'),('OrderTet','"Second"'),('Stimulation','"List", "List"'),('ResetExcitationList',''),('AddToExcitationList','"Zmax", "TE(0,0)"'),('AccuracyTet','"1e-5"' if a.strict else '"1e-4"'),('MeshAdaptionTet','"True"'),('FrequencySamples','"160"'),('SetNumberOfResultDataSamples','"2601"'),('SetResultDataSamplingMode','"Frequency (linear)"'),('UseParallelization','"True"'),('MaxCPUs','"8"')]))
if a.strict:
 s=c/'stages/06_solver.vba'
 s.write_text(s.read_text()+'\nWith FDSolver\n.SetStopSweepIfCriterionMet "True"\n.SetSweepThreshold "S-Parameters", "0.001"\n.SweepErrorChecks "3"\n.SweepMinimumSamples "10"\nEnd With\n')
 s.write_text(s.read_text()+'\nWith MeshAdaption3D\n.SetType "HighFrequencyTet"\n.MinPasses "4"\n.MaxPasses "8"\n.MaxDeltaS "0.003"\n.NumberOfDeltaSChecks "2"\n.RemoveAllUserDefinedStopCriteria\n.AddStopCriterion "All S-Parameters", "0.003", "2", "True"\nEnd With\n')
print(c)
