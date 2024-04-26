from flask import Flask, Response, render_template_string, jsonify, request
import json
import time
import random

app = Flask(__name__)

# Simulated vote counter
votes = {
    "option_a": 0,
    "option_b": 0
}

# HTML template for the main page
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Real-Time Vote Counter</title>
    <script>
        // Function to establish a connection with the server and listen for updates
        function setupEventSource() {
            const eventSource = new EventSource('/vote_stream');
            eventSource.onmessage = function(e) {
                // Parse the data received from the server
                const data = JSON.parse(e.data);
                // Update the vote counts on the page
                document.getElementById('votes-option-a').textContent = data.option_a;
                document.getElementById('votes-option-b').textContent = data.option_b;
            };
        }

        // Function to send a vote for option A
        function voteA(amount) {
            fetch('/vote_a?amount=' + amount);
        }

        // Function to send a vote for option B
        function voteB(amount) {
            fetch('/vote_b?amount=' + amount);
        }
    </script>
</head>
<body onload="setupEventSource()">
    <h1>Real-Time Vote Counter</h1>
    <div>
        <p>Votes for Option A: <span id="votes-option-a">0</span></p>
        <button onclick="voteA(1)">Vote +1 for Option A</button>
        <button onclick="voteA(10)">Vote +10 for Option A</button>
        <p>Votes for Option B: <span id="votes-option-b">0</span></p>
        <button onclick="voteB(1)">Vote +1 for Option B</button>
        <button onclick="voteB(10)">Vote +10 for Option B</button>
    </div>
</body>
</html>
"""

# Route for the main page
@app.route('/')
def index():
    return render_template_string(html_template)

# Route for the SSE stream
@app.route('/vote_stream')
def vote_stream():
    def generate():
        while True:
            # Simulate vote count changes
            data = json.dumps(votes)
            # Yield a server-sent event with the data
            yield f"data: {data}\n\n"
            # Wait for 1 second before sending the next event
            time.sleep(1)
    # Return a streaming response with the event stream
    return Response(generate(), mimetype='text/event-stream')

# Route to simulate a vote for option A
@app.route('/vote_a')
def vote_a():
    amount = int(request.args.get('amount', 1))
    votes['option_a'] += amount
    return jsonify(success=True)

# Route to simulate a vote for option B
@app.route('/vote_b')
def vote_b():
    amount = int(request.args.get('amount', 1))
    votes['option_b'] += amount
    return jsonify(success=True)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
