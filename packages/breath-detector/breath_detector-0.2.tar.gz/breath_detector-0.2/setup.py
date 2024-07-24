from setuptools import setup, find_packages

setup(
    name='breath_detector',  # 包名
    version='0.2',              # 版本号
    packages=find_packages(),   # 包含的包列表
    install_requires=[          # 依赖列表
        'scipy',
        'numpy',
    ],
    author='jasine',         # 作者信息
    author_email='jasinechen@gmail.com',
    description='breath detector in Lingjing Env',  # 简要描述
)
