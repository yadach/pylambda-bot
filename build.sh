#!/usr/bin/env bash
set -u

pkg_name="pylambda_bot"
PYTHON_VERSION=3.7.16


pkg_dir="${pkg_name}_zip2aws"
pkg_zip="${pkg_dir}.zip"

# make package directory
rm -rf "${pkg_dir}"
python3.7 -m pip install . -t "${pkg_dir}"
cp lambda_function.py "${pkg_dir}"
cp config.yaml "${pkg_dir}"

# zip pacakge directory
rm -f "${pkg_zip}"
cd "${pkg_dir}"
zip -r ../${pkg_zip} . \
    -x "./*.dist-info/*"
