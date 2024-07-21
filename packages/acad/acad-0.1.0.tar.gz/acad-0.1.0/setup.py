from setuptools import setup, find_packages

setup(
    name='acad',
    version='0.1.0',
    description='Adaptive Clustering and Anomaly Detection',
    author='Your Name',
    author_email='quadxome@gmail.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
    ],
    tests_require=[
        'pytest',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
