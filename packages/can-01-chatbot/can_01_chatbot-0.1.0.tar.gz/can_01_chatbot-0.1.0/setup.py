from setuptools import setup, find_packages

setup(
    name='can_01_chatbot',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'openai',
        'pyaudio',
        'six',
        'google-cloud-speech',
        'google-cloud-texttospeech',
        'pydub'
    ],
    entry_points={
        'console_scripts': [
            'can_chatbot=can_01_chatbot.can01:main',  
        ],
    },
    author='Michelle Li',
    author_email='lmxmichelle.l@gmail.com',
    description='A chatbot project that uses OpenAI, Google Cloud Speech-to-Text, and Text-to-Speech APIs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Mich404elle/Michelle', 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
