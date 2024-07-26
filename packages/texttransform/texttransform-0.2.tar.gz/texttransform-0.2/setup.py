from setuptools import setup

setup(
    name='texttransform',
    version='0.2',
    py_modules=['text_transform'],
    entry_points={
        'console_scripts': [
            'texttransform = text_transform:main',
        ],
    },
    description='A tool to convert sentences between uppercase and lowercase and to format sentences correctly.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Genevieve',
    author_email='genevieve.okon@rocketmail.com',
    url='https://github.com/Genevieveok/texttransform',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

