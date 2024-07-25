from setuptools import setup, find_packages

setup(
    name='cfaf',  # The name of your package
    version='0.1',
    packages=find_packages(),
    install_requires=[],  # Dependencies
    entry_points={
        'console_scripts': [
            'cfaf=cfaf.create_folder_and_files:main',  # Correct entry point
        ],
    },
    description='A package to create folders and files',
    author='waleedoff',
    author_email='waled988@hotmail.com',
    url='http://example.com/cfaf',
)
