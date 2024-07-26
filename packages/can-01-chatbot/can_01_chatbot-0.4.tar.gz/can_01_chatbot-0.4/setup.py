from setuptools import setup, find_packages

setup(
    name='can_01_chatbot',
    version='0.4',  # Update this version number to 0.4
    packages=find_packages(),
    install_requires=[
        'openai',
        'pyaudio',
        'pydub',
        'google-cloud-speech',
        'google-cloud-texttospeech',
        'six',
        'python-dotenv'
    ],
    include_package_data=True,
    description='A chatbot that responds in Cantonese using OpenAI and Google Cloud services.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/can_01_chatbot',  # Optional
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)


