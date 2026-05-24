"""Behavioral tests for the tox-build plugin."""

from __future__ import annotations

import typing as _t

import pytest


if _t.TYPE_CHECKING:
    from pytest_subtests import SubTests

    from tox.pytest import ToxProjectCreator


def test_build_envs_registered(
    tox_project: ToxProjectCreator,
    subtests: SubTests,
) -> None:
    """The plugin contributes the dist-build envs to the env list.

    :param tox_project: Tox-provided project factory fixture.
    :param subtests: Pytest's subtest fixture for granular reporting.
    """
    project = tox_project({'tox.ini': '[tox]\n'})
    tox_invocation_result = project.run('list')
    tox_invocation_result.assert_success()
    for env_name in ('cleanup-dists', 'build-dists', 'metadata-validation'):
        with subtests.test(msg=env_name):
            assert env_name in tox_invocation_result.out


@pytest.mark.parametrize(
    ('env_name', 'expected_present'),
    (
        pytest.param(
            'cleanup-dists',
            ('shutil.rmtree', 'dist'),
            id='cleanup-dists',
        ),
        pytest.param(
            'build-dists',
            ('-m build',),
            id='build-dists',
        ),
        pytest.param(
            'metadata-validation',
            ('-m twine', 'check', '--strict', 'dist/'),
            id='metadata-validation',
        ),
    ),
)
def test_env_commands(
    tox_project: ToxProjectCreator,
    env_name: str,
    expected_present: tuple[str, ...],
    subtests: SubTests,
) -> None:
    """The plugin's envs produce the expected ``commands`` config.

    :param tox_project: Tox-provided project factory fixture.
    :param env_name: Name of the env to query.
    :param expected_present: Substrings that must appear in the output.
    :param subtests: Pytest's subtest fixture for granular reporting.
    """
    project = tox_project({'tox.ini': '[tox]\n'})
    tox_invocation_result = project.run(
        'config',
        '-e',
        env_name,
        '-k',
        'commands',
    )
    tox_invocation_result.assert_success()
    for substring in expected_present:
        with subtests.test(msg=substring):
            assert substring in tox_invocation_result.out
