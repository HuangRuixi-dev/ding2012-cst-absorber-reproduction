"""Plot recorded discrete simulations, with linear interpolation only.

No rational-fit data are used for the new absorption curves. The interrupted
broadband fit is shown only in the explicitly labelled 43 GHz comparison.
"""
from pathlib import Path
import csv
import json
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / 'cases'
REFINED_MIDDLE = '--mid5GHz' in sys.argv
OUT = BASE / 'figures'
OUT.mkdir(exist_ok=True)
LEFT = 'FR4_80layer_left_mesh_check_screen'
RIGHT = 'FR4_80layer_right_mesh_check_screen'
MID = 'FR4_80layer_quick_boundary_screen'
CHECK43 = 'FR4_80layer_43GHz_direct_screen'
CASES = [LEFT, RIGHT, MID, CHECK43]
MID_GROUPS = ['FR4_80layer_mid%d_%d_5GHz_screen' % bounds
              for bounds in [(15,30), (35,50), (55,70)]]
EXTRA75 = 'FR4_80layer_75GHz_refined_screen'
if REFINED_MIDDLE:
    CASES += MID_GROUPS + [EXTRA75]
data = {n: np.atleast_1d(np.genfromtxt(ROOT / n / 'spectrum.csv', delimiter=',', names=True))
        for n in CASES}
metrics = {n: json.loads((ROOT / n / 'metrics.json').read_text()) for n in CASES}

# Sources are selected by frequency interval, never by which gives a better A.
# Retain one row per frequency; no mesh results are averaged together.
rows = []
selections = [
    (LEFT, data[LEFT]['frequency_GHz'] <= 15),
    (MID, (data[MID]['frequency_GHz'] > 15) & (data[MID]['frequency_GHz'] < 40)),
    (CHECK43, np.ones(len(data[CHECK43]), dtype=bool)),
    (MID, (data[MID]['frequency_GHz'] > 45) & (data[MID]['frequency_GHz'] < 74)),
    (RIGHT, np.ones(len(data[RIGHT]), dtype=bool)),
    (MID, data[MID]['frequency_GHz'] > 82),
]
if REFINED_MIDDLE:
    selections = [
        (LEFT, data[LEFT]['frequency_GHz'] < 15),
        *[(name, np.ones(len(data[name]), dtype=bool)) for name in MID_GROUPS],
        # Preserve the local 43 GHz results verbatim, replacing 40 and 45 GHz
        # with the newly requested five-GHz-grid simulations.
        (CHECK43, (data[CHECK43]['frequency_GHz'] > 40) & (data[CHECK43]['frequency_GHz'] < 45)),
        (RIGHT, np.ones(len(data[RIGHT]), dtype=bool)),
        (EXTRA75, np.ones(len(data[EXTRA75]), dtype=bool)),
        (MID, data[MID]['frequency_GHz'] > 82),
    ]
for name, mask in selections:
    for row in data[name][mask]:
        rows.append((float(row['frequency_GHz']), name, row))
rows.sort(key=lambda row: row[0])
f = np.array([row[0] for row in rows])
assert np.all(np.diff(f) > 0)
values = {key: np.array([row[2][key] for row in rows]) for key in data[MID].dtype.names}
A = values['A']
assert np.allclose(A + values['R'] + values['T'], 1, atol=1e-10)

def bands(freq, absorption):
    transitions = np.diff(np.r_[False, absorption >= .9, False].astype(int))
    results = []
    for start, end in zip(np.where(transitions == 1)[0], np.where(transitions == -1)[0] - 1):
        lo = freq[start] if start == 0 else np.interp(.9, absorption[start-1:start+1], freq[start-1:start+1])
        hi = freq[end] if end == len(freq)-1 else np.interp(.9, absorption[end:end+2][::-1], freq[end:end+2][::-1])
        results.append(dict(lower_GHz=float(lo), upper_GHz=float(hi),
                            lower_bracket_GHz=None if start == 0 else list(map(float, freq[start-1:start+1])),
                            upper_bracket_GHz=None if end == len(freq)-1 else list(map(float, freq[end:end+2])),
                            lower_censored=bool(start == 0), upper_censored=bool(end == len(freq)-1),
                            FBW_percent=float(200*(hi-lo)/(hi+lo))))
    return results

band_results = bands(f, A)
assert band_results
main = max(band_results, key=lambda band: band['upper_GHz']-band['lower_GHz'])
lo, hi = main['lower_GHz'], main['upper_GHz']
assert not main['lower_censored'] and not main['upper_censored']
blue, red, green, grey = '#176D96', '#C65F48', '#258A71', '#7D8A96'
plt.rcParams.update({'font.family':'Microsoft YaHei', 'font.size':13,
                     'axes.labelsize':15, 'axes.unicode_minus':False,
                     'axes.spines.top':False, 'axes.spines.right':False,
                     'svg.fonttype':'path'})

def canvas(title, ylabel='吸收率 / %', ylim=(0,104)):
    fig, ax = plt.subplots(figsize=(11,6.2))
    fig.subplots_adjust(left=.10, right=.97, top=.87, bottom=.22)
    ax.set(xlabel='频率 / GHz', ylabel=ylabel, ylim=ylim)
    ax.grid(alpha=.16)
    ax.set_title(title, pad=18, fontsize=20)
    return fig, ax

def save(fig, name, caption):
    fig.text(.10,.085,caption,fontsize=10,color='#435B69')
    fig.text(.10,.035,'80 层，H=20 mm；FR4 εr=4.4、tanδ=0.02；铜 σ=5×10⁷ S/m；离散频点线性插值初估。',fontsize=10,color='#435B69')
    for ext in ('png','svg'):
        fig.savefig(OUT / (name+'.'+ext), dpi=300, facecolor='white')
    plt.close(fig)

overviews = [
    ('01_absorption_1_60', (1,60), '80 层 FR4：1–60 GHz 吸收率'),
    ('02_absorption_90pct_band', (1,100), '80 层 FR4：90% 吸收边界初估')
]
if REFINED_MIDDLE:
    overviews[1] = ('02_absorption_1_80', (1,80), '80 层 FR4：1–80 GHz 吸收率')
for name, xlim, title in overviews:
    fig, ax = canvas(title)
    ax.axvspan(5,40,color=green,alpha=.07,label='目标频段 5–40 GHz')
    ax.plot(f,100*A,'o-',ms=3.3,lw=2,color=blue,label='实际求解点及线性插值')
    ax.axhline(90,color=red,ls='--',lw=1.5,label='90% 阈值')
    ax.set_xlim(*xlim)
    for x, label, shift in [(lo,'左边界',(6,-30)),(hi,'右边界',(-20,-30))]:
        if x <= xlim[1]:
            ax.scatter([x],[90],s=52,color=red,zorder=5)
            ax.axvline(x,color=red,ls=':',alpha=.55)
            ax.annotate(f'{label} ≈ {x:.2f} GHz',xy=(x,90),xytext=(x+shift[0],90+shift[1]),
                        arrowprops=dict(arrowstyle='->',color=red),fontsize=13,color=red)
    ax.legend(loc='lower right',frameon=False,fontsize=11)
    caption = (f'主吸收带初估 {lo:.2f}–{hi:.2f} GHz；FBW ≈ {main["FBW_percent"]:.2f}%。'
               + ('中间每 5 GHz 加密网格复算，保留 43 GHz 局部频点；线性插值。' if REFINED_MIDDLE else
                  '分段网格，未完成全带连续验证；当前结构不覆盖 5 GHz。'))
    save(fig,name,caption)

fig, ax = canvas('左侧 90% 边界：网格加密后直接求解')
left = data[LEFT]
coarse = data[MID]
ax.plot(coarse['frequency_GHz'],coarse['A']*100,'o--',color=grey,lw=1.3,ms=4,label='此前高频初始网格结果')
ax.plot(left['frequency_GHz'],left['A']*100,'o-',color=blue,lw=2,ms=5,label='左边界专用自适应网格')
ax.axhline(90,color=red,ls='--',lw=1.5)
ax.scatter([lo],[90],s=55,color=red,zorder=5)
ax.annotate(f'fL ≈ {lo:.3f} GHz',xy=(lo,90),xytext=(8.1,70),
            arrowprops=dict(arrowstyle='->',color=red),color=red,fontsize=16)
ax.set_xlim(5,13)
ax.legend(loc='upper left',frameon=False,fontsize=11)
lm=metrics[LEFT]
save(fig,'03_left_boundary',f'加密网格 {lm["mesh_cells"]:,} 单元，最终 ΔS={lm["last_delta_S"]:.5f}；交点由 {main["lower_bracket_GHz"]} GHz 两点线性插值。')

fig, ax = canvas('右侧 90% 边界：局部网格复核',ylim=(82,98))
right=data[RIGHT]
ax.plot(coarse['frequency_GHz'],100*coarse['A'],'o--',ms=4,color=grey,lw=1.3,label='此前初始网格')
ax.plot(right['frequency_GHz'],100*right['A'],'o-',ms=5,color=blue,lw=2,label='右边界局部加密网格')
ax.axhline(90,color=red,ls='--',lw=1.5)
ax.scatter([hi],[90],s=55,color=red,zorder=5)
ax.annotate(f'fH ≈ {hi:.3f} GHz',xy=(hi,90),xytext=(74.5,85),
            arrowprops=dict(arrowstyle='->',color=red),color=red,fontsize=16)
ax.set_xlim(73.5,82.5)
ax.legend(loc='upper right',frameon=False,fontsize=11)
rm=metrics[RIGHT]
status='达到设定停止阈值' if rm['mesh_converged'] else '达到最大加密轮次，尚未达到设定停止阈值'
save(fig,'04_right_boundary',f'{rm["mesh_cells"]:,} 单元，最终 ΔS={rm["last_delta_S"]:.5f}；{status}。')

# Show the rejected interrupted fit only in this audit comparison.
old=np.genfromtxt(BASE/'data/legacy_fit_curve.csv',delimiter=',',names=True)
near=(old['frequency_GHz']>=40)&(old['frequency_GHz']<=45)
direct=data[CHECK43]
fig,ax=canvas('43 GHz 附近：直接求解替换未收敛拟合',ylim=(55,102))
ax.plot(old['frequency_GHz'][near],100*old['A_preliminary'][near],'--',color=grey,lw=1.5,label='旧拟合（中止、未收敛）')
ax.plot(direct['frequency_GHz'],100*direct['A'],'o-',color=blue,lw=2,ms=4,label='新直接求解点及线性插值')
ax.axhline(90,color=red,ls='--',lw=1.3)
ax.set_xlim(40,45)
ax.legend(loc='lower left',frameon=False,fontsize=11)
idx=int(np.argmin(abs(direct['frequency_GHz']-43.6)))
save(fig,'05_43GHz_recheck',f'43.6 GHz 新直接求解 A={100*direct["A"][idx]:.2f}%；此段采用初始网格，按用户要求未继续加密。')

fig,ax=canvas('反射频谱：总反射与同极化 S11',ylabel='反射 / dB',ylim=(-35,2))
ax.plot(f,10*np.log10(np.maximum(values['R'],1e-30)),'o-',ms=3,color=blue,lw=2,label=r'总反射 $10\log_{10}R$（全部传播模态）')
ax.plot(f,values['S11_dB'],'--',color=grey,lw=1.4,label='同极化 S11')
ax.axhline(-10,color=red,ls='--',lw=1.2,label='总反射 −10 dB 参考线')
ax.set_xlim(1,80 if REFINED_MIDDLE else 100)
ax.legend(loc='lower left',frameon=False,fontsize=10)
save(fig,'06_reflection','吸收率按 A=1−R−T 核算；高频同极化 S11 不能单独替代总反射功率。')

with (BASE/'data/merged_discrete_spectrum.csv').open('w',newline='',encoding='utf-8-sig') as stream:
    writer=csv.writer(stream)
    keys=list(data[MID].dtype.names)
    writer.writerow(keys+['source_case'])
    for _,name,row in rows:
        writer.writerow([float(row[k]) for k in keys]+[name])
summary=dict(main_sampled_band=main,all_sampled_bands=band_results,
             note='Piecewise linear interpolation of discrete results; not proof of continuous-band convergence.',
             target_5_40_pass=False,source_metrics=metrics)
if REFINED_MIDDLE:
    summary['refined_middle_frequencies_GHz'] = list(range(15,76,5))
    summary['preserved_43GHz_frequencies_GHz'] = [float(x) for x in data[CHECK43]['frequency_GHz'] if 40 < x < 45]
    original = np.genfromtxt(BASE/'data/previous_merged_spectrum.csv',
                             delimiter=',',names=True,encoding='utf-8-sig',usecols=range(8))
    for row in original:
        frequency=float(row['frequency_GHz'])
        if 40 < frequency < 45:
            target = np.where(np.isclose(f,frequency,rtol=0,atol=1e-9))[0]
            assert len(target)==1 and abs(A[target[0]]-row['A']) < 1e-12
    # A separate table makes the requested newly solved points easy to review.
    with (BASE/'data/middle_5GHz_refinement.csv').open('w',newline='',encoding='utf-8-sig') as stream:
        writer=csv.writer(stream)
        writer.writerow(['frequency_GHz','A_percent','R_percent','mesh_cells','last_delta_S','mesh_converged','source_case'])
        for name in MID_GROUPS + [EXTRA75]:
            for row in data[name]:
                writer.writerow([float(row['frequency_GHz']),100*float(row['A']),100*float(row['R']),
                                 metrics[name]['mesh_cells'],metrics[name]['last_delta_S'],metrics[name]['mesh_converged'],name])
(BASE/'data/boundary_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
(BASE/'data/plot_notes.txt').write_text(
    '当前材料是论文 FR4 参数近似，不是 εr=22、tanδ=0.18 的旧设计介质。\n'
    '结构为原80层、H=20mm、Wb=6.9mm、Wt=0.65mm、周期7.2mm、对数轮廓。\n'
    '全部曲线采用实际离散频点线性连接，旧未收敛扫频仅用于43GHz对比图。\n'
    '左右边界由相邻实际频点夹逼后插值，网格状态见boundary_summary.json。\n'
    '不同频段采用不同网格；边界和带宽属于初估，不能作为连续频段全网格收敛认证。\n'
    '当前FR4结构不满足5–40GHz连续90%吸收要求。\n',encoding='utf-8')
print(json.dumps(dict(output=str(OUT),main_band=main),ensure_ascii=False,indent=2))
