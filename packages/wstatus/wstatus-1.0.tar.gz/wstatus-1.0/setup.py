from setuptools import setup, find_packages

setup(
    name="wstatus",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.2"
    ],
    entry_points={
        'console_scripts': [
            'wstatus=website_status_checker.checker:check_websites_cli',
        ],
    },
    python_requires='>=3.9',
    author="Diego Mengarelli",
    author_email="diegoamengarelli@gmail.com",
    description="Una herramienta que verifica si una lista de sitios web está activa y disponible.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/diegoamengarelli/web_status_checker",
)