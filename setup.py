from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
]

test_requirements = [
    "nose"
]

setup(
    name='bzoing',
    version='v1.0-beta',
    description='Calendar alarms with python3 and gtk3',
    long_description=readme + '\n\n' + history,
    author='Luis Louro',
    author_email='lapisdecor@gmail.com',
    url='https://github.com/lapisdecor/bzoing',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=requirements,
    include_package_data=True,
    licence='MIT licence',
    zip_safe=False,
    keywords='bzoing',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    scripts=['bin/bzoing-now']
)
