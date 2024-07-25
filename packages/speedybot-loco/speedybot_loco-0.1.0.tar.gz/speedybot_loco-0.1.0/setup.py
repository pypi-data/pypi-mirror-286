from setuptools import setup, find_packages
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name="speedybot-loco",
    version="0.1.0",
    author="Victor Algaze",
    author_email="valgaze@gmail.com",
    description="Use googles-- highly experimental conversation design infra",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/valgaze/speedybot-loco",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
