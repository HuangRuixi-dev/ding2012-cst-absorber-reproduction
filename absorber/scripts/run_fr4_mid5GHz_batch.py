"""Sequential, bounded mesh-adaptive simulations for the requested 5 GHz grid."""
from pathlib import Path
import json
import runpy
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get('CST_ABSORBER_RUN', str(HERE.parent/'cases')))
ROOT.mkdir(parents=True, exist_ok=True)
stages = []
for lower, upper in [(15, 30), (35, 50), (55, 70)]:
    case = 'FR4_80layer_mid%d_%d_5GHz_screen' % (lower, upper)
    stage = dict(case=case, lower_GHz=lower, upper_GHz=upper,
                 state='running', started=time.strftime('%Y-%m-%d %H:%M:%S'))
    stages.append(stage)
    (ROOT/'mid5GHz_batch_status.json').write_text(json.dumps(stages, indent=2))
    print('START_GROUP ' + case, flush=True)
    sys.argv = [str(HERE/'run_fr4_mid5GHz_group.py'), case,
                '80', '20', '6.9', '7.2', str(lower), str(upper)]
    try:
        runpy.run_path(str(HERE/'run_fr4_mid5GHz_group.py'), run_name='__main__')
    except BaseException as error:
        stage.update(state='error', error=str(error))
        (ROOT/'mid5GHz_batch_status.json').write_text(json.dumps(stages, indent=2))
        raise
    stage.update(state='exported', finished=time.strftime('%Y-%m-%d %H:%M:%S'))
    (ROOT/'mid5GHz_batch_status.json').write_text(json.dumps(stages, indent=2))
    print('FINISHED_GROUP ' + case, flush=True)
