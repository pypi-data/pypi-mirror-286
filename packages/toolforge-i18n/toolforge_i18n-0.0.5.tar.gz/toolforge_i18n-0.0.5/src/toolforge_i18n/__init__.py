try:
    import pytest
except ModuleNotFoundError:
    pass
else:
    pytest.register_assert_rewrite('toolforge_i18n.translations_tests', 'toolforge_i18n.translations_checks')
