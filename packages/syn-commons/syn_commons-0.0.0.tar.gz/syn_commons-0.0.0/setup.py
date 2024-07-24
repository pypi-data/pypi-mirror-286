from setuptools import find_packages, setup

setup(
    name='syn-commons',
    version='0.0.0',
    author='Alvin',
    author_email='alvin@example.com',
    description='A placeholder package to prevent public package prioritization',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://example.com/syn-commons',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
)

