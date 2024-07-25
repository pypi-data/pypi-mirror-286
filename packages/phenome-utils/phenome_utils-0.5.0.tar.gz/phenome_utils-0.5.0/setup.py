from setuptools import setup, find_packages

setup(
    name='phenome_utils',
    version='0.5.0',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A Python package for data manipulation and analysis utilities',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['pandas', 'numpy', 'matplotlib'],
    extras_require={
        'dev': ['pytest', 'pytest-cov', 'flake8'],
    },
    url='https://git.phenome.health/trent.leslie/phenome-utils',
    author='Trent Leslie',
    author_email='trent.leslie@phenomehealth.org',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='data analysis pandas utilities arivale snapshots',
    python_requires='>=3.8',
    package_data={'phenome-utils': ['main.py', 'arivale_snapshots_funcs.py']},
)
