from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='multi_agent_systems',
    version='1.0.0',
    author='haleen24',
    author_email='',
    description='Module for simulating multi-agent-systems using Petri nets from pm4py',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/haleen24/MultiAgentSystems.git',
    packages=find_packages(),
    install_requires=['requests>=2.25.1'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='multi-agent-systems simulating',
    project_urls={
        'Documentation': 'https://github.com/haleen24/MultiAgentSystems.git'
    },
    python_requires='>=3.7'
)
