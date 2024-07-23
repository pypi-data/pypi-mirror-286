from setuptools import setup, find_packages
import os

def get_data_files():
    data_files = []
    for file in ['config.ini']:
        if os.path.isfile(file) and file == 'config.ini':
            data_files.append(('', [file]))
        elif os.path.isfile(file):
            data_files.append(('apache_bot_blocker', [file]))  # Place files in the installation root
            print(f"Found file: {file}")
        else:
            print(f"Warning: {file} not found in the current directory.")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Files in current directory: {os.listdir('.')}")
    return data_files

setup(
    name="apache_bot_blocker",
    version="0.1.3",
    author="Albert Zheng",
    author_email="anpei.zheng@gmail.com",
    description="Bot Blocker for server log",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your-repo",
    packages=find_packages(),
    package_data= {'apache_bot_blocker': ['blacklist', 'whitelist', 'config.ini']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'run_bot_blocker=apache_bot_blocker.__main__:main_function',
        ],
    }
)