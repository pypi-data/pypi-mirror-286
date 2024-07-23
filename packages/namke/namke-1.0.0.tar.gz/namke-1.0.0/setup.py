import setuptools
from setuptools import setup

setup(
    name='namke',
    version='1.0.0',
    description='nagisa make, for nasm, c and c plus plus',
    author='nagisa',
    author_email='1300296933@qq.com',
    package_dir={"": "src"},  # 打包目录
    packages=setuptools.find_packages(where='src'),  # 搜索存在__init__.py打包文件夹
)
