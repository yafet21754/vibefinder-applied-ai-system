import {readFileSync} from 'node:fs';
import {recommend} from './engine.mjs';
const input=JSON.parse(readFileSync(0,'utf8'));
console.log(JSON.stringify(input.requests.map(r=>recommend(r,input.catalog))));
