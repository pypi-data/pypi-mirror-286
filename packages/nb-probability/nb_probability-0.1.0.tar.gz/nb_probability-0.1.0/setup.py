from setuptools import setup, find_packages

setup(
    name='nb_probability',
    version='0.1.0',
    author='Coskun Erden',
    description='A package for Gaussian and Binomial distributions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=[
        'matplotlib',
    ],
    extras_require={
        'dev': [
            'pytest',
            'sphinx',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
