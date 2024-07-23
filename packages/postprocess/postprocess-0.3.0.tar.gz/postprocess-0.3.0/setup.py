from setuptools import setup, find_packages

setup(
    name='postprocess',
    version='0.3.0',
    description='A brief description of the postprocess package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'rdkit',  # 指定包的依赖
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
