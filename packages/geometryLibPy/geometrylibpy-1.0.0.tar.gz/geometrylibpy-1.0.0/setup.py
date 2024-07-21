from setuptools import setup, find_packages


def readme() -> str:
    with open('../README.md', 'r') as f:
        return f.read()


setup(
    name='geometryLibPy',
    version='1.0.0',
    author='mav735',
    author_email='mav735@ya.ru',
    description='This is the simplest module for calculating the area of a geometric figures.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url=r'https://github.com/mav735/GeometryLibPy',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='math geometry figures area',
    project_urls={
        'GitHub': 'https://github.com/mav735/GeometryLibPy'
    },
    python_requires='>=3.8'
)
