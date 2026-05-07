#!/usr/bin/env bash
set -euo pipefail

# Local-only fallback for maintainers who need to publish outside GitHub
# Actions. The canonical release workflow uses PyPI Trusted Publishing via
# OIDC and must not call this script.

: "${RELEASE_INDEX:=TestPyPI}"

python -m pip install --upgrade twine

case "$RELEASE_INDEX" in
  PyPI)
    python -m twine upload -u __token__ -p "$PYPI_TOKEN" --non-interactive --skip-existing dist/*.whl dist/*.tar.gz
    ;;
  TestPyPI)
    python -m twine upload \
      --repository-url https://test.pypi.org/legacy/ \
      -u __token__ -p "$TEST_PYPI_TOKEN" \
      --non-interactive --skip-existing dist/*.whl dist/*.tar.gz
    ;;
  *)
    echo "Unsupported RELEASE_INDEX: $RELEASE_INDEX" >&2
    exit 1
    ;;
esac
