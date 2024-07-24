from setuptools import setup, find_packages

setup(
    name="crx-snake",
    version="1.1.0",
    description="A collection of functions for creating Discord bots, works with nextcord.",
    long_description="A collection of functions for creating Discord bots, works with nextcord.",
    url="https://discord.gg/EEp67FWQDP",
    author="CRX-DEV",
    author_email="cherniq66@gmail.com",
    license="MIT License",


    packages=find_packages(include=["crxsnake", "crxsnake.*"]),
    install_requires=[
        "tortoise-orm==0.21.0",
        "disnake==2.9.2",
        "aiofiles==23.2.1",
        "fastenv==0.5.0",
        "loguru==0.7.2",
    ]
)
