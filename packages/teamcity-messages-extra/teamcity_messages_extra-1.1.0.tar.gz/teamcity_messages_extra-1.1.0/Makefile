
test: _require_venv
	pytest --cov

style-check:
	black teamcity_extra tests --check
	isort teamcity_extra tests --check

style:
	black teamcity_extra tests
	isort teamcity_extra tests

# FIXME: https://github.com/pypa/pip/issues/11440
deps:
	pip install .[dev]
	pip uninstall -y teamcity-messages-extra

_require_venv:
	test -n "$(VIRTUAL_ENV)" || test -n "$(GITHUB_RUN_ID)"
