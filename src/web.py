"""Serve the VibeFinder interface using the original Python recommendation engine.

Usage: python -m src.web (then open http://127.0.0.1:8000).
Local development server only; do not expose it as a production server.
"""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from .recommender import load_songs
from .system import Request, run_system

ROOT = Path(__file__).resolve().parents[1]


def process_request(payload):
    if not isinstance(payload, dict):
        raise ValueError("Request must be a JSON object")
    try:
        request = Request(**payload)
    except TypeError as error:
        raise ValueError("Invalid or missing playlist fields") from error
    return run_system(request, load_songs(ROOT / "data/songs.csv"))


class Handler(SimpleHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/runtime.json":
            self.send_json({"engine": "python"})
        else:
            super().do_GET()

    def do_POST(self):
        if self.path != "/api/recommend":
            self.send_json({"message": "Not found"}, 404)
            return
        if self.headers.get("Origin") not in (None, f"http://127.0.0.1:{self.server.server_port}", f"http://localhost:{self.server.server_port}"):
            self.send_json({"message": "Origin not allowed"}, 403)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 16384:
                raise ValueError("Request body must contain 1–16384 bytes")
            payload = json.loads(self.rfile.read(length))
            self.send_json(process_request(payload))
        except (ValueError, UnicodeDecodeError) as error:
            self.send_json({"status": "error", "message": str(error)}, 400)
        except OSError:
            self.send_json({"status": "error", "message": "Catalog unavailable"}, 500)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(Handler, directory=str(ROOT / "web")))
    print(f"VibeFinder is ready: http://127.0.0.1:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
