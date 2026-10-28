from pathlib import Path
import json,hashlib,shutil,datetime
R=Path(__file__).resolve().parents[1]
final=json.loads((R/'data/final_selection.json').read_text());m=final['metrics'];p=m['parameters'];b=m['best'];guard=final.get('reporting_guardband',b)
if not m['passes_spec'] or not p['strict']:raise RuntimeError('Final result is not validated')
for part in ['report','slides','study_notes']:
 if not (R/part/'main.pdf').exists():raise RuntimeError('Missing PDF '+part)
sources=[R.parent/'课程建模大作业.pptx',R.parent/'第4组 复现图2图3.pdf',R.parent/'cst/Ding2012_20layer.cst',R.parent/'data/spectrum.csv']
def sha(f):
 h=hashlib.sha256()
 with f.open('rb') as fp:
  for chunk in iter(lambda:fp.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
manifest={'created':datetime.datetime.now().isoformat(),'source_hashes':{str(f.relative_to(R.parent)):sha(f) for f in sources},'final_case':final['case'],'nominal_case':final['nominal'],'deliverables':{str(f.relative_to(R)):sha(f) for f in [R/'report/main.pdf',R/'slides/main.pdf',R/'study_notes/main.pdf',R/'runs'/final['case']/'absorber.cst']}}
previous_manifest_path=R/'data/manifest.json'
if previous_manifest_path.exists():
 previous_manifest=json.loads(previous_manifest_path.read_text(encoding='utf-8-sig'))
 for key in ['audit_history','organization_history']:
  if key in previous_manifest:manifest[key]=previous_manifest[key]
(R/'data/manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
text=f'''# 课程建模大作业：第四题超宽带吸波器

本目录保存本次课程设计，与上级原始论文复现区分。旧版误做的 `group4_latex_20261023` 已移至 `../_archive/20261026/旧版误做的论文复现/`。任务依据为 `requirements/课程建模大作业.pptx` 第 4 页；不是重复复现论文图 2、图 3。

**最终 CST 只打开 [runs/{final['case']}/absorber.cst](runs/{final['case']}/absorber.cst)**；其余工程的用途见 [CST 工程用途说明](runs/00_CST工程用途说明.md)。复制或提交时保留整个 C06 案例文件夹。

## 阅读与提交

- `report/main.pdf`：中文研究报告，源码为同目录 `main.tex` 及被包含的 `.tex` 文件。
- `slides/main.pdf`：中文 LaTeX Beamer 汇报，可全屏播放；源码 `slides/main.tex`。按用户要求采用 LaTeX，没有转为 PPTX。
- `runs/{final['case']}/absorber.cst`：最终加严验证模型，须连同旁边同名 `absorber/` 结果目录保存。
- `study_notes/main.pdf`：独立个人学习笔记，解释优化方法与后续建议，不必作为正式报告提交。

## 已验证结果

P={p['period']:g} mm，底宽/顶宽={p['bottom']:g}/{p['top']:g} mm，N={p['layers']}，堆叠高度={p['height']:g} mm，介质厚 0.20 mm，铜厚 0.05 mm，背板 0.05 mm。介质 εr=4.4，tanδ={p['loss']:g}，铜电导率 5×10⁷ S/m。

正式验收使用保守内部频段 {guard['lower_GHz']:.1f}–{guard['upper_GHz']:.1f} GHz，相对带宽 {guard['RAB_percent']:.2f}%。原始插值阈值区间约 {b['lower_GHz']:.6f}–{b['upper_GHz']:.1f} GHz，对应估计带宽 {b['RAB_percent']:.2f}%；低端交点是 A=0.9 的等号位置。26 GHz 是扫描上限，未定位真实高频截止，未宣称整个 5–40 GHz 都达标。

材料为常参数设计有损介质，不是已测量的 FR4；未加工样品或开展自由空间实测。结果对应正入射无限周期阵列。没有用基模反射代替总反射，没有跨凹谷拼接带宽。

## 数据与案例

`data/summary.json` 汇总完成案例，`data/final_selection.json` 指明最终设计与标称网格对应关系。各运行目录含参数、几何 VBA、原生日志、复数 S 参数、功率谱与指标。接口调试失败或只有预设参数的目录未被当作完成案例。

- C01d_wide40：40 层、宽度扩展、tanδ=0.02。
- C02_loss06、C03_loss04：固定几何的损耗对照。
- {final['nominal']}：最终参数的标称计算。
- C05_loss12_refined：线性求解与扫频精度复核；网格停止条件未按预期加严，不作为最终网格验证。
- {final['case']}：最终参数的加严网格与扫频复核。

已有 20 层基准只使用上级已有的 6–15 GHz 数据，没有在本次重复其复现。新优化统一扫描 5–26 GHz，低于 P=11 mm 的正入射首阶衍射阈值约 27.25 GHz。扩展到 40 GHz 需增加高阶 Floquet 模式并检查模式数收敛。

## 重建与处理

在项目根目录运行，例如 `python group4_course_design_20261024/scripts/make_case.py 新案例名 --loss 0.12`，再运行 `group4_course_design_20261024/scripts/build_solve.ps1 -CaseName 新案例名`。生成器拒绝覆盖已有目录，建模脚本拒绝覆盖已有工程。CST 使用本机 2023 安装与官方批处理入口。

原生数据导出通过本机 CST 技能启动器运行 `scripts/export_case.py 案例名`，随后运行 `scripts/evaluate.py`。最终文稿和图表由 `scripts/write_results.py`、`scripts/plot_figures.py` 根据汇总数据更新。`scripts/build_documents.ps1` 以 XeLaTeX 编译三份文档，各两遍。三份文档的来源保持可编辑，图表 PDF 由实际 CSV 数据生成。

`data/manifest.json` 记录源文件与主要交付物 SHA-256。2026-10-26 已清除 `qa/` 排版截图、LaTeX 编译辅助文件和 Python 字节码；再次构建时可重新生成。失败或未运行试算已移至 `../_archive/20261026/失败及未运行试算/`；六个有效案例及其完整 CST 结果仍在 `runs/`。原始复现和正式文稿未改动。日志中内存分配代理的性能警告不等于求解失败；最终性能需要同时查看退出码、网格与扫频收敛。
'''
(R/'README_交付说明.md').write_text(text,encoding='utf-8')
print('Manifest and delivery guide written')
