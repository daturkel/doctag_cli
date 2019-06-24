from setuptools import setup

setup(
    name="doctag_cli",
    version="0.0.2",
    description="A simple CLI for tagging documents with doctag.",
    long_description=open("README.md").read(),
    install_requires=["doctag>=0.0.1", "Click>=7.0", "pyyaml>=5.1"],
    url="https://github.com/daturkel/doctag_cli",
    author="Dan Turkel",
    author_email="daturkel@gmail.com",
    license="MIT",
    packages=["doctag_cli"],
    zip_safe=False,
    entry_points="""
        [console_scripts]
        dt=doctag_cli.scripts.cli:cli
    """,
)
