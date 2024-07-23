from setuptools import setup, find_packages

setup(
    name="apache_bot_blocker",
    version="0.1.0",
    author="Albert Zheng",
    author_email="anpei.zheng@gmail.com",
    description="Bot Blocker for server log",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your-repo",
    packages=find_packages(include=["apache_bot_blocker"]),
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
            'run_bot_blocker=apache_bot_blocker.__main__:main_function',  # Adjusted entry point
        ],
    },
    package_data={
        '': ['*.txt', '*.ini'],  # Include all .txt and .ini files in any package directory
    },
)
