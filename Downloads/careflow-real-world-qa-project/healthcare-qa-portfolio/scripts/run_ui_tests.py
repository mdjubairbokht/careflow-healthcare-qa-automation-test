"""Launch isolated demo server, run Playwright tests, and stop server."""
import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

def main():
    with tempfile.TemporaryDirectory() as directory:
        port = free_port()
        env = dict(os.environ, DEMO_DB=str(Path(directory) / 'ui.db'), BASE_URL=f'http://127.0.0.1:{port}')
        server = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', str(port)], cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        try:
            for _ in range(100):
                if server.poll() is not None:
                    raise RuntimeError('Demo server stopped unexpectedly')
                try:
                    with socket.create_connection(('127.0.0.1', port), timeout=0.2):
                        break
                except OSError:
                    time.sleep(0.1)
            else:
                raise RuntimeError('Demo server failed to start')
            return subprocess.call([sys.executable, '-m', 'pytest', 'tests/ui', '--junitxml=reports/ui-results.xml'], cwd=ROOT, env=env)
        finally:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()

if __name__ == '__main__':
    sys.exit(main())
