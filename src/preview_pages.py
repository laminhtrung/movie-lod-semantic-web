"""Preview GitHub Pages under its project path; never fall back to domain-root assets."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlsplit
from common import ROOT,SITE_PATH

class PagesHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path=urlsplit(self.path).path
        if not (path==SITE_PATH or path.startswith(SITE_PATH+'/')):
            self.send_error(404,'Outside the GitHub Pages project');return
        if path==SITE_PATH:
            self.send_response(301);self.send_header('Location',SITE_PATH+'/');self.end_headers();return
        self.path=self.path[len(SITE_PATH):]
        super().do_GET()
    def log_message(self,*args):pass

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8017);args=parser.parse_args()
    print(f'http://127.0.0.1:{args.port}{SITE_PATH}/?browser=1',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),partial(PagesHandler,directory=str(ROOT/'web/dist'))).serve_forever()
