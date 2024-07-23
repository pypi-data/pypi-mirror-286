from setuptools import setup, find_packages

setup(
    name='opticonomy-pdme',
    version='0.1.7',
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Add command line scripts here if needed
        ],
    },
    author='Opticonomy',
    author_email='info@opticonomy.com',
    description='Opticonomy Prompt Driven Model Evaluation (PDME)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/opticonomy/opticonomy-pdme',  # Update with your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
