from setuptools import setup, find_packages

setup(
    name='groxai_llms',
    version='0.0.1',
    author='Intrepid-AI',
    author_email='jaiyesh0002@gmail.com',
    description='Helps to use the groxai_llms package for the devlopment',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Intrepid-AI/groxai_llms',
    project_urls={
        "Bug Tracker": f"https://github.com/Intrepid-AI/groxai_llms/issues",
    },
    package_dir = {'': 'src'},
    packages=find_packages(where='src'),
    
)
