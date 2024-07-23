import setuptools


setuptools.setup(
    name="woodAI",
    version="1.0.4",
    author="codemao",
    url='https://codemao.cn/',
    author_email="linyifeng@codemao.cn",
    description="wood ai",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=['websocket-client']
)