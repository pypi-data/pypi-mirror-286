from setuptools import setup

name = "types-PyYAML"
description = "Typing stubs for PyYAML"
long_description = '''
## Typing stubs for PyYAML

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`PyYAML`](https://github.com/yaml/pyyaml) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`PyYAML`.

This version of `types-PyYAML` aims to provide accurate annotations
for `PyYAML==6.0.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/PyYAML. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`0b1d35829b3f727ce562987360eabf45873d413c`](https://github.com/python/typeshed/commit/0b1d35829b3f727ce562987360eabf45873d413c) and was tested
with mypy 1.10.1, pyright 1.1.372, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="6.0.12.20240724",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/PyYAML.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['yaml-stubs'],
      package_data={'yaml-stubs': ['__init__.pyi', '_yaml.pyi', 'composer.pyi', 'constructor.pyi', 'cyaml.pyi', 'dumper.pyi', 'emitter.pyi', 'error.pyi', 'events.pyi', 'loader.pyi', 'nodes.pyi', 'parser.pyi', 'reader.pyi', 'representer.pyi', 'resolver.pyi', 'scanner.pyi', 'serializer.pyi', 'tokens.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
