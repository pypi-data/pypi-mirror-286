import pytest

from umd_lib_style.templatetags.umd_lib_style import environment_banner


@pytest.mark.parametrize(
    ('environment', 'expected_label'),
    [
        ('development', 'Local Environment'),
        ('sandbox', 'Sandbox Environment'),
        ('test', 'Test Environment'),
        ('qa', 'QA Environment'),
    ]
)
def test_environment_banner(settings, environment, expected_label):
    settings.ENVIRONMENT = environment
    html = environment_banner()
    assert html == f'<div class="{environment} environment-banner">{expected_label}</div>'


def test_production_environment(settings):
    settings.ENVIRONMENT = 'production'
    html = environment_banner()
    assert html == ''


def test_unknown_environment(settings):
    settings.ENVIRONMENT = 'xanadu'
    html = environment_banner()
    assert html == ''


def test_no_environment(settings):
    settings.ENVIRONMENT = None
    html = environment_banner()
    assert html == ''
