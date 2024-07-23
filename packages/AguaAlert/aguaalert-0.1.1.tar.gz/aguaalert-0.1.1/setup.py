from setuptools import setup, find_packages

setup(
    name='AguaAlert',
    version='0.1.1',
    description='Sistema de predicción de niveles de aguas subterráneas utilizando datos de precipitación.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='José Rodríguez, Anderson Pineda, Andriana Espinoza, Cesar Villavicencio, Jhon Castillo',
    author_email='jdrodriguez30@utpl.edu.ec',
    url='https://github.com/yourusername/AguaAlert',
    packages=find_packages(), 
    include_package_data=True, 
    package_data={ 'AguaAlert': ['data/*.csv'], },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy==1.24.1',
        'matplotlib',
        'pandas',
        'scikit-learn',
        'statsmodels',
        'scipy',
        'openpyxl',
    ],
)


