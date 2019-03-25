import os
import shutil
import tarfile
import zipfile

import tqdm

COUNT = 1337


def decode_zip(filename):
    with zipfile.ZipFile(filename, 'r') as f:
        f.extractall(path='.')


def decode_tar_gz(filename):
    with tarfile.open(filename, 'r:gz') as f:
        f.extractall(path='.')


def decode_tar_xz(filename):
    with tarfile.open(filename, 'r:xz') as f:
        f.extractall(path='.')


if os.path.exists('temp'):
    shutil.rmtree('temp')

os.mkdir('temp')
shutil.copy('result', f'temp/result_{COUNT}')

for i in tqdm.tqdm(range(COUNT, 0, -1)):
    cur = f'temp/result_{i}'
    check = os.popen(f'file {cur}').read()
    if 'gzip' in check:
        decode_tar_gz(cur)
    elif 'Zip' in check:
        decode_zip(cur)
    elif 'XZ' in check:
        decode_tar_xz(cur)
    else:
        print(check)
        os._exit(1)

shutil.move(f'temp/result_0', 'flag.test')
shutil.rmtree('temp')
