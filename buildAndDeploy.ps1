Remove-Item -Path "./dist/*" -Recurse -Force
python -m build
python -m twine upload dist/*