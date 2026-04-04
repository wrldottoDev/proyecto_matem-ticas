from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.db.session import SessionLocal
from app.services.seed_service import seed_initial_data


def main() -> None:
    db = SessionLocal()
    try:
        seed_initial_data(db)
        print("Datos semilla cargados correctamente.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
