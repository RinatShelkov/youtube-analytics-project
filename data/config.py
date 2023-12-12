from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent

DATA_PATH = ROOT_PATH.joinpath("data")
print(DATA_PATH)