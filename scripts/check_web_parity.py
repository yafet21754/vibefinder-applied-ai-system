"""Compare browser engine with Python across a deterministic request matrix. Requires Node.js."""
from dataclasses import asdict
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.recommender import load_songs
from src.system import Request, run_system

catalog = load_songs(ROOT / 'data/songs.csv')
assert json.loads((ROOT / 'web/catalog.json').read_text()) == catalog, 'Browser catalog is stale'
requests = []
for genre in ['lofi','house','pop','opera']:
    for mood in ['chill','euphoric','sad']:
        for energy in [0,.35,.88,1]:
            for strict in [False,True]:
                for low,high in [(1,300),(100,140)]:
                    requests.append(Request(genre,mood,energy,count=5,min_bpm=low,max_bpm=high,strict_genre=strict,exclude_ids=(4,)))
process = subprocess.run(['node','web/check-parity.mjs'],cwd=ROOT,input=json.dumps({'requests':[asdict(r) for r in requests],'catalog':catalog}),capture_output=True,text=True,check=True)
actual=json.loads(process.stdout)
for request,js_result in zip(requests,actual):
    expected=run_system(request,catalog)
    # IEEE floating arithmetic can differ below the reported score precision.
    for result in [expected,js_result]:
        for row in result['items']:
            row['score']=round(row['score'],9)
    assert js_result==expected, (request,js_result,expected)
assert len(actual)==len(requests)
print(f'{len(requests)}/{len(requests)} browser/Python parity cases passed (including catalog equality).')
