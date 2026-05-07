#!/usr/bin/env bash
set -euo pipefail

: "${DOPPLER_PROJECT:=all}"
: "${DOPPLER_CONFIG:=main}"

required_secrets=(
  CODECOV_TOKEN
  DOPPLER_GITHUB_SERVICE_TOKEN
  SAFETY_API_KEY
)

missing=()
for secret_name in "${required_secrets[@]}"; do
  if ! doppler secrets get "$secret_name" --plain \
        --project "$DOPPLER_PROJECT" --config "$DOPPLER_CONFIG" \
        >/dev/null 2>&1; then
    missing+=("$secret_name")
  fi
done

if [ "${#missing[@]}" -gt 0 ]; then
  printf 'Missing Doppler secrets in %s/%s:\n' "$DOPPLER_PROJECT" "$DOPPLER_CONFIG" >&2
  printf '  - %s\n' "${missing[@]}" >&2
  exit 1
fi

echo "All required Doppler secrets from docs/doppler-setup.md are present in ${DOPPLER_PROJECT}/${DOPPLER_CONFIG}."
