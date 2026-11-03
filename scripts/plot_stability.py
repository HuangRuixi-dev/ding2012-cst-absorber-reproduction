from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(r'C:\Users\huzst\Desktop\senior\metamaterial\ding2012-cst-absorber-reproduction-main\course_design_absorber\pyramid_optimization_5_40GHz');F=ROOT/'P05_loss18_full';C=ROOT/'P06_critical_stability_screen';s=json.loads((C/'adaptive_stability.json').read_text());e=json.loads((ROOT/'stability_40GHz/endpoint_40GHz.json').read_text());m=json.loads((F/'metrics.json').read_text());sel=json.loads((ROOT/'final_selection.json').read_text())
plt.rcParams.update({'font.family':'Microsoft YaHei','axes.unicode_minus':False,'font.size':12,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(1,2,figsize=(14,8));fig.subplots_adjust(top=.76,bottom=.42,left=.08,right=.95,wspace=.28)
axs[0].plot(np.array(s['mesh_cells_by_pass'])/1e4,np.array(s['A_by_pass'])*100,'o-',color='#176D96',label='本频点独立自适应（50 模式）');axs[0].axhline(m['min_A']*100,color='#C7774C',ls='--',label='完整扫频模型（18 模式）');axs[0].set(xlabel='网格单元数 / 万',ylabel='12.23 GHz 吸收率 / %',title='最薄弱点：同频率下比较网格');axs[0].grid(alpha=.18);axs[0].legend(fontsize=9,frameon=False)
axs[1].plot(e['passes'],np.array(e['A'])*100,'o-',color='#176D96',label='40 GHz 自适应序列（50 模式）');axs[1].axhline(m['at_40'][0]*100,color='#C7774C',ls='--',label='完整扫频模型（18 模式）');axs[1].set(xlabel='网格自适应轮次',ylabel='40 GHz 吸收率 / %',title='高频端：加密结果趋于稳定');axs[1].grid(alpha=.18);axs[1].legend(fontsize=9,frameon=False)
fig.text(.06,.945,'数值稳定性复核：比较的是同一频率的粗、细网格结果',fontsize=22,weight='bold',color='#17384D')
fig.text(.06,.87,'12.23 GHz 与 40 GHz 分别检查；并非把两个不同频率的吸收率互相比较。两处加密计算均收敛。',fontsize=11,color='#62727F')
ax=fig.add_axes([.08,.18,.87,.15]);ax.axis('off');rows=[]
for z in sel['refinement_checks']:rows.append([f"{z['frequency_GHz']:.2f}",f"{z['baseline_mesh_cells']:,}",f"{z['refined_mesh_cells']:,}",f"{z['baseline_A']*100:.3f}%",f"{z['refined_A']*100:.3f}%",f"{z['difference_percentage_points']:.3f}"])
t=ax.table(cellText=rows,colLabels=['频率 / GHz','完整扫频网格','加密网格','完整扫频 A','加密 A','差异 / 百分点'],loc='center',cellLoc='center');t.auto_set_font_size(False);t.set_fontsize(10.5);t.scale(1,2.1)
for (r,c),cell in t.get_celld().items():
 cell.set_edgecolor('#D8E0E5')
 if r==0:cell.set_facecolor('#EAF1F5');cell.set_text_props(weight='bold')
fig.text(.06,.095,'结果：两处吸收率差异均小于 0.1 个百分点，且加密结果均超过 90%。',fontsize=13,color='#27846C',weight='bold')
fig.text(.06,.04,'范围：这是关键频点的网格/模态稳定性检查；完整连续 5–40 GHz 性能来自 94,003 单元的已收敛宽带模型。',fontsize=10,color='#62727F')
fig.savefig(ROOT/'figures/05_numerical_stability.png',dpi=185);plt.close(fig);print('stability figure saved')
