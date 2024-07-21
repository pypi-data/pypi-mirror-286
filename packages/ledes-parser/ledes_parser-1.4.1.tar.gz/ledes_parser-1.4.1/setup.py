import os

from setuptools import find_packages, setup


# To avoid needless setup-time dependencies introduced as a side-effect of importing the __init__.py file, for now.
def read_version():
    version_file_path = os.path.join(
        os.path.dirname(__file__), "ledes_parser", "__init__.py"
    )
    with open(version_file_path) as f:
        for line in f:
            if line.startswith("__version__"):
                # Extract the version number.
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


def main() -> None:
    setup(
        name="ledes-parser",
        description="A package for parsing LEDES format files",
        url="https://github.com/travisbashor/ledes-parser",
        author="Travis Bashor",
        author_email="travis.bashor@gmail.com",
        version=read_version(),
        packages=find_packages(exclude=["tests*"]),
        include_package_data=True,
        package_data={"ledes_parser": ["grammars/**/*.lark", "transformers/**/*.py"]},
        install_requires=["lark-parser==0.12.0", "lark==1.1.9"],
    )


if __name__ == "__main__":
    main()
