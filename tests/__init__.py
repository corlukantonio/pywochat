import sys
from os.path import abspath, dirname, sep

path = dirname(dirname(abspath(__file__)))
assert path.split(sep)[-1].lower() == 'pywochat'
sys.path.append(path)
print('Folder \'pywochat\' appended to path: {0}'.format(path))
