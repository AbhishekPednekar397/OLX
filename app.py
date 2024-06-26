# import flask 

from flask import Flask,render_template,request
import sqlite3
import json
import pickle

app = Flask(__name__)


@app.route('/')                    # redirects to the homepage
def homepage():
    return render_template("home.html")    

@app.route('/contact', methods = ["GET","POST"]) 
def contactus():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        country = request.form.get("country")
        state = request.form.get("state")
        message = request.form.get("message")
        print(name,email,country,state,message)
        conn = sqlite3.connect('contactus.db')
        cur = conn.cursor()
        cur.execute(f'''
        INSERT INTO CONTACT VALUES(
                    "{name}","{email}",
                    "{country}","{state}",
                    "{message}"
        )
        ''')
        conn.commit()
        return render_template('message.html')
    else:
        return render_template('contactus.html')

@app.route("/check", methods = ["GET","POST"])
def predict():
    if request.method == "POST":
        make = request.form.get("make")
        model = request.form.get("model")
        year = request.form.get("year")
        kms_driven = request.form.get("kms_driven")
        fuel = request.form.get("fuel")
        reg_city = request.form.get("registration_city")
        car_documents = request.form.get("car_documents")
        assembly = request.form.get("assembly")
        transmission = request.form.get("transmission")
        print(make,model,year,kms_driven,fuel,reg_city,car_documents,assembly,transmission)

        with open("encdata.json","r") as file:
            data = json.load(file)
        make_enc = int(data["Make"][make])
        model_enc = int(data["Model"][model])
        fuel_enc = int(data["Fuel"][fuel])
        regcity_enc = int(data["Registration city"][reg_city])
        cardocuments_enc = int(data["Car documents"][car_documents])
        assembly_enc = int(data["Assembly"][assembly])
        transmission_enc = int(data["Transmission"][transmission])
        print(make_enc,model_enc,fuel_enc,regcity_enc,cardocuments_enc,assembly_enc,transmission_enc)
        file.close()

        with open("model.pickle","rb") as model:
            mymodel = pickle.load(model)
        res = mymodel.predict([[int(year),int(kms_driven),int(make_enc),int(model_enc),int(fuel_enc),int(regcity_enc),int(cardocuments_enc),int(assembly_enc),int(transmission_enc)]])
        print(res[0])
        return render_template('result.html', result = "Rs. " + str(int(res[0]*0.3)))

    else:
        return render_template('predict1.html')

if __name__ == '__main__':
    app.run()
