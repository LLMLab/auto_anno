from setuptools import setup, find_packages


setup(
    name='auto_anno_2',
    version='0.1.3',
    packages=find_packages(),
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
