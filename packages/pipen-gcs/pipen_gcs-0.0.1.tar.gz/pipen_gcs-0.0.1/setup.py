# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipen_gcs']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-storage>=2.17.0,<3.0.0', 'pipen>=0.15.0,<0.16.0']

entry_points = \
{'pipen': ['gcs = pipen_gcs:PipenGcsPlugin']}

setup_kwargs = {
    'name': 'pipen-gcs',
    'version': '0.0.1',
    'description': 'A plugin for pipen to handle file metadata in Google Cloud Storage',
    'long_description': '# pipen-gcs\n\nA plugin for [pipen][1] to handle files in Google Cloud Storage\n\n## Installation\n\n```bash\npip install -U pipen-gcs\n\n# uninstall to disable\npip uninstall pipen-gcs\n```\n\n## Usage\n\n```python\nfrom pipen import Proc, Pipen\n\nclass MyProc(Proc):\n    input = "infile:file"\n    input_data = ["gs://bucket/path/to/file"]\n    output = "outfile:file:gs://bucket/path/to/output"\n    script = "cat {{infile}} > {{outfile}}"\n\nclass MyPipen(Pipen):\n    starts = MyProc\n    # input files/directories will be downloaded to /tmp\n    # output files/directories will be generated in /tmp and then uploaded\n    #   to the cloud storage\n    plugin_opts = {"gcs_localize": "/tmp"}\n\nif __name__ == "__main__":\n    MyPipen().run()\n```\n\nYou can also disable localization, then you will have to handle the\ncloud storage files yourself.\n\n```python\nfrom pipen import Proc, Pipen\n\nclass MyProc(Proc):\n    input = "infile:file"\n    input_data = ["gs://bucket/path/to/file"]\n    output = "outfile:file:gs://bucket/path/to/output"\n    script = "gsutil cp {{infile}} {{outfile}}"\n\nclass MyPipen(Pipen):\n    starts = MyProc\n    plugin_opts = {"gcs_localize": False}\n\nif __name__ == "__main__":\n    MyPipen().run()\n```\n\n## Configuration\n\n- `gcs_localize`: The directory to localize the cloud storage files. If\n  set to `False`, the files will not be localized. Default is `False`.\n- `gcs_credentials`: The path to the Google Cloud Service Account\n  credentials file.\n\n[1]: https://github.com/pwwang/pipen\n',
    'author': 'pwwang',
    'author_email': '1188067+pwwang@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
