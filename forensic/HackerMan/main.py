from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    secret = '665248b6b28be8ace6e0edccc400e4ce'
    if request.args.get('secret') == secret:
        return "shadowctf{H1st0ry_1nf0Rmat1oN_sh0uld_b3_s3cUr3}"
    return "shadowctf{NO_FLAG_FOR_YOU} (It's not flag, really)"


if __name__ == "__main__":
    app.run()
