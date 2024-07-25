from setuptools import setup, find_packages
setup(
    name="Flowpicturize",
    version="1.1.1",
    author="HuangX",
    # 如果Flowpicturize目录下还有其他子包，使用find_packages()
    # packages=find_packages(),
    # 如果只有Flowpicturize这一个顶级包，可以省略packages参数
    # 或者显式指定（可选）
    packages=['Flowpicturize'],
    # 其他可能的设置，如安装需求（install_requires），描述（description）等
    # install_requires=[
    #     'numpy',
    #     'pandas',
    #     # 其他依赖
    # ],
    # description="A brief description of your package",
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    # ...
)