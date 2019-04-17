from flask import Flask, request, render_template
from subprocess import PIPE, Popen
from threading import Timer


app = Flask(__name__)


def cmdline(command):
    proc = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    timer = Timer(5, proc.kill)
    try:
        timer.start()
        ans = proc.communicate()
        return '\n'.join([x.decode() for x in ans])
    finally:
        timer.cancel()


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
