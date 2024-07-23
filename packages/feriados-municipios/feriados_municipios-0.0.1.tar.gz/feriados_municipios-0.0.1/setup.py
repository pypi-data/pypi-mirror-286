from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='feriados_municipios',
    version='0.0.1',
    license='MIT License',
    author='Luiz Fernando Teles Rodrigues',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='euluizfernando2001@gmail.com',
    keywords='feriados br municipais brasil',
    description='Versão beta da biblioteca de feriados municipais.',
    packages=find_packages(),
    install_requires=['datetime'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    entry_points={
        "console_scripts": [
            "feriados-municipios = feriados_municipios.main:main"
        ]
    }
)