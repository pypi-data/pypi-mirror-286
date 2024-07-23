from setuptools import setup

setup(name='tiana-sis',
      version='0.0.1',
      description='TIANA: Tool for Inference of Anomalies found by a Neural network Algorithm',
      url='https://github.com/stelais/tiana',
      author='Stela IS, TIANA authors',
      author_email='stela.ishitanisilva@nasa.gov',
      license='MIT',
      packages=['file_organizers',
                'metrics_plotter'],
      platforms="Mac OS 14.5",
      keywords=['Astronomy', 'Microlensing', 'Science', 'Neural Networks'],
      zip_safe=False,
      install_requires=["numpy>=1.26.2",
                        "pandas>=2.1.4",
                        "matplotlib>=3.8.3",
                        "bokeh>=3.1.0",
                        "scikit-learn>=1.4.1",
                        "tqdm>=4.66.1"
                        ])