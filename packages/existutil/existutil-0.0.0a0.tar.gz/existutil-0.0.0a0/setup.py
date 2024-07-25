import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='existutil',
    version='0.0.0a0',
    author='Devin A. Conley',
    author_email='devinaconley@gmail.com',
    description='exist utils for data loading, reading, and exploratory data analysis',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/devinaconley/exist-util',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'python-dotenv',
        'requests>=2,<3'
    ]
)
