from setuptools import setup, find_packages
from pathlib import Path

# Lire le fichier README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='wtf_calculator',
    version='0.2.2',
    packages=find_packages(),
    description='Une librairie pour faire des calculs complètement faux.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Zmeypp',
    author_email='lmayel@gmail.com',
    url='https://github.com/votre-utilisateur/wtf_calculator',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.6',
)
