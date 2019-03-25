import os
import random
import shutil
import tarfile
import zipfile

import tqdm

COUNT = 1337


def encode_zip(filename, result):
    with zipfile.ZipFile(result, 'w') as f:
        f.write(filename)


def encode_tar_gz(filename, result):
    with tarfile.open(result, 'w:gz') as f:
        f.add(filename)


def encode_tar_xz(filename, result):
    with tarfile.open(result, 'w:xz') as f:
        f.add(filename)


encoders = [encode_zip, encode_tar_xz, encode_tar_gz]

if os.path.exists('temp'):
    shutil.rmtree('temp')

os.mkdir('temp')
shutil.copy('flag.txt', 'temp/result_0')

for i in tqdm.tqdm(range(COUNT)):
    func = random.choice(encoders)
    func(f'temp/result_{i}', f'temp/result_{i + 1}')
    os.remove(f'temp/result_{i}')

shutil.move(f'temp/result_{COUNT}', 'result')
shutil.rmtree('temp')
