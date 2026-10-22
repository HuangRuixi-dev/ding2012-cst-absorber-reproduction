from pathlib import Path
import json,re,shutil,os
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER
root=Path(__file__).resolve().parent;run=Path(os.environ.get('CST_REPRO_RUN',str(root/'tasks/ding2012/runs/run_001')));a=run/'analysis'
m=json.loads((a/'metrics.json').read_text());out=root.parent/'复现结果';out.mkdir(exist_ok=True)
solver_log=(run/'projects'/'Ding2012_20layer'/'Result'/'Model.log').read_text(errors='replace')
mesh_delta=float(re.findall(r'All S-Parameters\s*:\s*([0-9.eE+-]+)',solver_log)[-1])
mesh_cells=int(re.findall(r'Number of mesh cells\s*:\s*(\d+)',solver_log)[-1])
mesh_dof=int(re.findall(r'Degrees of freedom\s*:\s*(\d+)',solver_log)[-1])
pdfmetrics.registerFont(TTFont('CN',r'C:\Windows\Fonts\msyh.ttc',subfontIndex=0))
pdfmetrics.registerFont(TTFont('CNB',r'C:\Windows\Fonts\msyhbd.ttc',subfontIndex=0))
body=ParagraphStyle('body',fontName='CN',fontSize=9.7,leading=16,wordWrap='CJK',spaceAfter=7,textColor=colors.HexColor('#263342'))
heading=ParagraphStyle('heading',parent=body,fontName='CNB',fontSize=14,leading=20,spaceBefore=9,spaceAfter=9,textColor=colors.HexColor('#15395d'))
title=ParagraphStyle('title',parent=heading,fontSize=21,leading=31,spaceAfter=15)
caption=ParagraphStyle('cap',parent=body,fontSize=8.4,leading=13,textColor=colors.HexColor('#536272'))
story=[]
def p(txt,style=body):story.append(Paragraph(txt,style))
def img(name,w,h):story.append(Image(str(a/name),width=w,height=h));story.append(Spacer(1,5))
def table(rows,widths):
 data=[[Paragraph(str(c),caption) for c in row] for row in rows]
 t=Table(data,colWidths=widths,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8f0f6')),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#92aabe')),('BOTTOMPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#dae2e8'))]));story.append(t);story.append(Spacer(1,8))
bands=m['bands_A_ge_0.9'];band=max(bands,key=lambda b:b[1]-b[0])
p('超宽带微波超材料吸波器<br/>图 2、图 3 仿真复现小报告',title)
p('文献：Fei Ding 等，Ultra-broadband microwave metamaterial absorber，Applied Physics Letters 100, 103506 (2012)，DOI: 10.1063/1.3692178。',caption)
p('1　复现范围与模型',heading)
p('采用本机 CST Studio Suite 2023 完成周期单元全波仿真，复现论文图 2 的吸收/反射/透射响应，以及图 3 在 8.3、10、12、14 GHz 的电场和磁场中央截面。图 2(b) 的论文实验曲线仅作为文献对照，不是本次测量结果。')
table([['参数','取值','依据'],['周期 P / 底宽 Wl / 顶宽 Wt','11 / 9 / 5 mm','论文图 1'],['复合层数 / 总高','20 / 5 mm','论文正文和图 1'],['铜厚 / FR4 厚','0.05 / 0.20 mm','每层 0.25 mm'],['铜电导率','5×10⁷ S/m','论文设定'],['FR4 相对介电常数 / 损耗角正切','4.4 / 0.02','论文设定'],['激励与边界','正入射，E 沿 y，x/y 单元周期，z 开放','TE(0,0)，Floquet 端口']], [132,180,189])
img('model_cross_section.png',385,262)
p('图 1　本次 CST 输入尺寸对应的 x=0 截面示意。每层宽度 wi=9-4i/19 mm，i=0,…,19；铜背板厚 0.05 mm。FR4 与铜采用等宽分层阶梯近似，未直接构造论文加工样品的连续斜侧壁。',caption)
story.append(PageBreak())
p('2　图 2：吸收谱与论文对比',heading)
p(f'使用二阶四面体频域求解器，6–15 GHz 扫频，获得 {m["samples"]} 个输出频率点。入射功率归一化后，将两个传播 Floquet 模式的反射、透射功率分别求和，计算 A=1-R-T；本频段高阶衍射模式不传播。')
img('figure2_reproduced.png',497,435)
p('图 2　本次独立 CST 仿真（蓝线）及文献曲线对比。黑色虚线和红线分别由所提供 PDF 的仿真、实验曲线进行图像数字化提取，属于近似参考数据。',caption)
table([['指标','本次结果','论文参考'],['最长连续 A≥90% 频段',f'{band[0]:.3f}–{band[1]:.3f} GHz','仿真范围由原图读取'],['相对吸收带宽 2(fU-fL)/(fU+fL)',f'{band[2]:.2f}%', '仿真 53.1%'],['最大透射功率','&lt; 1e-100','金属背板使其接近 0'],['与论文仿真曲线的全频段 RMSE',f'{m["RMSE_vs_digitized_paper_simulation"]:.4f}','6.1–15 GHz；包含图像提取误差']],[190,150,161])
p(f'本模型在 13–14.2 GHz 出现几处低于 90% 的小凹谷，因此最长连续带宽为 {band[2]:.2f}%，低于论文报告的 53.1%。低频吸收边缘及多峰趋势接近论文，高频连续性尚未完全复现。',caption)
story.append(PageBreak())
p('3　图 3：电场与磁场空间分布',heading)
p('导出 x=0 的 y-z 中央截面复数矢量场，取 |F|=√Σ(|Fi|²)。为比较共振位置，每幅图分别按该截面最大幅值归一化；颜色不代表不同频率之间具有相同绝对场强。白线标示铜层位置。')
img('figure3_reproduced.png',481,524)
p('图 3　从上到下依次为 8.3、10、12、14 GHz；左为 |E|，右为 |H|。所有彩色数据来自本次 CST 场监视器，未将论文场图或理论示意图作为仿真结果。',caption)
story.append(PageBreak())
p('4　机理、验证与复现边界',heading)
fieldH=[x for x in m['fields'] if x['field']=='H']
table([['频率 / GHz','磁场共振位置 z / mm','截面最大 |H| / A·m⁻¹']]+[[str(v['frequency_GHz']),f'{v["dielectric_energy_peak_z_mm"]:.3f}',f'{v["max_amplitude"]:.2f}'] for v in fieldH],[150,175,176])
p('共振位置由介质内部各高度的 |H|² 截面积分峰值确定，尽量排除金属内部和侧边缘尖峰；该数值是本报告新增的定量指标，不是论文原始数据。场图和该指标共同用于检查随频率升高，共振从底部较宽贴片向顶部较窄贴片迁移的趋势。')
p('数值验证',heading)
p(f'首轮网格自适应在 15 GHz 进行了 3 次加密，最后相邻两轮的全部 S 参数差异为 {mesh_delta:.7g}，达到求解器当前阈值。最终网格为 {mesh_cells:,} 个四面体、{mesh_dof:,} 个自由度。该结果属于求解器自适应收敛，不等同于多组独立网格在全频段的严格误差界。')
p('误差来源与说明',heading)
p('① 几何近似：采用分层阶梯单元，论文结构具有加工斜侧壁；贴片边缘与介质轮廓会影响局部电容和共振。② 材料模型：使用论文给定的常数介电参数与表面阻抗铜模型，未拟合实际 FR4 批次色散。③ 文献对照：参考曲线由 PDF 栅格图数字化，含像素误差。④ 实验差别：论文反射实验约为 10° 入射、有限阵列并有加工/装配误差，本次为无限周期正入射模型。因此图 2(b) 不能解释为重新完成了原论文实验。')
p('交付与复算',heading)
p('CST 工程及完整结果位于本次运行指定的 CST_REPRO_RUN 目录中。使用时应保留 .cst 文件旁的同名结果文件夹。exports 包含复数 S 参数和八幅场数据；analysis 包含谱线 CSV、场数组 NPZ、指标 JSON 与图片；stages 保存建模命令，logs 保存求解日志。仿真采用独立 Python 3.9 调用 CST 2023 官方接口。')
p('参考资料',heading)
p('[1] Ding F., Cui Y., Ge X., Jin Y., He S. Applied Physics Letters 100, 103506 (2012). DOI: 10.1063/1.3692178。<br/>[2] 本机 CST 2023 帮助：Python/source/cst.interface.html；Python/source/cst.results.html；VBA_3D/special_vbaports/floquetport_object.htm；VBA_3D/common_vbaimpexp/asciiexport_object.htm。',caption)
def footer(c,doc):
 c.saveState();c.setStrokeColor(colors.HexColor('#c6d4df'));c.line(47,39,548,39);c.setFont('CN',8);c.setFillColor(colors.HexColor('#617080'));c.drawString(47,26,'课程建模作业 · Ding 2012 图 2 / 图 3 复现');c.drawRightString(548,26,str(doc.page));c.restoreState()
pdf=out/'图2图3仿真复现小报告.pdf'
SimpleDocTemplate(str(pdf),pagesize=(595.28,841.89),rightMargin=47,leftMargin=47,topMargin=39,bottomMargin=51,title='图2图3仿真复现小报告',author='课程建模仿真复现').build(story,onFirstPage=footer,onLaterPages=footer)
for name in ['figure2_reproduced.png','figure3_reproduced.png','model_cross_section.png','spectrum.csv','metrics.json']:
 shutil.copy2(a/name,out/name)
(out/'结果说明.txt').write_text('本目录包含报告、复现图和谱线。最终 CST 工程及完整原始结果位于 '+str(run/'projects')+' 。必须保留 .cst 文件旁的同名目录。\n论文实验曲线为图像数字化文献数据，本次没有进行实体实验。\n',encoding='utf-8')
print(pdf)
