from setuptools import setup, find_packages

setup(
    name='postcodinator', 
    version='0.1.5',
    packages=find_packages(),
    include_package_data=True,
    description='A package to get info on UK post codes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Stephen Bourne',
    author_email='hello@stephenbourne.dev',
    install_requires=[
        'pandas',  
        'pyarrow',
    ],
    package_data={
        'postcodinator': ['data/*.parquet'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
