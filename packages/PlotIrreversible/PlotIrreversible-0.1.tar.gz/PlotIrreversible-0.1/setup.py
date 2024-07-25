from setuptools import setup

setup( name='PlotIrreversible',
       version='0.01',
       author='Kyle Mills',
       author_email="kyle.mills@irreversible.tech",
       description="Set matplotlib style to conform with Irreversible's brand policies",
       packages=['plotirr', 'plotirr.report_maker'],
       install_requires=['tabulate', 'matplotlib>=3.1.0', 'gif', 'tqdm', 'numpy'],
       include_package_data=True
    )
