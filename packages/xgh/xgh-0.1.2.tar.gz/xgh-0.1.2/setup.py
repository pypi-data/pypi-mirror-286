from setuptools import setup, find_packages

setup(
    name='xgh',
    version='0.1.2',
    description='I think, therefore I am not XGH',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/xgh',  # Replace with your actual URL
    author='Shane Busenitz',
    author_email='shanebusenitz@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'boto3',
        'tqdm'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
