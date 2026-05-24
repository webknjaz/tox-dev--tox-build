[![SWUbanner]][SWUdocs]

[![tox-dev badge]][tox-dev]
[![pre-commit.ci status badge]][pre-commit.ci results page]
[![GH Sponsors badge]][GH Sponsors URL]

[SWUbanner]:
https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg
[SWUdocs]:
https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md

[tox-dev]: https://github.com/tox-dev
[tox-dev badge]:
https://img.shields.io/badge/project-yellow?label=tox-dev&labelColor=c3cc39&color=7f833e

[pre-commit.ci status badge]:
https://results.pre-commit.ci/badge/github/tox-dev/tox-build/main.svg
[pre-commit.ci results page]:
https://results.pre-commit.ci/latest/github/tox-dev/tox-build/main

[GH Sponsors badge]:
https://img.shields.io/badge/%40webknjaz-transparent?logo=githubsponsors&logoColor=%23EA4AAA&label=Sponsor&color=2a313c
[GH Sponsors URL]:
https://github.com/sponsors/webknjaz


# tox-build

A tox plugin providing pypa/build dist-build environments.


## Usage

Add `tox-build` to your project's `tox` requirements -- either
in `tox.toml`:

```toml
requires = [
  "tox-build",
]
```

...or in `tox.ini`:

```ini
[tox]
requires =
  tox-build
```

Then invoke any of the three dist-build envs the plugin exposes:

```console
$ tox run -q -e cleanup-dists        # wipe dist/
$ tox run -q -e build-dists          # build sdist + wheel into dist/
$ tox run -q -e metadata-validation  # twine-check the dists
```
