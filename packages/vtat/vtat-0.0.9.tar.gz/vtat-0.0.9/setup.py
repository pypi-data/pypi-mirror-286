from setuptools import setup, find_packages

setup(
    name='vtat',
    version='0.0.9',
    packages=find_packages(),
    description='A simple ACL system',
    author='vtat',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author_email='askofback@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[],
    python_requires='>=3.6'
)
