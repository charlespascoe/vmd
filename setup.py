from setuptools import setup, find_packages
setup(
    name = 'vmd',
    packages = find_packages(),
    package_data = {
        'vmd': ['themes/*']
    },
    version = '0.1.1',
    description = 'Terminal Markdown Renderer',
    author = 'Charles Pascoe',
    url='https://github.com/cpascoe95/vmd',
    author_email = 'charles@cpascoe.co.uk',
    keywords = ['terminal', 'markdown', 'viewer', 'md'],
    classifiers = [ # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Markup',
        'Topic :: Utilities'
    ],
    install_requires = [
        'Markdown==2.6.8'
    ],
    entry_points={
        'console_scripts': [
            'vmd = vmd:main'
        ]
    }
)
