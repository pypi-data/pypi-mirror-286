from setuptools import setup, find_packages

setup(
    name='wordocx',
    version='1.0.4',
    packages=find_packages(),
    description='A simple docx manipulation utility library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ashad Mohamed',  # Replace with your name
    author_email='deigott@proton.me',  # Replace with your email
    url='https://github.com/deigott/wordocx',  # Replace with the URL of your project
    install_requires=[
        'python-docx>=0.8.10',
        'docx2python>=1.27.0',
        # 'jsonlib-python3>=1.6.1'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
