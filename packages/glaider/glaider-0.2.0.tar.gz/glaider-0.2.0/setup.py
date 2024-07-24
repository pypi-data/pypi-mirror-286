from setuptools import setup, find_packages

setup(
    name='glaider',
    version='0.2.0',
    description='A Python library to interact with generative ai tools safely',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Lorenzo Abati',
    author_email='lorenzo@glaider.it',
    url='',
    packages=find_packages(),
    install_requires=[
        'cohere==4.11.2',
        'openai==0.27.8',
        'pydantic==1.10.9',
        'requests==2.31.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)
