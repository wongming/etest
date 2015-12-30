from setuptools import setup, find_packages
setup(
    name = "stest",
    version = "1.0.0",
    packages = find_packages(),
    package_data = {'': ['*.txt',
                         '*.html',
                         '*.md',
                         ]
    },
    entry_points = {
        'console_scripts': [
            'stest = stest:main',
        ]
    }
 )
