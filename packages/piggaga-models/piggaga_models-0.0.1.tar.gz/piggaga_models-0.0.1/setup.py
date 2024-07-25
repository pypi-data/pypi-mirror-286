from setuptools import setup, find_packages

# 读取README.md文件内容
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='piggaga_models',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'tqdm',
        'rich'
    ],
    entry_points={
        'console_scripts': [
            'piggaga_models = piggaga_models.piggaga_models:download_google_images',
        ],
    },
    author='豬嘎嘎',
    author_email='piggaga.company@gmail.com',
    description='piggaga_models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/piggaga/piggaga',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
