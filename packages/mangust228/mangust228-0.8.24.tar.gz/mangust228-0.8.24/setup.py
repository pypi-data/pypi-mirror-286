from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

extras = {
    'repo': ['sqlalchemy'],
    'parsed': ['aiofiles', 'aiocsv'],
    'proxy': ['httpx'],
    'saver': ['aiofiles', 'nanoid'],
    'ua': []
}

extras['all'] = sum(extras.values(), [])

setup(
    name="mangust228",
    version="0.8.24",
    description="Lazy utils each I use sometimes",
    author="mangust228",
    author_email="bacek.mangust@gmail.com",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mangustik228/proxy_manager',
    install_requires=[],
    extras_require=extras,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    test_suite='tests',
    python_requires='>=3.9'
)
