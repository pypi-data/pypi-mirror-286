# setup.py

from setuptools import setup, find_packages

setup(
    name='BorgTestGenerator',
    version='0.1.2',
    packages=find_packages(),
    install_requires=['openai', 'python-dotenv'],
    author='0x07cb',
    author_email='83157348+0x07CB@users.noreply.github.com',
    description='Librairie pour générer des tests unitaires à partir de scripts Python en utilisant OpenAI.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/smartestmanuniverse/BorgTestGenerator',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
