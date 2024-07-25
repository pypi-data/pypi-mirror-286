from setuptools import setup, find_packages

setup(
    name='mstturing',
    version='1.5.0',
    author='Martynas Stelmokas',
    author_email='stelmokas00@gmail.com',
    description='A package containing utility functions for matrix operations including transpose, 1D windowing, and 2D convolution.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/TuringCollegeSubmissions/martstelm-DE2v2.1.5',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'numpy',
    ],
    python_requires='>=3.6',
    license='MIT',
)