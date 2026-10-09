"""Local SPARQL Protocol query endpoint plus linked-data dereferencing."""
import json
from urllib.parse import unquote
from flask import Flask, Response, request, send_from_directory, redirect
from rdflib import Graph, URIRef, Dataset
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.parserutils import CompValue
from common import ROOT, BASE, RES, EX, SITE_PATH, site_path

app=Flask(__name__,static_folder=None)
app.config['MAX_CONTENT_LENGTH']=64*1024
_flask_wsgi=app.wsgi_app

def mounted_wsgi(environ,start_response):
    path=environ.get('PATH_INFO','/')
    if SITE_PATH and (path==SITE_PATH or path.startswith(SITE_PATH+'/')):
        environ['SCRIPT_NAME']=SITE_PATH
        environ['PATH_INFO']=path[len(SITE_PATH):] or '/'
    return _flask_wsgi(environ,start_response)

app.wsgi_app=mounted_wsgi
DATA=Graph().parse(ROOT/'data/processed/movies.ttl')
SCHEMA=Graph().parse(ROOT/'ontology/movie.ttl')
REASONED=Graph().parse(ROOT/'data/processed/reasoned.ttl') if (ROOT/'data/processed/reasoned.ttl').exists() else DATA+SCHEMA
NAMED=Dataset().parse(ROOT/'data/processed/before_after.trig',format='trig') if (ROOT/'data/processed/before_after.trig').exists() else Dataset()

def disallow_remote(node):
    if isinstance(node,CompValue):
        if node.name=='ServiceGraphPattern' or ('datasetClause' in node and node['datasetClause']):
            raise ValueError('This endpoint queries the MovieLOD dataset only. SERVICE and FROM are not supported.')
        for value in node.values():disallow_remote(value)
    elif isinstance(node,(list,tuple)):
        for value in node:disallow_remote(value)
    elif isinstance(node,dict):
        for value in node.values():disallow_remote(value)

@app.after_request
def headers(response):
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['X-Content-Type-Options']='nosniff'
    return response

@app.route('/sparql',methods=['GET','POST','OPTIONS'])
def sparql():
    if request.method=='OPTIONS':
        return Response(status=204,headers={'Access-Control-Allow-Methods':'GET, POST, OPTIONS','Access-Control-Allow-Headers':'Content-Type, Accept'})
    query=request.args.get('query')
    if request.method=='POST':
        if request.mimetype=='application/sparql-query':query=request.get_data(as_text=True)
        elif request.is_json:query=(request.get_json(silent=True) or {}).get('query')
        else:query=request.form.get('query')
    if not isinstance(query,str) or not query.strip():return {'error':'A SPARQL query is required.'},400
    try:
        prepared=prepareQuery(query)
        disallow_remote(prepared.algebra)
        mode=request.args.get('mode',request.form.get('mode','asserted'))
        if request.is_json:mode=(request.get_json(silent=True) or {}).get('mode',mode)
        if mode not in ['asserted','reasoned','dataset']:raise ValueError('Unknown query mode.')
        result={'asserted':DATA,'reasoned':REASONED,'dataset':NAMED}[mode].query(prepared)
        if result.type in ['SELECT','ASK']:
            return Response(result.serialize(format='json'),content_type='application/sparql-results+json')
        return Response(result.graph.serialize(format='turtle'),content_type='text/turtle; charset=utf-8')
    except Exception as e:
        return {'error':str(e)},400

@app.get('/health')
def health():return {'status':'ok','data_triples':len(DATA),'query_engine':'RDFLib','ontology_version':'3.0.0','modes':['asserted','reasoned','dataset']}

@app.get('/resource/<slug>')
@app.get('/resource/<slug>/')
def resource(slug):
    s=RES[slug]
    if not any(DATA.triples((s,None,None))):return {'error':'Resource not found.'},404
    if 'text/turtle' in request.headers.get('Accept',''):
        return redirect(site_path('/describe/'+slug+'.ttl'),code=303)
    if 'application/ld+json' in request.headers.get('Accept',''):
        return redirect(site_path('/describe/'+slug+'.jsonld'),code=303)
    return send_from_directory(ROOT/'web/dist/resource'/slug,'index.html')

@app.get('/describe/<slug>.<suffix>')
def describe(slug,suffix):
    if suffix not in ['ttl','jsonld']:return {'error':'Unsupported format.'},404
    s=RES[slug];sub=Graph()
    for t in DATA.triples((s,None,None)):sub.add(t)
    if not len(sub):return {'error':'Resource not found.'},404
    fmt,ctype=('turtle','text/turtle') if suffix=='ttl' else ('json-ld','application/ld+json')
    return Response(sub.serialize(format=fmt),content_type=ctype+'; charset=utf-8')

@app.get('/ontology')
def ontology():
    if 'text/turtle' in request.headers.get('Accept',''):return Response(SCHEMA.serialize(format='turtle'),content_type='text/turtle')
    return send_from_directory(ROOT/'web/dist/ontology','index.html')

@app.get('/')
def home():return send_from_directory(ROOT/'web/dist','index.html')

@app.get('/<path:path>')
def assets(path):
    if path=='dataset' or path=='dataset/':return send_from_directory(ROOT/'web/dist/dataset','index.html')
    return send_from_directory(ROOT/'web/dist',path)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8000);p.add_argument('--host',default='127.0.0.1')
    args=p.parse_args();app.run(host=args.host,port=args.port,debug=False)
