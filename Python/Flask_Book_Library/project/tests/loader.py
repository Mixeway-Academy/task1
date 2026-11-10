import importlib
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = ROOT


def load(module_name):
    if 'project' not in sys.modules:
        package = types.ModuleType('project')
        package.__path__ = [str(PROJECT_DIR)]
        sys.modules['project'] = package
    return importlib.import_module(module_name)