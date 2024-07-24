from setuptools import setup, find_packages

setup(
    name="sqlalchemy_serializer_meta",
    version="0.2.0",
    description="A simple serializer for SQLAlchemy models and Flask Models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Wehda23/sqlalchemy_serializer_meta",
    author="Waheed Khaled Elhariri",
    author_email="waheedkhaled95@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["sqlalchemy", "pydantic==2.7.4", "pydantic_core==2.18.4"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="sqlalchemy serializer pydantic flask",
    include_package_data=True,
)
