from setuptools import setup, find_packages

setup(
    name='acuimax',
    version='0.1.3',
    description='CAPACIDAD DE CARGA MÁXIMA Y TIEMPO DE AGOTAMIENTO ENTRE DOS ACUÍFEROS.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ajila Nagua Ana Isabel, Ordoñez Salinas Xavi Alexander, Jonathan Tapia Cuenca, Taipe Jaramillo Josselyn Estefania',
    author_email='xavial152001@gmail.com, aiajila@utpl.edu.ec, jetaipe@utpl.edu.ec, jatapia14@utpl.edu.ec ',
    url='https://github.com/JonathanTapia-1/AcuiMax.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy==1.24.1',
    ],
)


