import setuptools
with open("README.md",  "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="csdnuploadimage",  # 模块名称
    version="2.0",  # 当前版本
    author="wqt",  # 作者
    author_email="2916311184@qq.com",  # 作者邮箱
    description="上传图片到csdn并返回图片url",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    # url="https://gitee.com/windheartyolo/csdn",  # 模块gitee地址
    packages=setuptools.find_packages(exclude="demos"),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'requests'
    ],
    python_requires='>=3.7',
)