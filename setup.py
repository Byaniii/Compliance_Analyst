from setuptools import setup

setup(
    name="bounty-compliance",
    version="0.1.0",
    description="AML/KYC Compliance Review System",
    py_modules=["compliance_engine", "cli", "examples"],
    install_requires=[
        "flask>=2.0",
        "flask-cors>=3.0",
        "pytest>=7.0",
    ],
)
