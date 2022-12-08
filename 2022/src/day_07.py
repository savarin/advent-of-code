from typing import Dict, List, Optional, TextIO, Union
import dataclasses


@dataclasses.dataclass
class File:
    name: str
    size: int


@dataclasses.dataclass
class Directory:
    name: str

    def __post_init__(self):
        self.size: Optional[int] = None
        self.subdirectories: List[str] = []
        self.files: List[File] = []


def generate_directories(commands: Union[List[str], TextIO]) -> Dict[str, Directory]:
    directories_by_directory_path: Dict[str, Directory] = {"/": Directory("/")}
    current_directory: Directory = directories_by_directory_path["/"]
    current_path: List[str] = []
    previous_command: Optional[str] = None

    for line in commands:
        if line.startswith("$ "):
            contents = line.rstrip("\n")[2:].split(" ")
            current_command, args = contents[0], contents[1:]

            if current_command == "ls":
                previous_command = "ls"
                continue

            elif current_command == "cd":
                previous_command = "cd"
                assert len(args) == 1

                if args[0] == "/":
                    current_directory = directories_by_directory_path["/"]
                    current_path = []
                    continue

                elif args[0] == "..":
                    current_path.pop()

                else:
                    current_path.append(args[0])

                current_directory = directories_by_directory_path[
                    "/" + "/".join(current_path)
                ]

            else:
                raise Exception("Exhaustive switch error.")

        elif line.startswith("dir "):
            assert previous_command == "ls"
            directory_name = line.rstrip("\n")[4:]
            current_directory.subdirectories.append(directory_name)

            directory_path = "/" + "/".join(current_path + [directory_name])
            directories_by_directory_path[directory_path] = Directory(directory_path)

        elif line.split(" ")[0].isdigit():
            assert previous_command == "ls"
            file_size, file_name = line.rstrip("\n").split(" ")
            current_directory.files.append(File(file_name, int(file_size)))

        else:
            raise Exception("Exhaustive switch error.")

    return directories_by_directory_path


def stringify_directories(directories: Dict[str, Directory]) -> List[str]:
    results: List[str] = []

    def closure(directory_path: str) -> None:
        directory = directories[directory_path if directory_path != "" else "/"]
        results.append(f"- {directory} (dir)")

        for file in sorted(directory.files, key=lambda x: x.name):
            results.append(f"  - {file.name}, (file, size={file.size})")

        for subdirectory_name in sorted(directory.subdirectories):
            subdirectory_path = directory_path + "/" + subdirectory_name
            closure(subdirectory_path)

    closure("")
    return results


def sum_file_sizes(directories: Dict[str, Directory]) -> int:
    def closure(directory_path: str) -> int:
        directory = directories[directory_path if directory_path != "" else "/"]

        if directory.size is not None:
            return directory.size

        size: int = 0

        for file in directory.files:
            size += file.size

        for subdirectory_name in directory.subdirectories:
            subdirectory_path = directory_path + "/" + subdirectory_name
            size += closure(subdirectory_path)

        directory.size = size
        return size

    return closure("")


def test_generate_directories() -> None:
    commands = [
        "$ cd /",
        "$ ls",
        "dir a",
        "14848514 b.txt",
        "8504156 c.dat",
        "dir d",
        "$ cd a",
        "$ ls",
        "dir e",
        "29116 f",
        "2557 g",
        "62596 h.lst",
        "$ cd e",
        "$ ls",
        "584 i",
        "$ cd ..",
        "$ cd ..",
        "$ cd d",
        "$ ls",
        "4060174 j",
        "8033020 d.log",
        "5626152 d.ext",
        "7214296 k",
    ]

    expected_result = [
        "- Directory(name='/') (dir)",
        "  - b.txt, (file, size=14848514)",
        "  - c.dat, (file, size=8504156)",
        "- Directory(name='/a') (dir)",
        "  - f, (file, size=29116)",
        "  - g, (file, size=2557)",
        "  - h.lst, (file, size=62596)",
        "- Directory(name='/a/e') (dir)",
        "  - i, (file, size=584)",
        "- Directory(name='/d') (dir)",
        "  - d.ext, (file, size=5626152)",
        "  - d.log, (file, size=8033020)",
        "  - j, (file, size=4060174)",
        "  - k, (file, size=7214296)",
    ]

    directories_by_directory_path = generate_directories(commands)
    assert directories_by_directory_path["/"].size is None

    for i, item in enumerate(stringify_directories(directories_by_directory_path)):
        assert item == expected_result[i]

    sum_file_sizes(directories_by_directory_path)
    assert directories_by_directory_path["/"].size == 48381165


if __name__ == "__main__":
    test_generate_directories()

    with open("data/day_07.txt", "r") as f:
        directories_by_directory_path = generate_directories(f)
        sum_file_sizes(directories_by_directory_path)
        print(
            sum(
                [
                    directory.size
                    for _, directory in directories_by_directory_path.items()
                    if directory.size is not None and directory.size <= 100000
                ]
            )
        )

        assert directories_by_directory_path["/"].size is not None
        min_size = directories_by_directory_path["/"].size - (70000000 - 30000000)
        print(
            min(
                [
                    directory.size
                    for _, directory in directories_by_directory_path.items()
                    if directory.size is not None and directory.size > min_size
                ]
            )
        )
