from setuptools import setup

with open('requirements.txt') as reqs:
    requirements = filter(lambda r: r!='',
                          map(lambda r: r.strip(),
                              reqs))

setup(name='PyABICodec',
      version='1.0',
      description='A Codec for the Ethereum ABI.',
      author='ChrisCalderon',
      author_email='calderon.christian760@gmail.com',
      packages=['abicodec'],
      install_requires=requirements)
