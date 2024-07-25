from setuptools import setup

 

setup(
    name='DIAL_API_THULASI2024',
    version='1.0.0',
    author='Kadiyala Thulasi Ram',
    author_email='thulasiramchowdary1999@gmail.com',
    description='Dail_API',
    packages=['device_config'],
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'argparse',  # Example dependency, adjust according to your requirements
        'ncclient',
        'xmltodict',
        'langchain_google_genai',
        'langchain',
        # List any other dependencies your module requires
    ],
)
