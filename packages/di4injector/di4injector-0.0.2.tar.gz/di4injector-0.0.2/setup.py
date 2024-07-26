from setuptools import setup, find_packages


with open('README.md', encoding='utf-8') as f:
    readme = f.read()


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name='di4injector',
    version='0.0.2',
    author='taiyo tamura',
    author_email='gtaiyou24@gmail.com',
    description='DI for injector',
    long_description=readme,
    url='https://github.com/gtaiyou24/di4injector',
    long_description_content_type='text/markdown',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=_requires_from_file('requirements.txt'),
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"]
)
