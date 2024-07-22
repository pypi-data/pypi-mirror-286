from setuptools import setup, find_packages

setup(
    name='LLM4HW',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        # sudo apt-get install python3-tk
        # pip install numpy
        'numpy',
        # pip install openai
        'openai',
        # pip install Flask
        'Flask',
        # pip install python-dotenv
        'python-dotenv',
        # 'python3-tk',
    ],
    author='Siyu Qiu',
    author_email='siyu.qiu1@unsw.edu.au',
    description='Everything you need to install for the LLM4HW tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/annnnie-qiu/annie_install',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
