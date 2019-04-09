from flask import Flask, request, render_template
import os
import subprocess
import sys
app = Flask(__name__)

from subprocess import PIPE, Popen


def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        stderr=PIPE,
        shell=True
    )
    return '\n'.join([x.decode() for x in process.communicate()])

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        url = request.form.get('ans')
        url = url.replace(';', '')
        url = url.replace('|', '')
        url = url.replace('&', '')
        url = url.replace('>', '')
        url = url.replace('<', '')
        ans = str(cmdline('curl {}'.format(url)))
        ans = ans.replace('\\n', '\n').split('\n')
        return render_template('kek.html', ans=ans)
    else:
        return render_template('kek.html')


app.run(host='0.0.0.0')
