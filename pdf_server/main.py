import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))

from pdf_server.backend import app
from pdf_server.database import DatabaseConnection

if __name__ == "__main__":
    with DatabaseConnection():
        app.run(host="0.0.0.0", threaded=True)
