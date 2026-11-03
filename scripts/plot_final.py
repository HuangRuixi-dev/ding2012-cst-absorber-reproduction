from pathlib import Path
import json,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(r'C:\Users\huzst\Desktop\senior\metamaterial\ding2012-cst-absorber-reproduction-main\course_design_absorber\pyramid_optimization_5_40GHz');OUT=ROOT/'figures';name=sys.argv[1];D=ROOT/name
m=json.loads((D/'metrics.json').read_text());cfg=json.loads((D/'parameters.json').read_text());a=np.genfromtxt(D/'spectrum.csv',delimiter=',',names=True)
assert m['full_5_40_pass'];assert not m['screening'];assert m['mesh_converged'] and m['broadband_converged'] and m['power_sanity'] and not m['solver_errors']
plt.rcParams.update({'font.family':'Microsoft YaHei','axes.unicode_minus':False,'font.size':12,'axes.spines.top':False,'axes.spines.right':False})
BLUE='#176D96';RED='#CB6947';GREEN='#27846C';GRAY='#637381'
f=a['frequency_GHz'];fig=plt.figure(figsize=(14,9));fig.text(.06,.946,'金字塔优化方案：连续频段性能验证',fontsize=24,weight='bold',color='#18384D');fig.text(.06,.9,'铜—设计介质交替层 + 对数渐变截面 + 铜背板；CST 法向入射 TE(0,0)，按全部传播模态核算功率。',fontsize=11,color=GRAY)
ax=fig.add_axes([.08,.55,.56,.28]);ax.plot(f,a['A']*100,color=BLUE,lw=2,label='总吸收 A');ax.plot(f,a['R']*100,color=RED,lw=1.5,label='总反射 R');ax.plot(f,a['T']*100,color=GREEN,lw=1,ls=':',label='透射 T≈0');old=np.genfromtxt(ROOT/'comparison_data/P04_high_eps_full/spectrum.csv',delimiter=',',names=True);ax.plot(old['frequency_GHz'],old['A']*100,color=GRAY,lw=1.2,ls='--',label='填谷前 A（tanδ=0.12）');ax.axhline(90,color=RED,ls='--',lw=1);ax.set(xlim=(5,40),ylim=(-2,103),ylabel='功率占比 / %');ax.grid(alpha=.18);fig.legend(*ax.get_legend_handles_labels(),loc='upper left',bbox_to_anchor=(.08,.535),ncol=2,frameon=False,fontsize=10)
ins=fig.add_axes([.22,.61,.31,.12]);ins.plot(f,a['A']*100,color=BLUE,lw=1.3);ins.plot(old['frequency_GHz'],old['A']*100,color=GRAY,lw=1,ls='--');ins.axhline(90,color=RED,ls='--',lw=.8);ins.set(xlim=(5,40),ylim=(87,100.1));ins.tick_params(labelsize=8);ins.grid(alpha=.15);ins.set_title('填谷前后 A 放大 / %',fontsize=9)
ax2=fig.add_axes([.08,.19,.56,.27]);ax2.plot(f,a['S11_dB'],color=BLUE,lw=1.6,label='同极化 S11');ax2.axhline(-10,color=RED,ls='--',label='−10 dB 验收线');ax2.set(xlim=(5,40),ylim=(min(-45,float(a['S11_dB'].min())-3),-5),xlabel='频率 / GHz',ylabel='S11 / dB');ax2.grid(alpha=.18);ax2.legend(frameon=False,loc='lower left',fontsize=10)
fig.text(.7,.74,f"最低总吸收率\n{m['min_A']*100:.3f}%",fontsize=24,color=BLUE,weight='bold',linespacing=1.5)
fig.text(.7,.57,f"最不利频点：{m['min_A_frequency_GHz']:.2f} GHz\n最差 S11：{m['max_copolar_S11_dB']:.2f} dB",fontsize=13,linespacing=2)
fig.text(.7,.37,'验证频段：5–40 GHz\n绝对带宽：35 GHz\n相对带宽：155.56%',fontsize=14,color=GREEN,linespacing=1.9)
fig.text(.7,.2,'全频段通过' if m['full_5_40_pass'] else '本组参数仍未全频段通过',fontsize=18,color=GREEN if m['full_5_40_pass'] else RED,weight='bold')
fig.text(.06,.085,f"工程：{name}；输出 {m['samples']} 个频率点（宽带插值输出，非同等数量的独立求解频点）。",fontsize=10,color=GRAY)
fig.text(.06,.04,f"设计介质 εr={cfg['eps']}、tanδ={cfg['loss']} 为仿真假设，区别于原文 FR4；理想周期阵列、法向入射。",fontsize=10,color=GRAY)
fig.savefig(OUT/'03_fullband_performance.png',dpi=185);plt.close(fig)
# Comparisons and evidence
fig=plt.figure(figsize=(14,8.3));fig.text(.06,.944,'结构继承、文献对比与收敛证据',fontsize=24,weight='bold',color='#18384D');fig.text(.06,.89,'以铜—介质渐变金字塔为基础，优化周期、轮廓与损耗参数，扩展吸收频段。',fontsize=11,color=GRAY)
ax=fig.add_axes([.23,.6,.43,.19]);bands=[(7.8,14.7),(7.160414,26),(5,40)]
for i,((lo,hi),c) in enumerate(zip(bands,[GRAY,'#A7BBC6',BLUE])):ax.barh(i,hi-lo,left=lo,height=.52,color=c);ax.text((lo+hi)/2,i,f'{lo:.2f}–{hi:g} GHz',ha='center',va='center',color='white',fontsize=10)
ax.set_yticks(range(3),['Ding 2012（实验）','原 C06（仿真）','本次金字塔（仿真）']);ax.invert_yaxis();ax.set(xlim=(0,42),xlabel='A >90% 的连续频段 / GHz');ax.grid(axis='x',alpha=.15)
ax=fig.add_axes([.09,.25,.56,.23]);ax.axis('off');rows=[['层数 / 高度','20 / 5 mm','80 / 20 mm'],['底宽 / 顶宽','9 / 5 mm','6.9 / 0.65 mm'],['周期','11 mm','7.2 mm'],['介质 εr / tanδ','4.4 / 0.02',f"{cfg['eps']} / {cfg['loss']}"],['铜层 / 介质层厚','0.05 / 0.20 mm','0.05 / 0.20 mm'],['宽度渐变','线性','对数']]
t=ax.table(cellText=rows,colLabels=['参数','论文原结构','本次方案'],loc='center',cellLoc='center',colWidths=[.32,.34,.34]);t.auto_set_font_size(False);t.set_fontsize(10);t.scale(1,1.65)
for (r,c),cell in t.get_celld().items():
 cell.set_edgecolor('#D8E0E5')
 if r==0:cell.set_facecolor('#EAF1F5');cell.set_text_props(weight='bold')
fig.text(.73,.74,'验证证据',fontsize=16,weight='bold',color=BLUE)
fig.text(.73,.54,f"网格单元：{m['mesh_cells']}\n最终网格 ΔS：{m['last_delta_S']:.2e}\n网格自适应：已收敛\n宽带扫频：已收敛\n求解器错误：0",fontsize=12,linespacing=2)
selection=json.loads((ROOT/'final_selection.json').read_text());dc=max(z['difference_percentage_points'] for z in selection['refinement_checks'])
fig.text(.73,.32,f"独立数值稳定性复核\n12.23 GHz：178,365 单元\n40 GHz：319,913 单元\n两处最大差异 {dc:.3f} 个百分点\n均高于 90%（关键点检查）",fontsize=10.5,color=GRAY,linespacing=1.8)
fig.text(.06,.115,'相对带宽按端点统一重算：论文实验约 61.33%，原 C06 验证区间约 113.63%，本次 5–40 GHz 为 155.56%。',fontsize=10,color=GRAY)
fig.text(.06,.065,'原 C06 的 26 GHz 为扫描上限；本次 5 和 40 GHz 为验证区间边界，未宣称为物理吸收带的真实截止频率。',fontsize=10,color=GRAY)
fig.text(.06,.025,'参考：Ding et al., Applied Physics Letters 100, 103506 (2012), doi:10.1063/1.3692178（用户提供 PDF）。',fontsize=10,color=GRAY)
fig.savefig(OUT/'04_comparison_validation.png',dpi=185);plt.close(fig)
print('final images generated',m['full_5_40_pass'])

