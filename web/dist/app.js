'use strict';
const $=id=>document.getElementById(id);
let engine=null, rowsForExport=null, exportType='json', records=[], samples=[];
const base='https://laminhtrung.github.io/movie-lod-semantic-web';
const sitePath=new URL(base).pathname.replace(/\/$/,'');
const siteUrl=path=>sitePath+path;
const localMode=['localhost','127.0.0.1'].includes(location.hostname)&&!new URLSearchParams(location.search).has('browser');
function status(text,error=false){$('status').textContent=text;$('status').className=error?'error':'';}
function linkFor(uri){return uri.startsWith(base+'/')?siteUrl(uri.slice(base.length)):uri;}
function renderTable(vars,rows){
  const table=document.createElement('table'),head=document.createElement('thead'),tr=document.createElement('tr');
  vars.forEach(v=>{const th=document.createElement('th');th.textContent=v;tr.append(th);});head.append(tr);table.append(head);
  const body=document.createElement('tbody');
  rows.forEach(row=>{const tr=document.createElement('tr');vars.forEach(v=>{const td=document.createElement('td'),term=row[v];
    if(term?.type==='uri'&&/^https?:\/\//.test(term.value)){const a=document.createElement('a');a.href=linkFor(term.value);a.textContent=term.value.split('/').pop();td.append(a);}
    else {const value=term?.value;const number=Number(value);td.textContent=term?.datatype&&/(integer|decimal|double|float)$/.test(term.datatype)&&Number.isFinite(number)?String(number):(value??'—');}tr.append(td);});body.append(tr);});table.append(body);$('results').replaceChildren(table);
}
function renderJson(data){
  rowsForExport=data;exportType='json';
  if('boolean' in data){const p=document.createElement('p');p.className='boolean';p.textContent=data.boolean?'True':'False';$('results').replaceChildren(p);return 1;}
  const rows=data.results.bindings;renderTable(data.head.vars,rows);return rows.length;
}
function termJson(t){if(t.termType==='NamedNode')return {type:'uri',value:t.value};if(t.termType==='BlankNode')return {type:'bnode',value:t.value};const out={type:'literal',value:t.value};if(t.language)out['xml:lang']=t.language;else if(t.datatype)out.datatype=t.datatype.value;return out;}
function ntriplesTerm(t){if(t.termType==='NamedNode')return '<'+t.value+'>';if(t.termType==='BlankNode')return '_:'+t.value;return JSON.stringify(t.value)+(t.language?'@'+t.language:t.datatype?'^^<'+t.datatype.value+'>':'');}
async function fetchRdf(input,options){
  const response=await fetch(input,options);
  const url=new URL(typeof input==='string'?input:input.url,location.href);
  const mediaType=(response.headers.get('content-type')||'').split(';')[0].trim().toLowerCase();
  // Static hosting may serve .ttl as a generic download. Normalize only our
  // known Turtle dataset; preserve failures and all other remote responses.
  if(response.ok&&url.origin===location.origin&&['/data/movies.ttl','/data/reasoned.ttl','/data/before_after.trig'].map(siteUrl).includes(url.pathname)&&(!mediaType||mediaType==='application/octet-stream')){
    const headers=new Headers(response.headers);
    headers.set('Content-Type',url.pathname.endsWith('.trig')?'application/trig; charset=utf-8':'text/turtle; charset=utf-8');
    return new Response(response.body,{status:response.status,statusText:response.statusText,headers});
  }
  return response;
}
async function execute(){
  const query=$('query-text').value.trim();if(!query){status('Enter a SPARQL query.',true);return;}
  $('run').disabled=true;$('export').disabled=true;status('Running query…');const started=performance.now();
  try{
    let count;
    if(localMode){
      const response=await fetch(siteUrl('/sparql?mode=')+encodeURIComponent($('query-mode').value),{method:'POST',headers:{'Content-Type':'application/sparql-query','Accept':'application/sparql-results+json'},body:query});
      if(!response.ok){const err=await response.json();throw new Error(err.error||'Unable to run the query.');}
      if(response.headers.get('content-type').includes('sparql-results'))count=renderJson(await response.json());
      else{rowsForExport=await response.text();exportType='ttl';const pre=document.createElement('pre');pre.textContent=rowsForExport;$('results').replaceChildren(pre);count=null;}
    }else{
      engine??=new Comunica.QueryEngine();
      const sourcePath={asserted:'/data/movies.ttl',reasoned:'/data/reasoned.ttl',dataset:'/data/before_after.trig'}[$('query-mode').value];
      const context={sources:[{type:'file',value:new URL(siteUrl(sourcePath),location.origin).href}],fetch:fetchRdf};
      const result=await engine.query(query,context);
      if(result.resultType==='bindings'){
        const stream=await result.execute();const rows=[];const vars=[];
        await new Promise((resolve,reject)=>{stream.on('data',b=>{const row={};for(const [k,v]of b){if(!vars.includes(k.value))vars.push(k.value);row[k.value]=termJson(v);}rows.push(row);});stream.on('end',resolve);stream.on('error',reject);});
        const meta=await result.metadata();const ordered=meta.variables?.map(x=>(x.variable||x).value)||vars;
        count=renderJson({head:{vars:ordered},results:{bindings:rows}});
      }else if(result.resultType==='boolean')count=renderJson({boolean:await result.execute()});
      else if(result.resultType==='quads'){
        const stream=await result.execute(),lines=[];
        await new Promise((resolve,reject)=>{stream.on('data',q=>lines.push([q.subject,q.predicate,q.object].map(ntriplesTerm).join(' ')+' .'));stream.on('end',resolve);stream.on('error',reject);});
        rowsForExport=lines.join('\n');exportType='ttl';const pre=document.createElement('pre');pre.textContent=rowsForExport;$('results').replaceChildren(pre);count=lines.length;
      }else throw new Error('Only read queries are supported: SELECT, ASK, CONSTRUCT and DESCRIBE.');
    }
    const seconds=((performance.now()-started)/1000).toFixed(2);status((count===null?'RDF graph':count+' result'+(count===1?'':'s'))+' · '+seconds+' s');$('export').disabled=false;
  }catch(e){status('Query error: '+e.message,true);const p=document.createElement('p');p.className='empty';p.textContent='Check the syntax or choose a sample query.';$('results').replaceChildren(p);}
  finally{$('run').disabled=false;}
}
function renderFilms(){
  const text=$('search').value.toLocaleLowerCase('en');const list=records.filter(r=>(r.title+' '+r.director.map(p=>p.name).join(' ')).toLocaleLowerCase('en').includes(text));
  $('film-list').replaceChildren();for(const film of list){const a=document.createElement('a');a.className='film-card';a.href=linkFor(film.uri);
    const h=document.createElement('h3');h.textContent=film.title;const meta=document.createElement('p');meta.className='film-meta';meta.textContent=(film.year??'Year unknown')+' · '+(film.runtime_minutes===null?'Runtime unknown':film.runtime_minutes+' min');
    const dir=document.createElement('p');dir.textContent=film.director.map(x=>x.name).join(', ')||'Director unknown';const q=document.createElement('p');q.textContent=film.qid+' ↗';a.append(h,meta,dir,q);$('film-list').append(a);
  }if(!list.length){const p=document.createElement('p');p.textContent='No matching films found.';$('film-list').append(p);}
}
async function init(){
  try{
    const [stats,films,queries]=await Promise.all(['/data/statistics.json','/data/films.json','/data/queries.json'].map(async url=>{const r=await fetch(siteUrl(url));if(!r.ok)throw new Error('Unable to load the dataset.');return r.json();}));
    records=films;samples=queries;
    $('stats').replaceChildren();for(const [n,label]of [[stats.films,'films'],[stats.same_as,'external links'],[stats.classes,'classes']]){const s=document.createElement('span'),b=document.createElement('b');b.textContent=n.toLocaleString('en-US');s.append(b,document.createTextNode(label));$('stats').append(s);}
    samples.forEach((q,i)=>{const o=document.createElement('option');o.value=i;o.textContent=q.label;$('sample').append(o);});$('query-text').value=samples[0].query;$('query-mode').value=samples[0].mode;renderFilms();
    $('engine-note').textContent=localMode?'Querying the application SPARQL endpoint.':'Querying the RDF dataset in your browser with Comunica.';
    await execute();
  }catch(e){status(e.message,true);}
}
$('run').addEventListener('click',execute);$('sample').addEventListener('change',()=>{$('query-text').value=samples[+$('sample').value].query;$('query-mode').value=samples[+$('sample').value].mode;execute();});$('search').addEventListener('input',renderFilms);$('query-mode').addEventListener('change',()=>{status('Knowledge scope changed. Run the query to refresh results.');$('export').disabled=true;});
$('query-text').addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();execute();}});
$('copy').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('query-text').value);status('Query copied.');}catch{status('Select the query text and copy it with your keyboard.');}});
$('export').addEventListener('click',()=>{const payload=exportType==='json'?JSON.stringify(rowsForExport,null,2):rowsForExport;const url=URL.createObjectURL(new Blob([payload],{type:exportType==='json'?'application/json':'text/turtle'}));const a=document.createElement('a');a.href=url;a.download='query_results.'+exportType;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
init();
