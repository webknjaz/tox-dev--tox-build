"""A tox plugin providing pypa/build dist-build environments."""

from __future__ import annotations

import typing as _t
from shlex import join as shlex_join

from tox.config.loader.memory import MemoryLoader
from tox.plugin import impl


if _t.TYPE_CHECKING:
    from collections import abc as _c  # noqa: WPS347

    from tox.config.sets import ConfigSet
    from tox.session.state import State


_PYTHON_CLI_OPTIONS = (
    'python',
    '-bb',
    '-E',
    '-s',
    '-I',
    '-Werror',
)


@impl
def tox_extend_envs() -> _c.Iterable[str]:
    """Declare the dist-build environments.

    :returns: The names of the tox environments this plugin provides.
    """
    return ('cleanup-dists', 'build-dists', 'metadata-validation')


@impl
def tox_add_core_config(
    core_conf: ConfigSet,  # noqa: ARG001  # pylint: disable=unused-argument
    state: State,
) -> None:
    """Inject default configuration for the dist-build environments.

    :param core_conf: The core tox configuration set (unused).
    :param state: The tox session state to inject environments into.
    """
    _inject_cleanup_dists(state)
    _inject_build_dists(state)
    _inject_metadata_validation(state)


def _inject_cleanup_dists(state: State) -> None:
    """Inject the ``cleanup-dists`` environment.

    :param state: The tox session state to inject the env into.
    """
    cleanup_cmd = (
        *_PYTHON_CLI_OPTIONS,
        '-c',
        (
            'import os, shutil, sys; '
            'shutil.rmtree("dist", ignore_errors=True); '
            'sys.exit(os.path.exists("dist"))'
        ),
    )

    state.conf.memory_seed_loaders['cleanup-dists'].append(
        MemoryLoader(
            base=[],
            description='[tox-build] Wipe the `dist/` folder',
            deps=[],
            commands_pre=[],
            commands=[shlex_join(cleanup_cmd)],
            commands_post=[],
            package='skip',
        ),
    )


def _inject_build_dists(state: State) -> None:
    """Inject the ``build-dists`` environment.

    :param state: The tox session state to inject the env into.
    """
    build_cmd = (
        *_PYTHON_CLI_OPTIONS,
        '-m',
        'build',
    )

    state.conf.memory_seed_loaders['build-dists'].append(
        MemoryLoader(
            base=[],
            description=(
                '[tox-build] Build sdist and wheel into `dist/` '
                'using pypa/build'
            ),
            deps=['build'],
            depends=['cleanup-dists'],
            commands_pre=[],
            commands=[shlex_join(build_cmd)],
            commands_post=[],
            package='skip',
        ),
    )


def _inject_metadata_validation(state: State) -> None:
    """Inject the ``metadata-validation`` environment.

    :param state: The tox session state to inject the env into.
    """
    check_cmd = (
        *_PYTHON_CLI_OPTIONS,
        '-m',
        'twine',
        'check',
        '--strict',
        'dist/*',
    )

    state.conf.memory_seed_loaders['metadata-validation'].append(
        MemoryLoader(
            base=[],
            description=(
                '[tox-build] Verify that dists under `dist/` '
                'have valid metadata'
            ),
            deps=['twine'],
            depends=['build-dists'],
            commands_pre=[],
            commands=[shlex_join(check_cmd)],
            commands_post=[],
            package='skip',
        ),
    )
