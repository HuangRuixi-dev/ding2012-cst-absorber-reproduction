"""Prepare the 1-80 GHz model entry point. Does not run a new simulation.

Recorded results remain in cases/. A new full-band solver result is deliberately
not claimed: the published figure combines the documented discrete case data.
"""
from pathlib import Path
import csv
import json
from cst_runtime import bootstrap
bootstrap()
import cst.interface

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE/'cases/FR4_80layer_mid55_70_5GHz_screen/absorber.cst'
TARGET = BASE.parent/'cst/absorber.cst'
if TARGET.exists():
    raise FileExistsError('Refusing to overwrite existing model: ' + str(TARGET))
with (BASE/'data/merged_discrete_spectrum.csv').open(encoding='utf-8-sig') as stream:
    frequencies = sorted(float(row['frequency_GHz']) for row in csv.DictReader(stream)
                         if float(row['frequency_GHz']) <= 80)
assert len(frequencies) == len(set(frequencies))
code = 'Solver.FrequencyRange "1", "80"\nWith FDSolver\n'
code += '.MeshAdaptionTet "True"\n.SetMethod "", "Discrete samples only"\n.ResetSampleIntervals "all"\n'
for frequency in frequencies:
    adapt = 'True' if frequency == 78 else 'False'
    code += '.AddSampleInterval "%s", "%s", "1", "Single", "%s"\n' % (frequency, frequency, adapt)
code += 'End With'
env = cst.interface.DesignEnvironment.new()
project = None
try:
    print('Preparing owned CST environment pid=' + str(env.pid()), flush=True)
    project = env.open_project(str(SOURCE))
    assert Path(project.filename()).resolve() == SOURCE.resolve()
    project.modeler.add_to_history('Prepare 1-80 GHz discrete sampling setup', code, timeout=120)
    project.save(str(TARGET), include_results=False)
    assert TARGET.is_file() and TARGET.stat().st_size > 0
    info = dict(entry_project='cst/absorber.cst', source_case=SOURCE.parent.name,
                frequency_range_GHz=[1, 80], discrete_frequencies_GHz=frequencies,
                prepared_without_new_solver_run=True,
                published_result_source='absorber/data/merged_discrete_spectrum.csv',
                mesh_note='Rerunning this entry point uses one mesh adapted at 78 GHz; published cases used separate frequency-group meshes.')
    (BASE/'data/main_project_info.json').write_text(json.dumps(info,indent=2),encoding='utf-8')
    print('Saved cst/absorber.cst; no solver run.', flush=True)
finally:
    if project is not None:
        project.close()
    env.close()
