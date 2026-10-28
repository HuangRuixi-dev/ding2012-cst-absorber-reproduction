from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
R=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.sans-serif':['Microsoft YaHei'],'axes.unicode_minus':False,'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
F=R/'figures';F.mkdir(exist_ok=True)
def save(fig,name):
 fig.savefig(F/(name+'.pdf'),bbox_inches='tight');fig.savefig(F/(name+'.png'),dpi=190,bbox_inches='tight');plt.close(fig)
summary=json.loads((R/'data/summary.json').read_text())
summary=[m for m in summary if not m['parameters']['strict'] or float(m['last_mesh_delta'])<.003]
summary.sort(key=lambda m:(m['parameters']['loss'],m['parameters']['strict']))
colors=['#2166AC','#D6604D','#439D78','#8C62AA','#B98028','#3B9EA5']
fig,ax=plt.subplots(figsize=(9.2,4.2))
base=np.loadtxt(R/'data/baseline_spectrum.csv',delimiter=',',skiprows=1)
ax.plot(base[:,0],base[:,1],color='.55',lw=1.2,label='已有 20 层基准')
for j,m in enumerate(summary):
 a=np.loadtxt(R/'runs'/m['case']/'spectrum.csv',delimiter=',',skiprows=1)
 p=m['parameters'];label=f"N={p['layers']}, H={p['height']:g} mm, tanδ={p['loss']:g}"+('（加严网格）' if p['strict'] else '')
 ax.plot(a[:,0],a[:,1],lw=1.6,color=colors[j%len(colors)],label=label)
ax.axhline(.9,color='black',ls='--',lw=1,label='90% 阈值');ax.set(xlim=(5,26),ylim=(0,1.025),xlabel='频率 / GHz',ylabel='总吸收率 A')
ax.legend(fontsize=9,loc='lower right',frameon=False);ax.grid(alpha=.15);save(fig,'optimization_spectra')
fig,ax=plt.subplots(figsize=(9.2,3.8))
for j,m in enumerate(summary):
 a=np.loadtxt(R/'runs'/m['case']/'spectrum.csv',delimiter=',',skiprows=1);p=m['parameters']
 ax.plot(a[:,0],a[:,1],lw=1.8,color=colors[j%len(colors)],label=f"tanδ={p['loss']:g}"+('（加严网格）' if p['strict'] else ''))
ax.axhline(.9,color='black',ls='--',lw=1);ax.set(xlim=(14,22),ylim=(.6,1.005),xlabel='频率 / GHz',ylabel='总吸收率 A');ax.grid(alpha=.15);ax.legend(frameon=False);save(fig,'dip_detail')
fig,axs=plt.subplots(1,2,figsize=(9,4.4),gridspec_kw={'width_ratios':[1.2,1]})
for ax,p,title in [(axs[0],dict(layers=40,height=10,bottom=10,top=2.5,period=11),'优化结构截面（x=0）')]:
 td=p['height']/p['layers']*.8;tm=p['height']/p['layers']*.2
 ax.add_patch(Rectangle((-p['period']/2,-.05),p['period'],.05,color='#C28B31'))
 for i,w in enumerate(np.linspace(p['bottom'],p['top'],p['layers'])):
  z=i*(td+tm);ax.add_patch(Rectangle((-w/2,z),w,td,color='#766C9F',lw=0));ax.add_patch(Rectangle((-w/2,z+td),w,tm,color='#CF9C46',lw=0))
 ax.set(xlim=(-6,6),ylim=(-.3,10.7),xlabel='y / mm',ylabel='z / mm',title=title,aspect='equal');ax.text(0,10.2,'入射方向 ↓',ha='center',fontsize=9)
axs[1].plot(np.linspace(9,5,20),np.linspace(0,4.75,20),'o-',ms=3,color='.5',label='基准：20 层')
axs[1].plot(np.linspace(10,2.5,40),np.linspace(0,9.75,40),'o-',ms=2.5,color='#2166AC',label='优化：40 层')
axs[1].set(xlabel='贴片边长 w / mm',ylabel='层起始高度 z / mm',title='几何变化');axs[1].legend(frameon=False);axs[1].grid(alpha=.15)
fig.tight_layout();save(fig,'geometry')
if (R/'data/final_selection.json').exists():
 final=json.loads((R/'data/final_selection.json').read_text());m=final['metrics'];b=final.get('reporting_guardband',m['best'])
 a=np.loadtxt(R/'runs'/final['case']/'spectrum.csv',delimiter=',',skiprows=1)
 fig,axs=plt.subplots(2,1,figsize=(9.2,5.8),sharex=True,gridspec_kw={'height_ratios':[1.15,1]})
 ax=axs[0];ax.plot(a[:,0],a[:,1],label='总吸收 A',lw=1.8,color='#2166AC');ax.plot(a[:,0],a[:,2],label='总反射 R',lw=1.3,color='#D6604D');ax.plot(a[:,0],a[:,3],label='透射 T（可忽略）',lw=1.2,color='#439D78')
 ax.axhline(.9,color='black',ls='--',lw=.8);ax.axvspan(b['lower_GHz'],b['upper_GHz'],alpha=.08,color='#439D78')
 ax.set(ylabel='功率比',ylim=(-.02,1.025));ax.legend(loc='center right',frameon=False,ncol=1);ax.grid(alpha=.15)
 axs[1].plot(a[:,0],a[:,5],label='同偏振 S11',color='#2166AC',lw=1.7);axs[1].axhline(-10,color='black',ls='--',lw=.8,label='-10 dB')
 axs[1].axvspan(b['lower_GHz'],b['upper_GHz'],alpha=.08,color='#439D78');axs[1].set(xlim=(5,26),ylim=(-45,0),xlabel='频率 / GHz',ylabel='反射系数 / dB');axs[1].legend(frameon=False);axs[1].grid(alpha=.15)
 fig.tight_layout();save(fig,'final_performance')
print('Figures updated:',len(summary),'completed cases')
