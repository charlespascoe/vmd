
setup:
	pip3 install -r requirements.txt

readme:
	pandoc README.md -o README.rst

sdist:
	python3 setup.py sdist

publish: sdist
	twine upload --sign dist/*

publish-test:
	echo "TODO: Implement!"

clean:
	rm -rf dist/ vmd.egg-info/ **/__pycache__/
