from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(r'C:\Users\huzst\Desktop\senior\metamaterial\ding2012-cst-absorber-reproduction-main\course_design_absorber\pyramid_optimization_5_40GHz');OUT=ROOT/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'Microsoft YaHei','axes.unicode_minus':False,'font.size':12,'axes.spines.top':False,'axes.spines.right':False})
items=[('P01_geometry_FR4_direct','1 几何展宽'),('P02_loss12_screen','2 增加损耗'),('P03_log_profile_screen_retry','3 对数轮廓'),('P04_high_eps_screen','4 紧凑周期'),('P05_loss18_screen','4a 损耗细调')]
fig,axs=plt.subplots(1,2,figsize=(15,7.8));fig.subplots_adjust(left=.075,right=.96,top=.78,bottom=.22,wspace=.3)
colors=['#7A8792','#C9784C','#8A70A6','#176D96','#27846C'];bars=[];labels=[];summary=[]
for (name,label),color in zip(items,colors):
 D=ROOT/'comparison_data'/name
 if not (D/'metrics.json').exists():
  if not (D/'endpoint_40GHz.json').exists():continue
  e=json.loads((D/'endpoint_40GHz.json').read_text());row=[40,e['latest_A'],1-e['latest_A'],0,e['R_copolar'][-1],0,e['R_higher'][-1],e['latest_S11_dB']];arr=np.array([row]);scope='40 GHz 端点筛选（4 级网格）'
 else:
  ar=np.genfromtxt(D/'spectrum.csv',delimiter=',',names=True);arr=np.atleast_2d(np.array(ar.tolist(),dtype=float));scope='离散已求解频点筛选'
 axs[0].scatter(arr[:,0],arr[:,1]*100,s=65,label=label,color=color,zorder=4)
 i=int(np.argmin(abs(arr[:,0]-40)));row=arr[i];bars.append([row[1]*100,(row[4]+row[5])*100,row[6]*100]);labels.append(label)
 summary.append(dict(name=name,scope=scope,at_40_GHz_A=float(row[1]),at_40_GHz_Rhigher=float(row[6]),at_40_GHz_S11_dB=float(row[7])))
axs[0].axhline(90,color='#C65C42',ls='--',lw=1.2);axs[0].set(xlim=(3,42),ylim=(65,101),xlabel='频率 / GHz',ylabel='总吸收率 / %',title='筛选数据：仅显示实际求解点');axs[0].set_xticks([5,10,20,30,40]);axs[0].grid(alpha=.16);axs[0].legend(frameon=False,fontsize=11,loc='lower left')
bars=np.array(bars);xx=np.arange(len(labels));bottom=np.zeros(len(labels))
for j,(co,la) in enumerate([('#176D96','吸收'),('#D9A37B','零阶反射（双极化）'),('#926E96','高阶衍射反射')]):
 axs[1].bar(xx,bars[:,j],bottom=bottom,color=co,width=.6,label=la);bottom+=bars[:,j]
for i,rec in enumerate(summary):axs[1].text(i,bars[i,0]/2,f"{bars[i,0]:.1f}%",color='white',ha='center',weight='bold',fontsize=10)
axs[1].axhline(90,color='#C65C42',ls='--',lw=1.2);axs[1].set(ylim=(0,103),ylabel='入射功率占比 / %',title='40 GHz 功率去向：含全部传播模态');axs[1].set_xticks(xx,[v.replace(' ','\n',1) for v in labels]);axs[1].legend(frameon=True,facecolor='white',framealpha=.94,edgecolor='none',loc='lower right',fontsize=10)
fig.text(.06,.94,'依次筛选：结构优化是否真正提高了总吸收？',fontsize=23,weight='bold',color='#17364A')
fig.text(.06,.865,'几何、损耗、轮廓依次调整；单频或五频点筛选可排除明显不达标的候选，不能据此证明连续带宽。',fontsize=11,color='#647382')
fig.text(.075,.095,'前三条路线的本组参数受到高阶反射限制；同极化 S11 < −10 dB 不能代替总吸收率 >90%。\n方案 1 的端点证据来自未完成宽带扫频的网格序列；方案 2/3 为正常完成的离散频点筛选。',fontsize=11,color='#647382',linespacing=1.8)
fig.savefig(OUT/'02_screening_comparison.png',dpi=180);plt.close(fig)
(ROOT/'screening_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print('screening image updated; completed candidates:',len(summary))
