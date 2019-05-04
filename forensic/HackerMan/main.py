from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    secret = 'e9a40c0d861499b1db890399a04185b1'
    if request.args.get('secret') == secret:
        return "shadowctf{H1st0ry_1nf0Rmat1oN_sh0uld_b3_s3cUr3_s3c0nd_v3R5i0n}"
    return "shadowctf{NO_FLAG_FOR_YOU} (It's not flag, really)"


if __name__ == "__main__":
    app.run()
