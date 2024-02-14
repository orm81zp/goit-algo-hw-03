""" 
Модуль по копіюванню файлів.
Приймає source та output папки як аргументи командного рядка. Source та dist за замовчуванням
"""

import shutil
from pathlib import Path
import sys
from abc import ABC, abstractmethod


class UnexpectedException(Exception):
    """Класс перехоплення загальних помилок"""


# ANSI escape codes for colored output
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"


def display_tree(path: Path, indent: str = "", prefix: str = "") -> None:
    """Виводить ієрархію переданого шляху у вигляді дерева"""
    try:
        if path.is_dir():
            print(indent + prefix + COLOR_BLUE + str(path.name) + COLOR_RESET)
            indent += "    " if prefix else ""
            children = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))

            for index, child in enumerate(children):
                is_last = index == len(children) - 1
                display_tree(child, indent, "└── " if is_last else "├── ")
        else:
            print(indent + prefix + str(path.name))
    except UnexpectedException as err:
        print("Сталася помилка при побудові дерева ієрархії")
        print(err)


def parse_arguments():
    """Отримує аргументи командного рядка"""
    source = "source"
    output = "dist"

    if len(sys.argv) > 2:
        source = sys.argv[1]
        output = sys.argv[2]
    elif len(sys.argv) > 1:
        source = sys.argv[1]

    print(f'Вихідна папка "{source}", кінцева папка "{output}"')
    print()

    return (source, output)


class BasicCopier(ABC):
    """Базовий класс Менеджерів з копіювання файлів"""

    def __init__(self, source_folder, output_folder):
        self.source_folder = Path(source_folder)
        self.output_folder = Path(output_folder)

    @abstractmethod
    def read_folder(self, source_path: Path):
        """Сканує source_path шлях на файли, викликає себе якщо поточний елемент директорія"""
        raise NotImplementedError("method should be implemented")

    @abstractmethod
    def copy_file(self, file: Path):
        """Копіює переданий file у output_folder"""
        raise NotImplementedError("method should be implemented")

    @abstractmethod
    def copy(self, show_result: bool):
        """Запускає процес пошуку файлів та їх копіювання"""
        raise NotImplementedError("method should be implemented")


class CopierByExtention(BasicCopier):
    """Копіюйє файли в директорії відповідно до їх розширення, наслідує BasicCopier класс"""

    def copy(self, show_result=False):
        self.read_folder(self.source_folder)
        if show_result:
            display_tree(self.output_folder)

    def read_folder(self, source_path: Path):
        try:
            for source in source_path.iterdir():
                if source.is_dir():
                    self.read_folder(source)
                else:
                    self.copy_file(source)
        except FileNotFoundError as err:
            self.handle_exception(err, "Такого файлу чи каталогу немає, перевірте...")

    def copy_file(self, file: Path):
        try:
            # отримати розширення файлу
            suffix = file.suffix.lower()
            # створити шлях для збереження та додати до нього розширення файлу
            output_folder = self.output_folder / suffix
            # за потреби створити необхідні директорії
            output_folder.mkdir(exist_ok=True, parents=True)
            # копіювати файл
            shutil.copyfile(file, output_folder / file.name)
        except UnexpectedException as err:
            self.handle_exception(err)

    def handle_exception(self, err, message="О, це все! Сталася біда!"):
        """Виводить кастомне повідомлення та повідомлення винятку"""
        print(message)
        print(err)


class Copier:
    """Запускає на виконання переданий менеджер копіювання файлів"""

    def __init__(self, copier: BasicCopier):
        self.copier = copier

    def copy(self, show_result=False):
        """Запускає копіювання файлів"""
        self.copier.copy(show_result)


def main():
    """Створює стратегію по копіюванню файлів та запускає на виконання"""
    print('"Супер Менеджер" з копіювання файлів v1')
    source_folder, output_folder = parse_arguments()
    copier = Copier(CopierByExtention(source_folder, output_folder))
    copier.copy(show_result=True)


if __name__ == "__main__":
    main()
