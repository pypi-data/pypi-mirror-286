from setuptools import setup, find_packages

setup(
    name="notify_online",
    version="0.1.1",
    description="A package to send email notifications when the device comes online",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Koi",
    author_email="your.email@example.com",
    url="https://github.com/datlt4",
    packages=find_packages(),
    install_requires=["Flask", "Flask-CORS", "Flask-Mail", "Jinja2", "requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
