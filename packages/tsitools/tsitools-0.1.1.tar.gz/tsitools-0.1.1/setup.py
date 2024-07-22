from setuptools import setup, find_packages

setup(
    name='tsitools',
    version='0.1.1',
    description='A Python module for parsing and analyzing output files from the TSI 3330 optical particle sizer.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tayebcodes/tsitools',
    author='Tayeb Kakeshpour',
    author_email='tayeb.codes@gmail.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=[
        'numpy',
        'pandas'
    ],
)
