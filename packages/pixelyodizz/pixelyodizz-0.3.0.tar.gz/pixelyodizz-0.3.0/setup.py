from setuptools import setup, find_packages


with open("README.md", "r") as f:
    description = f.read()

setup(
    name="pixelyodizz",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        'pathlib',
        'tensorflow',
        'matplotlib',
        'numpy',
        'seaborn',
        'IPython',
        'gradio',
        # Add dependencies here.
        # e.g. 'numpy>=1.11.1'
    ],

    long_description=description,
    long_description_content_type="text/markdown",
)
