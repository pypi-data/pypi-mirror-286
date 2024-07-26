from setuptools import setup, find_packages

setup(
    name="envmate",
    version="0.2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "inquirer",
    ],
    entry_points={
        'console_scripts': [
            'your_command=your_package.main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A brief description of your package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/harris-ahmad/your_project",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
