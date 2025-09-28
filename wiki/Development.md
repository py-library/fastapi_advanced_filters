# Development

- Lint & typecheck: `pre-commit run --all-files`
- Tests with coverage: `pytest --cov --cov-report=term-missing`
- Build (Poetry): `poetry build`

CI/CD:
- CI runs flake8, mypy, and pytest with coverage on pushes and PRs.
- Coverage is uploaded to Codecov for visibility in badges and PRs.
- Publishing is handled on GitHub Releases via trusted publishing to PyPI.
