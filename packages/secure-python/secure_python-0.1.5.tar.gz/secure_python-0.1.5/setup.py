from setuptools import setup, find_packages

setup(
    name='secure-python',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        'chardet', 
        'pyarmor',
    ],
    entry_points={
    'console_scripts': [
        'encrypt_code=secure_python.encryptor:encrypt_code',
    ],
    },
    author='Om Prakash',
    author_email='omprakash.das@involead.com',
    description='A package for securing Python code .',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
