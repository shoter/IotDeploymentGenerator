Remove-Item -Path "./dist/*" -Recurse -Force
python -m build
python -m twine upload --repository testpypi dist/*