PUBLISH=python3 setup.py sdist upload --sign

setup:
	pip3 install -r requirements.txt

publish:
	${PUBLISH} -r pypi

publish-test:
	${PUBLISH} -r pypitest

clean:
	rm -rf dist/ vmd.egg-info/ **/__pycache__/
