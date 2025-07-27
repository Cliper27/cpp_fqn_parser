from pathlib import Path
import json

from _pytest.python import Metafunc


def pytest_generate_tests(metafunc: Metafunc) -> None:
    if "fqn_dict" in metafunc.fixturenames:
        path: Path = Path(__file__).parent.parent / "test_data" / "fqns.json"
        with path.open() as f:
            fqns = json.load(f)
        metafunc.parametrize("fqn_dict", fqns)
