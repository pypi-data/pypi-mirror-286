# setup.py

from setuptools import setup, find_packages

setup(
    name='evaluate_attacks',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'torch',
        'torchattacks',
        'matplotlib',
        'numpy',
    ],
    author='Sahbaaz Ansari',
    author_email='mlsecadversarialattack@gmail.com',
    description='A package for evaluating adversarial attacks on deep learning models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Cyberus-MLSec/eval_adv_attack',  # Replace with your repository URL
)
