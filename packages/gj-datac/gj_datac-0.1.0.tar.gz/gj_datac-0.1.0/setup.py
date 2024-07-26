from setuptools import setup, find_packages

setup(
    name='gj_datac',  # 你的包名
    version='0.1.0',  # 版本号
    description='gj_datac api',  # 包的简要描述
    author='shuai yin',  # 作者姓名
    author_email='2018209921@qq.com',  # 作者邮箱
    packages=find_packages(),  # 自动查找包目录
    # install_requires=['requests'],  # 依赖库列表 (如果需要)
)