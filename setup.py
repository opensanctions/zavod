from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()


setup(
    name="zavod",
    version="0.2.0",
    description="Data factory for followthemoney data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="data mapping identity followthemoney etl parsing",
    author="Friedrich Lindenberg",
    author_email="friedrich@pudo.org",
    url="https://github.com/opensanctions/zavod",
    license="MIT",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    namespace_packages=[],
    include_package_data=True,
    package_data={"": ["zavod/data/*", "zavod/py.typed"]},
    zip_safe=False,
    install_requires=[
        "followthemoney >= 2.9.4, < 3.0.0",
        "addressformatting",
        "requests",
        "structlog",
        "lxml",
        "click >= 8.0.0, < 8.2.0",
    ],
    tests_require=[],
    entry_points={
        "console_scripts": [],
    },
    extras_require={
        "dev": [
            "wheel>=0.29.0",
            "twine",
            "mypy",
            "flake8>=2.6.0",
            "pytest",
            "pytest-cov",
            "lxml-stubs",
            "coverage>=4.1",
            "types-setuptools",
            "types-requests",
        ]
    },
)
