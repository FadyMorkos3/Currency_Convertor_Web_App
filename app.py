from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            from_currency = request.form["from"].upper()
            to_currency = request.form["to"].upper()

            api_key = os.getenv("API_KEY")
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{to_currency}/{amount}"
            response = requests.get(url).json()
            print("API Response:", response)

            if response["result"] == "success":
                converted = response["conversion_result"]
                result = f"{amount} {from_currency} = {converted:.2f} {to_currency}"
            else:
                result = "Conversion failed. Please check your input or try again later."
        except Exception as e:
            result = f"Error: {str(e)}"
            print("Error:", e)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)

