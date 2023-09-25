from setuptools import setup, find_packages


setup(
    name='auto_anno_2',
    version='0.1.6',
    packages=find_packages(),
    # 仓库地址
    url='https://github.com/LLMLab/auto_anno',
    # 作者
    author="LLMLab",
    # 作者邮箱
    author_email="541182180@qq.com",
    # 描述
    description='auto_anno_2',
    # 项目主页
    project_urls={
        "Bug Tracker": "https://github.com/LLMLab/auto_anno",
        "Documentation": "https://github.com/LLMLab/auto_anno",
        "Source Code": "https://github.com/LLMLab/auto_anno",
    },
    # 项目分类
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    # 关键字
    keywords='auto_anno_2',
    # 安装依赖
    install_requires=[
        # list your project dependencies here
        'erniebot==0.3.1'
    ],
)

# python setup.py sdist bdist_wheel # 打包
# pip install dist/auto_anno_2-*-py3-none-any.whl # 本地安装，包名调整为打包出的包名
# twine upload dist/* # 上传到pypi
# pip install auto_anno_2 -U -i https://pypi.org/simple # 从pypi安装
# pip list|grep auto # 查看安装的包
# pip uninstall auto_anno_2 # 卸载包
