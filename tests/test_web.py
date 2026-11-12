import json
from functools import partial
from http.server import ThreadingHTTPServer
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request as HTTPRequest, urlopen
import pytest
from src.web import Handler, ROOT, process_request
from src.system import Request, run_system
from src.recommender import load_songs


@pytest.fixture
def server():
    httpd = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(ROOT / 'web')))
    thread = Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f'http://127.0.0.1:{httpd.server_port}'
    httpd.shutdown()
    httpd.server_close()
    thread.join()


def test_web_assets_and_runtime(server):
    with urlopen(server + '/') as r:
        assert r.status == 200 and b'Find your' in r.read()
    with urlopen(server + '/runtime.json') as r:
        assert json.load(r) == {'engine': 'python'}


def test_api_uses_original_python_engine(server):
    payload = dict(genre='lofi', mood='chill', energy=.35, count=3)
    request = HTTPRequest(server + '/api/recommend', data=json.dumps(payload).encode(), headers={'Content-Type':'application/json'})
    with urlopen(request) as r:
        result = json.load(r)
    assert result == run_system(Request(**payload), load_songs(ROOT / 'data/songs.csv'))


@pytest.mark.parametrize('payload', [[], {}, {'genre':'lofi','mood':'chill','energy':2}, {'genre':'lofi','mood':'chill','energy':.35,'unexpected':1}])
def test_invalid_requests_are_handled(server, payload):
    with pytest.raises(HTTPError) as error:
        urlopen(HTTPRequest(server+'/api/recommend', data=json.dumps(payload).encode()))
    assert error.value.code == 400
    assert json.load(error.value)['status'] == 'error'


def test_cross_origin_requests_rejected(server):
    with pytest.raises(HTTPError) as error:
        urlopen(HTTPRequest(server+'/api/recommend', data=b'{}',headers={'Origin':'https://example.com'}))
    assert error.value.code == 403
