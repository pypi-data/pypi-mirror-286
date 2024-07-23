from setuptools import setup, find_packages

setup(
    name='textevaluator',
    version='0.1',
    packages=find_packages(),
    package_data={'textevaluator': ['data/my_model.h5', 'data/data.json']},
    install_requires=[
        'tensorflow',
        'nltk'
    ],
    entry_points={
        'console_scripts': [
            'textevaluator=textevaluator:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='A text evaluation module using TensorFlow',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_project',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
