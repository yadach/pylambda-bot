#!/usr/bin/env bash
set -u

pkg_name="pylambda_bot"

pkg_dir="awspkg_${pkg_name}"
pkg_zip="${pkg_dir}.zip"

# make package directory
rm -rf "${pkg_dir}"
source .venv/bin/activate
python -m pip install . -t "${pkg_dir}"
cp lambda_function.py "${pkg_dir}"
cp config.yaml "${pkg_dir}"

# zip pacakge directory
rm -f "${pkg_zip}"
cd "${pkg_dir}"
zip -r ../${pkg_zip} . \
    -x "./*.dist-info/*"
