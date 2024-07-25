from setuptools import setup, find_packages

setup(
    name='dapcy',
    version='0.1.1',
    author='Alejandro Correa Rojo',
    author_email='alejandro.correarojo@uhasselt.be',
    description='An sklearn implementation of discriminant analysis of principal components (DAPC) for population genetics',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/uhasselt-bioinfo/dapcy',  # Update with your repo URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'bed_reader',
        'joblib',
        'matplotlib',
        'numpy',
        'pandas',
        'scikit-learn',
        'scipy',
        'seaborn',
        'sgkit',
        'sgkit[vcf]',
    ],
)
