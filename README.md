# CST reproduction of Ding et al. (2012), Figures 2 and 3

This project reproduces the absorption spectrum and field-localization trend of the 20-layer microwave metamaterial absorber in Fei Ding et al., “Ultra-broadband microwave metamaterial absorber,” *Applied Physics Letters* **100**, 103506 (2012), DOI: [10.1063/1.3692178](https://doi.org/10.1063/1.3692178).

## Results

- [Short report (Chinese, PDF)](report/图2图3仿真复现小报告.pdf)
- [Figure 2: absorption, reflection, transmission, and paper comparison](figures/figure2_reproduced.png)
- [Figure 3: E/H field magnitude at 8.3, 10, 12, and 14 GHz](figures/figure3_reproduced.png)
- [Model cross-section](figures/model_cross_section.png)
- [Spectrum (CSV)](data/spectrum.csv), [summary metrics (JSON)](data/metrics.json), and [field-magnitude grids (NPZ)](data/fields)

The calculated absorption has a longest continuous `A >= 0.9` band of **8.196–12.967 GHz**, a **45.08% relative bandwidth**. The paper reports **53.1%** for its simulation. The model reproduces the low-frequency onset and the upward migration of the field hot spot, but has several extra dips below 90% at 13–14.2 GHz. The E/H hotspot moves from about **0.5 mm at 8.3 GHz** to **4.5 mm at 14 GHz**.

## Model and methods

The CST Studio Suite 2023 model uses a periodic 11 mm square unit cell with a copper backplane and 20 copper/FR4 layers. The layer width decreases linearly from 9 to 5 mm. Each layer has 0.20 mm of FR4 and 0.05 mm of copper; FR4 has relative permittivity 4.4 and loss tangent 0.02, and copper conductivity is `5e7 S/m`. A normally incident Floquet TE(0,0) mode excites the cell. The frequency-domain tetrahedral solver runs from 6 to 15 GHz with adaptive meshing. Absorption is calculated from both propagating Floquet modes as `A = 1 - R - T`.

The layers are **stepped square patches**, approximating the paper's continuously milled sloping sides. The report describes the remaining differences and convergence checks. The paper curves in Figure 2 are approximate values digitized from the supplied PDF; the red curve is the **paper's experiment**, not a new measurement. The original article PDF is not redistributed here.

## CST project and complete native results

The small [CST project file](cst/Ding2012_20layer.cst) contains the model setup. CST keeps its 3D results in a **same-named directory next to the `.cst` file**. The complete native project with this directory is provided as a downloadable archive under this repository's **Releases**. Extract the archive without changing that directory structure before opening it in CST. The repository itself also includes compact exported spectra and field grids so the figures remain inspectable without CST.

## Reproduce the simulation

Requirements: Windows, a licensed CST Studio Suite 2023 installation, Python 3.9 for CST's official Python interface, and a modern Python with the packages in [`requirements.txt`](requirements.txt) for plotting and the PDF report. Set the CST installation and a writable **ASCII-only** run directory. In PowerShell, from the repository root:

```powershell
$env:CST_INSTALL_DIR = 'E:\CST Studio Suite 2023' # adjust if needed
$env:CST_REPRO_RUN = 'C:\cst_reproduction\run'
& 'C:\path\to\python39\python.exe' scripts/build_and_run.py --build-only
& 'C:\path\to\python39\python.exe' scripts/solve_existing.py
& 'C:\path\to\python39\python.exe' scripts/export_clean.py
& 'C:\path\to\analysis-python\python.exe' -m pip install -r requirements.txt
& 'C:\path\to\analysis-python\python.exe' scripts/analyze_results.py
& 'C:\path\to\analysis-python\python.exe' scripts/make_report.py
```

`export_clean.py` deliberately runs the export macro **without adding it to model history**. Recording a result-export command in model history can invalidate CST's current 3D results. The first field export verifies that the values are nonzero before continuing. The complete solve took about seven minutes on the original workstation; runtime depends on hardware and solver settings.

## Data organization

`data/fields/*.npz` stores the central `x = 0` plane coordinates (`y`, `z`) and absolute vector-field magnitude (`amplitude`). Each panel in Figure 3 is normalized by its own maximum for display. `data/paper_*_digitized_clean.csv` holds approximate curves read from the paper's raster figure, with obvious axis/legend artefacts removed. `scripts/` holds the build, solve, export, analysis, and report programs. The PDF report contains the numerical comparison, field hot-spot positions, limitations, and source references.
