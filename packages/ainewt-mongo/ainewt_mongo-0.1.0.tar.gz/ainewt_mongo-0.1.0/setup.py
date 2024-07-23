from setuptools import setup, find_packages

setup(
    name='ainewt_mongo',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pymongo',
        'bson',
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A MongoDB utility package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://your.package.repo.url',  # Update this with your package repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
