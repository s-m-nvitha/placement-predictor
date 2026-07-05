from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)


@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    cgpa = None
    iq = None

    if request.method == 'POST':
        try:
            cgpa = float(request.form['cgpa'])
            iq = float(request.form['iq'])

            # Input validation
            if cgpa < 4 or cgpa > 10:
                prediction = "Please enter a CGPA between 4 and 10."

            elif iq < 60 or iq > 160:
                prediction = "Please enter an IQ between 60 and 160."

            else:
                features = np.array([[cgpa, iq]])
                result = model.predict(features)[0]

                if result == 1:
                    prediction = "Likely to be Placed"
                else:
                    prediction = "Not Likely to be Placed"

        except ValueError:
            prediction = "Please enter valid numeric values."

    return render_template(
        "index.html",
        prediction=prediction,
        cgpa=cgpa,
        iq=iq
    )


if __name__ == "__main__":
    app.run(debug=True)