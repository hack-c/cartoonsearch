from setuptools import setup, find_packages

setup(
    name='cartoonsearch',
    version='0.1',
    author="Charlie Hack",
    author_email="charles.t.hack@gmail.com",
    description="improved semantic search engine for TNY cartoons",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'tqdm',
        'click',
        'annoy',
        'pandas',
        'gensim',
        'unidecode',
        'scikit-learn',
    ],
)


