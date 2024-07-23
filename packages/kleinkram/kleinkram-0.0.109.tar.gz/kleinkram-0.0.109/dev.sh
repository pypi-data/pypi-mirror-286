#!/usr/bin/zsh

rm ./dist/*

python3 -m build
pip3 install dist/Kleinkram_CLI*.whl --force-reinstall