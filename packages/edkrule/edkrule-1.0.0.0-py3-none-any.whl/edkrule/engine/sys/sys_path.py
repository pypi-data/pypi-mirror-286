import pathlib


def sys_path():
    return pathlib.Path(__file__).parent.joinpath(pathlib.Path("engine.xml"))


if __name__ == "__main__":
    print(sys_path())