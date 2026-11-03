from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(r'C:\Users\huzst\Desktop\senior\metamaterial\ding2012-cst-absorber-reproduction-main\course_design_absorber\pyramid_optimization_5_40GHz')
OUT=ROOT/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'Microsoft YaHei','axes.unicode_minus':False,'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
cases=[('论文原结构',20,5,9,5,11,4.4,.02,'linear'),('方案 1：几何展宽',80,20,16,1.5,17,4.4,.02,'linear'),('方案 2：增加损耗',80,20,16,1.5,17,4.4,.12,'linear'),('方案 3：非线性轮廓',80,20,16,1.5,17,4.4,.12,'log'),('方案 4：紧凑高介电常数',80,20,6.9,.65,7.2,22,.12,'log')]
fig,axes=plt.subplots(1,5,figsize=(16,6.8));fig.subplots_adjust(left=.04,right=.98,top=.77,bottom=.29,wspace=.3)
for ax,(n,N,H,wb,wt,P,eps,loss,law) in zip(axes,cases):
 t=np.linspace(0,1,N);w=wb-(wb-wt)*t if law=='linear' else wb*(wt/wb)**t;z=t*H
 for wi,zi in zip(w,z):ax.plot([-wi/2,wi/2],[zi,zi],color='#98673C',lw=1.1)
 ax.fill_betweenx(z,-w/2,w/2,color='#A6B7CE',alpha=.35)
 ax.plot([-P/2,P/2],[0,0],color='#3F5264',lw=4)
 ax.set(xlim=(-9,9),ylim=(-1,22),xlabel='横向 / mm');ax.set_title(n,fontsize=11,weight='bold');ax.grid(alpha=.12)
 ax.text(.5,-.24,f'N={N}，H={H} mm\nWb={wb}，Wt={wt} mm\nP={P} mm；εr={eps}\ntanδ={loss}；{law}',transform=ax.transAxes,ha='center',va='top',fontsize=9.5,linespacing=1.5)
axes[0].set_ylabel('高度 / mm')
fig.text(.04,.94,'围绕论文金字塔结构的四条初始优化路线',fontsize=24,weight='bold',color='#16364B')
fig.text(.04,.865,'全部保留：铜—介质交替层、沿高度渐变截面、周期阵列和金属背板。图为剖面参数示意，不代表性能已达标。',fontsize=11,color='#5F6F7D')
fig.text(.04,.035,'参考：Ding et al., Applied Physics Letters 100, 103506 (2012), doi:10.1063/1.3692178。各候选方案需依次由 CST 核验。',fontsize=10,color='#5F6F7D')
fig.savefig(OUT/'01_routes.png',dpi=180);plt.close(fig)
print(OUT/'01_routes.png')

