from setuptools import setup, find_packages

setup(
    name='Pale_exe',
    version='0.1',
    install_requires=[
        'maturin>=1.7.0'
    ],
    extras_require={
        'dev': ['twine>=4.0.2']
    },
    packages=find_packages(),
    python_requires='>=3.7',
)