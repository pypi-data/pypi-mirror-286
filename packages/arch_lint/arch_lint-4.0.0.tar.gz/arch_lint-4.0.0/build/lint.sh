# shellcheck shell=bash

echo "Executing pylint phase" \
  && pylint arch_lint \
  && echo "Finished pylint phase"
