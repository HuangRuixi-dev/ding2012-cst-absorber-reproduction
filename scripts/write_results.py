from pathlib import Path
import json,re
import numpy as np
R=Path(__file__).resolve().parents[1]
summary=json.loads((R/'data/summary.json').read_text())
valid=[m for m in summary if m['passes_spec'] and m['parameters']['strict'] and float(m['last_mesh_delta'])<.003]
if not valid:raise RuntimeError('No passing case with stricter mesh verification; do not create a final claim.')
winner=max(valid,key=lambda m:m['best']['RAB_percent']);w=winner['best'];p=winner['parameters']
nominal=sorted([m for m in summary if not m['parameters']['strict']],key=lambda m:m['parameters']['loss'])
match=[m for m in nominal if all(m['parameters'][k]==p[k] for k in ['layers','height','bottom','top','loss','period','law'])]
if not match:raise RuntimeError('Missing nominal case for convergence comparison')
n=match[0];a=np.loadtxt(R/'runs'/winner['case']/'spectrum.csv',delimiter=',',skiprows=1);b=np.loadtxt(R/'runs'/n['case']/'spectrum.csv',delimiter=',',skiprows=1)
diff=float(np.max(abs(a[:,1]-np.interp(a[:,0],b[:,0],b[:,1]))))
fL,fU,B=w['lower_GHz'],w['upper_GHz'],w['RAB_percent'];flag='（扫描上限截断）' if w['right_censored'] else ''
guardL=float(np.ceil((fL+.1)*10)/10);guardU=float(np.floor(fU*10)/10)
g=a[(a[:,0]>=guardL)&(a[:,0]<=guardU)]
gf=np.r_[guardL,a[(a[:,0]>guardL)&(a[:,0]<guardU),0],guardU]
ga=np.interp(gf,a[:,0],a[:,1])
guardB=200*(guardU-guardL)/(guardU+guardL);guardMin=float(ga.min());guardMean=float(np.trapezoid(ga,gf)/(guardU-guardL));guardS11=float(g[:,5].max())
def wr(rel,s):(R/rel).write_text(s,encoding='utf-8')
rows=[]
for m in nominal+[winner]:
 q=m['best'];kind='加严网格' if m['parameters']['strict'] else '标称'
 rows.append(f"{m['parameters']['loss']:g}（{kind}） & {q['lower_GHz']:.3f}--{q['upper_GHz']:.3f} & {q['RAB_percent']:.2f} & "+('达标' if m['passes_spec'] else '未达标')+r'\\')
wr('report/abstract.tex',r'\begin{abstract}'+'本设计以 Ding 等的渐变金属介质方台为结构基础，扩大宽度范围至 10--2.5 mm，增加至 40 层、高度 10 mm，再固定几何扫描介质损耗。'+f"最终采用常参数介质 $\\varepsilon_r=4.4$、$\\tan\\delta={p['loss']:g}$。在该材料模型与正入射条件下，CST 加严网格结果的保守验收频段为 {guardL:.1f}--{guardU:.1f} GHz，带内导出样点最低吸收率 {100*guardMin:.2f}\\%，相对带宽 {guardB:.2f}\\%。"+'这在所用数值精度内满足连续吸收和带宽要求，未将完整 5--40 GHz 视为达标。结果按总反射与透射功率计算，不跨越凹谷；高端为扫描上限。文中区分已有基准、本次计算、文献结果与设计假设。本工作未表征材料或开展样品实测。'+r'\end{abstract}')
wr('report/results.tex',r'''\section{参数扫描与性能结果}
\begin{figure}[H]\centering\includegraphics[width=.87\linewidth]{geometry.pdf}\caption{由实际几何参数绘制的截面与宽度分布。左侧金色为铜，紫色为有损介质；右侧比较已有基准与优化几何。此图为模型示意，不是样品照片。}\end{figure}
已有基准的连续高吸收区间为 8.196--12.967 GHz，相对带宽 45.08\%，不能满足本课程指标。首轮采用 40 层、大宽度范围及原损耗 0.02，主带扩至 7.284--15.348 GHz，相对带宽 71.26\%，但中高频凹谷仍打断频带。把损耗增至 0.06 后，许多高频凹谷抬升，约 16.2 GHz 的缺口仍保留。因此继续扫描损耗，而没有把两个分离区间合并报告。
\begin{table}[H]\centering\caption{完成求解的参数组合。几何为 $P=11$ mm、$W_l=10$ mm、$W_t=2.5$ mm、40 层、高度 10 mm。边界是 $A=0.9$ 交点估计；右端触及 26 GHz 时为扫描截断。最终验收另用保守内部频段。}
\begin{tabular}{lccc}\toprule 损耗与计算 & 阈值区间估计 / GHz & 相对带宽 / \% & 指标\\\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule\end{tabular}\end{table}
\begin{figure}[H]\centering\includegraphics[width=.98\linewidth]{optimization_spectra.pdf}\caption{已有基准与实际优化谱线。虚线为 90\% 阈值，各曲线直接来自导出数据；没有平滑消除凹谷。}\end{figure}
\begin{figure}[H]\centering\includegraphics[width=.98\linewidth]{dip_detail.pdf}\caption{中高频缺口的局部对照。损耗扫描显示凹谷抬升，但没有给出独立模态或损耗分解，不能据此确认具体的峰展宽和阻抗匹配机理。}\end{figure}
\subsection{最终设计与网格复核}
'''+f"最终选择 $\\tan\\delta={p['loss']:g}$，堆叠高度 {p['height']:g} mm，含背板总厚度 {p['height']+.05:g} mm。加严计算的线性求解精度为 $10^{{-5}}$，网格阈值 0.003、扫频阈值 0.001。最终网格 {int(winner['mesh_cells']):,} 个四面体，最后网格差 {winner['last_mesh_delta']}，日志记录 33 个扫频频率样本并满足设置的准则，退出码 0。相对标称网格，全扫描吸收率最大绝对差为 {diff:.4f}。"+'\n\n'+f"低端 $A=0.9$ 交点估计为 {fL:.6f} GHz；从该交点至 {fU:.1f} GHz 的相对带宽估计为 {B:.2f}\\%。交点本身对应等号，不能把向下取整的端点直接作为严格 $A>0.9$ 闭区间的证明。"+('26 GHz 为扫描上限，未定位真实高频截止。' if w['right_censored'] else '')+f"最大交叉反射功率为 {winner['max_cross_reflection']:.3g}，透射在数值上可忽略；极小透射值不代表同等数量级的物理预测精度。"+r'''
\input{guardband}
\begin{figure}[H]\centering\includegraphics[width=.98\linewidth]{final_performance.pdf}\caption{最终设计的加严网格结果。阴影为保守验收频段 7.3--26 GHz；右端是扫描上限。谱线包含扫频插值，不表示对所有实频率的解析证明。}\end{figure}
''')
wr('report/guardband.tex',f"正式验收采用保守内部频段 {guardL:.1f}--{guardU:.1f} GHz，相对带宽 {guardB:.2f}\\%。在导出样点和当前数值精度内，最低吸收率 {100*guardMin:.2f}\\%，最大同偏振 $S_{{11}}$ 为 {guardS11:.2f} dB；按频率积分的平均吸收率约 {100*guardMean:.2f}\\%。含背板厚度与该频段低端自由空间波长之比约 {(p['height']+.05)*guardL/299.792458:.3f}，未开展制造容差统计。\n")
wr('report/comparison_row.tex',r'\newcommand{\FinalComparisonRow}{'+f"本设计（保守） & {guardL:.1f}--{guardU:.1f} GHz & {guardB:.2f} & {p['height']+.05:g} & 本次数值设计"+r'\\}'+'\n')
con=f"在常参数介质 $\\varepsilon_r=4.4$、$\\tan\\delta={p['loss']:g}$ 及正入射条件下，本设计的保守验收频段为 {guardL:.1f}--{guardU:.1f} GHz，最低导出样点吸收率 {100*guardMin:.2f}\\%，相对带宽 {guardB:.2f}\\%。该结论以已扫描范围和数值精度为限，不表示完整 5--40 GHz 覆盖或已实现的 FR4 样品性能。厚度增加与高损耗材料是假设和代价；模态归因、材料表征、端口截断、有限阵列及角度性能仍需进一步验证。"
wr('report/conclusion.tex',r'\section{结论}'+'\n'+con+'\n')
wr('slides/result_frames.tex',r'''\begin{frame}{实际参数扫描}
\centering\small\begin{tabular}{lccc}\toprule 损耗与计算 & 阈值区间估计 / GHz & 相对带宽 / \% & 指标\\\midrule
'''+ '\n'.join(rows)+r'''
\bottomrule\end{tabular}
\vspace{4mm}\par 边界为90\%阈值估计，26 GHz为扫描截断。最终验收另取7.3--26 GHz。\par 已有基准仅有6--15 GHz数据；其所报连续带宽45.08\%。
\end{frame}
\begin{frame}{宽度范围扩展与损耗扫描}
\centering\includegraphics[width=.98\linewidth,height=.79\textheight,keepaspectratio]{optimization_spectra.pdf}
\end{frame}
\begin{frame}{限制带宽的吸收凹谷}
\centering\includegraphics[width=.98\linewidth,height=.73\textheight,keepaspectratio]{dip_detail.pdf}
\par\small 低于 90\% 的凹谷会切断频带；平均吸收高也不能替代连续带宽。
\end{frame}
\begin{frame}{最终设计的数值性能}
\centering\includegraphics[width=.98\linewidth,height=.8\textheight,keepaspectratio]{final_performance.pdf}
\end{frame}
\begin{frame}{加严网格复核}
\begin{itemize}
'''+f"\\item 线性求解精度 $10^{{-5}}$；网格阈值 0.003；扫频阈值 0.001。\n\\item 最终 {int(winner['mesh_cells']):,} 个四面体，最后网格差 {winner['last_mesh_delta']}。\n\\item 全扫描范围吸收率与标称网格最大差 {diff:.4f}。\n\\item 日志记录33个扫频频率样本；2601个输出位置含插值。\n\\item 保守 {guardL:.1f}--{guardU:.1f} GHz，最低样点吸收 {100*guardMin:.2f}\\%，带宽 {guardB:.2f}\\%。\n"+r'''\end{itemize}
\vspace{3mm}\small 插值阈值区间约7.160--26 GHz、113.63\%；26 GHz为扫描上限。
\end{frame}
\begin{frame}{与已发表工作的比较}
\small\centering\begin{tabular}{lccc}\toprule 来源 & 90\% 吸收频带 / GHz & 相对带宽 / \% & 高度 / mm\\\midrule
Ding 2012 仿真 & 原文报告 & 53.1 & 5\\
Zhang 2025 仿真 & 4.4--60 & 173 & 9.7\\
'''+f"本设计保守频段 & {guardL:.1f}--{guardU:.1f} & {guardB:.2f} & {p['height']+.05:g}"+r'''\\\bottomrule\end{tabular}
\vspace{4mm}\par\small Ding 为堆叠高度；本设计含背板。Zhang 的60 GHz亦为扫描上限。\par\vspace{3mm}\footnotesize 文献 DOI：10.1063/1.3692178；10.1038/s41598-025-97277-9。
\end{frame}
''')
wr('slides/conclusion_frame.tex',r'\begin{frame}{结论}'+'\n'+f"保守验收频段\\par\\bigskip\n{{\\Large\\color{{navy}}{guardL:.1f}--{guardU:.1f} GHz，{guardB:.2f}\\%}}\\par\\bigskip\n最低导出样点吸收率 {100*guardMin:.2f}\\%，在当前数值精度内满足指标。\\par\\bigskip\n"+r'''条件：正入射，常参数介质 $\varepsilon_r=4.4$、$\tan\delta=0.12$。\par\medskip
未证明完整5--40 GHz覆盖、真实材料或样品性能。
\end{frame}
''')
wr('data/final_selection.json',json.dumps({'case':winner['case'],'nominal':n['case'],'max_absorption_difference':diff,'reporting_guardband':{'lower_GHz':guardL,'upper_GHz':guardU,'RAB_percent':guardB,'minimum_A':guardMin,'frequency_average_A':guardMean,'max_copolar_S11_dB':guardS11},'metrics':winner},indent=2))
print(winner['case'],fL,fU,B,'documents populated')
