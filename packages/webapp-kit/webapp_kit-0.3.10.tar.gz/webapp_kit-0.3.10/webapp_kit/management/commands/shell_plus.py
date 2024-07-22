import code
import importlib
import inspect
import os
import pkgutil
import sys
from typing import Type

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from webapp_kit.persistence.sync.repositories.repository import BaseSyncRepository
from webapp_kit.persistence.entities import BaseDBEntity


class ShellPlusCommand:
    DB_ENTITIES_PACKAGES = []

    def models_to_import(self) -> set[Type[BaseDBEntity]]:
        subclasses = set()

        # Рекурсивно ищем все модули в пакете
        def iter_modules(package):
            for _, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
                yield module_name
                if is_pkg:
                    module = importlib.import_module(module_name)
                    yield from iter_modules(module)

        # Импортируем все модули и ищем наследников
        for package in self.DB_ENTITIES_PACKAGES:
            imported_package = importlib.import_module(package)
            for module_name in iter_modules(imported_package):
                try:
                    module = importlib.import_module(module_name)
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if issubclass(obj, BaseDBEntity) and obj is not BaseDBEntity:
                            subclasses.add(obj)
                            print(f"Imported {name} from {module_name}")
                except ImportError as e:
                    print(f"Could not import module {module_name}: {e}")
                except Exception as e:
                    print(f"Error processing module {module_name}: {e}")

        return subclasses

    def run(self) -> None:
        context = {
            "BaseSyncRepository": BaseSyncRepository
        }
        models = self.models_to_import()
        for model in models:
            context[model.__name__] = model
        code.interact(local=context)

if __name__ == '__main__':
    cmd = ShellPlusCommand()
    cmd.DB_ENTITIES_PACKAGES = ["test_models"]
    cmd.run()