from setuptools import setup, find_packages

setup(
    name="mu_teg_sim",
    version="1.0.0",
    author="Davide Beretta",
    author_email="mail.davide.beretta+github@gmail.com",
    description="An app to simulate the device physics of micro Thermoelectric Generators",
    long_description="An app to simulate the device physics of micro Thermoelectric Generators (μTEGs). "
                     "It calculates the power generated, the efficiency of conversion, the device resistance, the open circuit voltage, and the short circuit current "
                     "per unit area as a function of the thermocouple length. "
                     "This app is designed for scientists, researchers, and engineers who want to simulate the device physics of μTEGs, "
                     "to analyze performance metrics and optimize designs for various applications.",
    url="https://github.com/BerriesLab/mu-teg-sim",
    readme="README.md",
    packages=find_packages(),
    keywords=["python", "thermoelectric", "physics"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
    entry_points={
        'console_scripts': [
            "mu_teg_sim=mu_teg_sim.cli.cli:main",
        ]
    },
    include_package_data=False,
)
