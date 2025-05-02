from flask import Flask, render_template, request, stream_with_context, Response
import ollama

app = Flask(__name__)
client = ollama.Client()
MODEL = "gemma3:1b"

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route('/stream', methods=["POST"])
def stream():
    city = request.form.get("city")
    days = request.form.get("days")
    budget = request.form.get("budget")
    selected_activities = request.form.getlist('activities')
    prompt = (
        f"Voglio visitare {city} in {days} giorni. Crea un itinerario. "
        f"Il mio budget è {budget} e voglio fare le seguenti attività:"
        f"{', '.join(selected_activities) if selected_activities else 'varie'}"
    )

    def generate():
     for chunk in client.generate(model=MODEL, prompt=prompt, stream=True):
        clean = chunk['response'].replace('**', '').replace('\n', '<br>')
        yield f"data: {clean}\n\n"

    return Response(stream_with_context(generate()), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)