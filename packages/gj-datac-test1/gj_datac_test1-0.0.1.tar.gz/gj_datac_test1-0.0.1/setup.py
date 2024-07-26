from setuptools import setup, find_packages


with open('description_info.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gj_datac_test1',  # 你的包名
    version='0.0.1',  # 版本号
    description='测试包1',  # 包的简要描述
    long_description=long_description,  # 包的详细描述
    long_description_content_type='text/markdown',  # 描述文件的类型
    # include_package_data=True,  # 包含包数据
    author='yin',  # 作者姓名
    author_email='2018209921@qq.com',  # 作者邮箱
    packages=find_packages(),  # 自动查找包目录
    python_requires='>3.6',  # 依赖库列表
    # install_requires=['requests'],  # 依赖库列表 (如果需要)
)