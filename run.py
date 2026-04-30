"""Entry point for launching the Streamlit app.

Run:
    python run.py
"""

from pathlib import Path
import subprocess
import sys


def main() -> None:
    app_path = Path(__file__).parent / "src" / "projectile_optimizer" / "app.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)], check=True)


if __name__ == "__main__":
    main()
