from setuptools import setup, find_packages

setup(
    name='krrsnkapi',
    version='2024.07.21',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    description='Модуль для лёгкого использования моего бесполезного API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='kararasenok-gd',
    author_email='kararasenok_gd@icloud.com',
    url='https://github.com/kararasenok-gd/krrsnkapi/',  # URL проекта (если есть)
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
