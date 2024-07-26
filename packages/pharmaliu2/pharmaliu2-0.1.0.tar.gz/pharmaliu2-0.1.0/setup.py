from setuptools import setup, find_packages

setup(
    name='pharmaliu2',
    version='0.1.0',
    description='A package for pharmacokinetic modeling and parameter estimation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='liucann',
    author_email='liucan18726995722@163.com',
    # url='https://github.com/yourusername/pharmacokinetics',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)