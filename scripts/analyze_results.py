from pathlib import Path
import json,re,os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.signal import find_peaks
from scipy.ndimage import median_filter
root=Path(__file__).resolve().parent
run=Path(os.environ.get('CST_REPRO_RUN',str(root/'tasks/ding2012/runs/run_001'))); out=run/'analysis'; out.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':160})
raw=json.loads((run/'exports/sparameters.json').read_text())
print('AVAILABLE',list(raw))
# CST Floquet notation: receiving port/mode followed by exciting port/mode.
def pair(k):
 return re.findall(r'Z(?:max|min)\([12]\)',k,re.I)
selected={k:v for k,v in raw.items() if len(pair(k))==2 and pair(k)[1].lower()=='zmax(1)'}
if len(selected)<2:raise RuntimeError('Cannot identify S parameters for excitation Zmax(1)')
f=np.asarray(next(iter(selected.values()))['frequency_GHz'])
R=np.zeros_like(f);T=R.copy();cross=R.copy()
for k,v in selected.items():
 y=np.asarray(v['real'])+1j*np.asarray(v['imag']);power=abs(y)**2
 if pair(k)[0].lower().startswith('zmax'):
  R+=power
  if pair(k)[0].lower()=='zmax(2)':cross+=power
 else:T+=power
A=1-R-T
np.savetxt(out/'spectrum.csv',np.column_stack([f,A,R,T,cross]),delimiter=',',header='frequency_GHz,absorption,reflection,transmission,cross_reflection',comments='')
def bands(x,y,threshold=.9):
 b=y>=threshold;edges=np.diff(np.r_[False,b,False].astype(int));ans=[]
 for lo,hi in zip(np.where(edges==1)[0],np.where(edges==-1)[0]-1):
  fl=x[lo] if lo==0 else x[lo-1]+(threshold-y[lo-1])*(x[lo]-x[lo-1])/(y[lo]-y[lo-1])
  fu=x[hi] if hi==len(x)-1 else x[hi]+(threshold-y[hi])*(x[hi+1]-x[hi])/(y[hi+1]-y[hi])
  ans.append([float(fl),float(fu),float(200*(fu-fl)/(fu+fl))])
 return ans
ref=np.loadtxt(root.parent/'data/paper_simulation_digitized_clean.csv',delimiter=',',skiprows=1)
exp=np.loadtxt(root.parent/'data/paper_experiment_digitized_clean.csv',delimiter=',',skiprows=1)
ref[:,1]=np.where(abs(ref[:,1]-median_filter(ref[:,1],size=13,mode='nearest'))>.12,median_filter(ref[:,1],size=13,mode='nearest'),ref[:,1])
ref=ref[ref[:,0]>=6.1]
exp=exp[(exp[:,0]>=7.8)&(exp[:,0]<=14.7)]
np.savetxt(out/'paper_simulation_digitized_clean.csv',ref,delimiter=',',header='frequency_GHz,absorption',comments='')
np.savetxt(out/'paper_experiment_digitized_clean.csv',exp,delimiter=',',header='frequency_GHz,absorption',comments='')
mask=(f>=ref[0,0])&(f<=ref[-1,0]);err=A[mask]-np.interp(f[mask],ref[:,0],ref[:,1])
metrics={'bands_A_ge_0.9':bands(f,A),'max_transmission':float(T.max()),'max_cross_reflection':float(cross.max()),'RMSE_vs_digitized_paper_simulation':float(np.sqrt(np.mean(err**2))),'MAE_vs_digitized_paper_simulation':float(np.mean(abs(err))),'samples':len(f),'paper_reported_sim_RAB_percent':53.1,'paper_reported_experimental_band_GHz':[7.8,14.7]}
fig,axs=plt.subplots(2,1,figsize=(8,7),sharex=True,layout='constrained')
axs[0].plot(f,A,color='#155ac4',lw=1.5,label='Absorption A (this CST run)');axs[0].plot(f,R,color='#d83c35',lw=1.2,label='Reflection R');axs[0].plot(f,T,color='#339242',lw=1.2,label='Transmission T')
axs[0].set_title('(a) Computed power spectra');axs[0].legend(loc='center',frameon=False)
axs[1].plot(f,A,color='#155ac4',lw=1.6,label='This CST simulation');axs[1].plot(ref[:,0],ref[:,1],color='#252525',ls='--',lw=1,label='Paper simulation (digitized)');axs[1].plot(exp[:,0],exp[:,1],color='#d83c35',alpha=.85,lw=.9,label='Paper experiment (digitized)')
axs[1].set_title('(b) Comparison with Fig. 2 of Ding et al. (2012)');axs[1].legend(loc='lower center',frameon=False)
for ax in axs:ax.axhline(.9,color='0.5',ls=':',lw=.8);ax.set(xlim=(6,15),ylim=(0,1.035),ylabel='Power fraction');ax.grid(alpha=.18)
axs[1].set_xlabel('Frequency (GHz)');fig.savefig(out/'figure2_reproduced.png',dpi=240);plt.close(fig)
# A model cross-section drawn directly from the actual dimensions used in CST.
fig,ax=plt.subplots(figsize=(6.6,4.5),layout='constrained')
ax.add_patch(Rectangle((-5.5,-.05),11,.05,color='#c99728',label='Copper'))
for i in range(20):
 w=9-4*i/19;z=.25*i
 ax.add_patch(Rectangle((-w/2,z),w,.2,color='#7b487c',label='FR4' if i==0 else None))
 ax.add_patch(Rectangle((-w/2,z+.2),w,.05,color='#c99728'))
ax.annotate('Incident plane wave',xy=(0,5.2),xytext=(0,6.2),ha='center',arrowprops={'arrowstyle':'->','lw':1.5})
ax.set(xlim=(-5.6,5.6),ylim=(-.25,6.8),xlabel='y (mm)',ylabel='z (mm)',title='Model at x = 0: 20 copper / FR4 composite layers');ax.set_aspect('equal');ax.legend(frameon=False);fig.savefig(out/'model_cross_section.png',dpi=220);plt.close(fig)
fig,axs=plt.subplots(4,2,figsize=(9,9.8),layout='constrained')
field_stats=[]
for i,freq in enumerate(['8.3','10','12','14']):
 for j,typ in enumerate(['E','H']):
  path=run/'exports'/(typ+'_'+freq+'_x0.txt')
  lines=[]
  for line in path.read_text(errors='replace').splitlines():
   try:
    row=[float(v) for v in line.split()]
    if len(row)>=9:lines.append(row)
   except ValueError:pass
  data=np.array(lines)
  if not len(data):raise RuntimeError('No numeric fields: '+str(path))
  data=data[np.isclose(data[:,0],0,atol=1e-12)]
  if not len(data):raise RuntimeError('Central plane x=0 is missing')
  y=np.unique(data[:,1]);z=np.unique(data[:,2]);amp=np.sqrt(np.sum(data[:,3:9]**2,axis=1))
  grid=np.full((len(z),len(y)),np.nan);grid[np.searchsorted(z,data[:,2]),np.searchsorted(y,data[:,1])]=amp
  yy,zz=np.meshgrid(y,z)
  # Exclude conducting interiors when locating the dielectric resonance.
  layer=np.clip(np.floor(zz/.25).astype(int),0,19);w=9-4*layer/19
  dielectric=(zz>=0)&(zz<5)&((zz% .25)<.199)&(abs(yy)<w/2-.06)
  profile=np.nansum(np.where(dielectric,grid**2,0),axis=1)
  hotspot=float(z[np.argmax(profile)])
  mx=float(np.nanmax(grid))
  if not np.isfinite(mx) or mx<=0:raise RuntimeError('Invalid zero field export: '+str(path))
  norm=grid/mx
  ax=axs[i,j];pic=ax.pcolormesh(y,z,norm,cmap='turbo',vmin=0,vmax=1,shading='auto',rasterized=True)
  for n in range(20):
   wn=9-4*n/19;zn=.25*n
   ax.add_patch(Rectangle((-wn/2,zn+.2),wn,.05,fill=False,edgecolor='white',lw=.25,alpha=.8))
  ax.plot([-4.5,-2.5],[0,5],color='white',lw=.4);ax.plot([4.5,2.5],[0,5],color='white',lw=.4)
  ax.set(xlim=(-5.5,5.5),ylim=(0,5.5),ylabel='z (mm)',title=f'{typ}-field | {freq} GHz');ax.set_aspect('equal');
  if i==3:ax.set_xlabel('y (mm)')
  fig.colorbar(pic,ax=ax,fraction=.035,pad=.02,label='|'+typ+'| / max')
  field_stats.append(dict(field=typ,frequency_GHz=float(freq),max_amplitude=mx,unit='V/m' if typ=='E' else 'A/m',dielectric_energy_peak_z_mm=hotspot,grid_shape=list(grid.shape)))
  np.savez_compressed(out/(typ+'_'+freq+'_field.npz'),y=y,z=z,amplitude=grid)
fig.savefig(out/'figure3_reproduced.png',dpi=240);plt.close(fig)
metrics['fields']=field_stats
(out/'metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8');print(json.dumps(metrics,indent=2))
