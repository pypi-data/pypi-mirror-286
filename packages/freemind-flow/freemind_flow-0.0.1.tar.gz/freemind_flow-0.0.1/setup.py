from setuptools import setup, find_packages

setup(
    name='freemind-flow',  # Replace with your package name
    version='0.0.1',  # Replace with your package version
    packages=find_packages(),  # Automatically find packages in the project
    install_requires=[
        # List your package dependencies here
        # e.g., 'numpy>=1.19.2', 'pandas>=1.1.3'
    ],
    entry_points={
        'console_scripts': [
            # Define your console scripts here
            # e.g., 'my-command=my_package.module:main_function'
        ],
    },
    author='cowabungajohnny3',
    author_email='cowabungajohnny3@gmail.com',
    description='A brief description of your package',
    long_description=open('README.md', encoding='utf-8').read(),  # Ensure you have a README.md file
    long_description_content_type='text/markdown',
    url='https://github.com/cowabungajohnny3/freemind-flow',  # Replace with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Replace with your minimum Python version requirement
)