from setuptools import setup, find_packages

setup(
    name='silabi-tokenizer',
    version='0.5.0',
    description='A custom tokenizer for Swahili text using syllabic vocabulary with byte fallback.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Edwin Nguthiru',
    author_email='nguthiruedwin@gmail.com',
    url='https://github.com/nguthiru/silabi-tokenizer',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'transformers>=4.0.0',
        # Add any other dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
