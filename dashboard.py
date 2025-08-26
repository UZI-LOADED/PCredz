from flask import Flask, render_template_string, request, jsonify
from threading import Thread
import queue

app = Flask(__name__)
creds_queue = queue.Queue()
creds_list = []

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PCredz Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #222; color: #eee; }
        h1 { color: #6cf; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #444; padding: 8px; text-align: left; }
        th { background: #333; }
        tr:nth-child(even) { background: #2a2a2a; }
    </style>
</head>
<body>
    <h1>PCredz Credential Dashboard</h1>
    <table>
        <thead>
            <tr><th>Credential</th><th>Time</th></tr>
        </thead>
        <tbody id="creds">
        </tbody>
    </table>
    <script>
        async function fetchCreds() {
            const res = await fetch('/api/creds');
            const data = await res.json();
            let html = '';
            for (let c of data) {
                html += `<tr><td>${c.cred}</td><td>${c.time}</td></tr>`;
            }
            document.getElementById('creds').innerHTML = html;
        }
        setInterval(fetchCreds, 2000);
        fetchCreds();
    </script>
</body>
</html>
'''

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/creds', methods=['GET'])
def get_creds():
    return jsonify(creds_list[-100:])  # limit to last 100 creds

@app.route('/api/creds', methods=['POST'])
def post_cred():
    data = request.json
    if data and 'cred' in data:
        creds_list.append({'cred': data['cred'], 'time': data.get('time', '')})
        return '', 204
    return 'Bad Request', 400

def run_dashboard():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    Thread(target=run_dashboard).start()
