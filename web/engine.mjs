export function scoreSong(r,s){let score=0;const reasons=[];for(const [field,w] of [['genre',2],['mood',1]])if(r[field].trim().toLowerCase()===s[field].trim().toLowerCase()){score+=w;reasons.push(`${field} match (+${w.toFixed(2)})`)}const sim=1-Math.abs(s.energy-r.energy);score+=sim;reasons.push(`energy similarity ${sim.toFixed(2)} (+${sim.toFixed(2)})`);return {score,reason:reasons.join('; ')}}
export function recommend(r,catalog){
 for(const key of ['genre','mood'])if(typeof r[key]!=='string'||!r[key].trim()||r[key].length>80)throw Error(`${key} must contain 1–80 characters`);
 for(const key of ['energy','min_bpm','max_bpm'])if(typeof r[key]!=='number'||!Number.isFinite(r[key]))throw Error(`${key} must be a finite number`);
 if(r.energy<0||r.energy>1)throw Error('Energy must be between 0 and 1');
 if(!(r.min_bpm>0&&r.min_bpm<=r.max_bpm&&r.max_bpm<=300))throw Error('Minimum tempo must be no greater than maximum tempo (1–300 BPM).');
 for(const key of ['count','max_per_artist'])if(!Number.isInteger(r[key])||r[key]<1||r[key]>20)throw Error(`${key} must be an integer from 1 to 20`);
 if(typeof r.strict_genre!=='boolean'||!Array.isArray(r.exclude_ids)||r.exclude_ids.some(x=>!Number.isInteger(x)||x<=0))throw Error('Invalid genre or exclusion setting');
 const eligible=s=>!r.exclude_ids.includes(s.id)&&s.tempo_bpm>=r.min_bpm&&s.tempo_bpm<=r.max_bpm&&(!r.strict_genre||s.genre.toLowerCase()===r.genre.trim().toLowerCase());
 const candidates=catalog.filter(eligible);const ranked=candidates.map(song=>({song,...scoreSong(r,song)})).sort((a,b)=>b.score-a.score);
 const items=[],artists=new Map();for(const row of ranked){let key=row.song.artist.trim().toLowerCase();if((artists.get(key)||0)<r.max_per_artist){items.push(row);artists.set(key,(artists.get(key)||0)+1)}if(items.length===r.count)break}
 const errors=[],seen=new Set(),counts=new Map();for(const row of items){const original=catalog.find(s=>s.id===row.song.id),expected=scoreSong(r,row.song),artist=row.song.artist.trim().toLowerCase();if(!original||JSON.stringify(original)!==JSON.stringify(row.song))errors.push('Catalog membership');if(seen.has(row.song.id)||!eligible(row.song))errors.push('Constraint violation');seen.add(row.song.id);counts.set(artist,(counts.get(artist)||0)+1);if(Math.abs(expected.score-row.score)>1e-9||expected.reason!==row.reason)errors.push('Score integrity')}
 if(items.length>r.count||[...counts.values()].some(n=>n>r.max_per_artist)||items.some((v,i)=>i&&items[i-1].score<v.score))errors.push('Playlist integrity');
 const trace=[{step:'validate',status:'pass'},{step:'filter',candidates:candidates.length,catalog_size:catalog.length},{step:'rank_and_diversify',selected:items.length},{step:'verify',status:errors.length?'fail':'pass',errors}];
 if(errors.length)return {status:'blocked',items:[],warnings:['Verification failed; results withheld.'],trace};
 const warnings=[];if(!candidates.some(s=>s.genre.toLowerCase()===r.genre.trim().toLowerCase()))warnings.push('No requested-genre matches within constraints; review alternatives or change the request.');if(items.length<r.count)warnings.push('Too few eligible tracks; constraints were not relaxed.');
 return {status:items.length?'ok':'no_matches',items,warnings,trace};
}
