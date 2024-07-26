from setuptools import setup, find_packages

setup(
    name="covidslimiter",
    version="0.43",
    packages=find_packages(),
    description="A simple IP rate limiter for Flask apps.",
    author="Covid Gtag",
    py_modules=['rate_limiter', 'decorator'],
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python",
        "Framework :: Flask",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="flask ip rate limiter",
    install_requires=[
        "Flask>=2.0.0"
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "flake8",
            "black"
        ]
    },
)
