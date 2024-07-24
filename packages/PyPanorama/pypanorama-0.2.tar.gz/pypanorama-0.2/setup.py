from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as stream:
    long_description = stream.read()

setup(
    name="PyPanorama",
    author="ZOOM",
    version="0.02",
    description="A versatile Python library offering a wide range of functionalities for various applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['Python', 'versatile', 'utilities', 'social media', 'Instagram', 'Facebook', 'TikTok'],
    python_requires='>=3.6',
)
