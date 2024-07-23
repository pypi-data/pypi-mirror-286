from setuptools import setup, find_packages

setup(
    name="streamlit-imp-sidebar",
    version="1.0.0",
    author="",
    author_email="",
    description="",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=find_packages(),  # Ensure this matches the package name
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "streamlit",
        # Add other dependencies
    ],
    package_data={
        "streamlit_imp_sidebar": ["frontend/build/*"],  # Use the correct package name
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
