from setuptools import setup, find_packages
import flask_boost

entry_points = {
    "console_scripts": [
        "boost = flask_boost.cli:main",
    ]
}

with open("requirements.txt") as f:
    requires = [l for l in f.read().splitlines() if l]

setup(
    name='Flask-Boost',
    version=flask_boost.__version__,
    packages=find_packages(),
    include_package_data=True,
    description='Flask application generator for boosting your development.',
    long_description=open('README.rst').read(),
    url='https://github.com/hustlzp/Flask-Boost',
    author='hustlzp',
    author_email='hustlzp@gmail.com',
    license='MIT',
    keywords='flask sample generator',
    install_requires=requires,
    entry_points=entry_points,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)