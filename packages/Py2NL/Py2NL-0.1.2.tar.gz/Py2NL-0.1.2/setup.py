from setuptools import setup

setup(
    name='Py2NL',
    version='0.1.2',
    description='A natural language interface for Python',
    url='https://github.com/TsXTatzumi/PyNLI',
    author='Simeon Quant',
    author_email='K51831785@students.jku.at',
    license='BSD 2-clause',
    packages=['PyNLI'],
    install_requires=['langchain~=0.2.10',
                      'langchain-openai~=0.1.8',
                      'langchain-community~=0.2.9',
                      'langchain-experimental~=0.0.49',
                      'solara~=1.35.1',
                      'pandas~=2.2.2',
                      'opencv-python~=4.10.0.84',
                      'Pillow~=10.4.0',
                      'pydantic~=2.7.0',
                      'libcst~=1.3.1',
                      'markdown~=3.6',
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Framework :: Jupyter',
        'Programming Language :: Python :: 3.10',
    ],
)