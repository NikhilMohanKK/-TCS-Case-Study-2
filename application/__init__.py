from flask import Flask,render_template,redirect,request, url_for,flash
import yaml
from flask_mysqldb import MySQL







app=Flask(__name__)
mysql = MySQL(app)
app.secret_key = "super secret key"
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


@app.route('/',methods=['GET', 'POST'])
@app.route('/Create_Patient',methods=['GET', 'POST'])
def createpatient():
    if request.method=="POST":
        ssn_id=request.form.get('ssn_id')
        patient_name=request.form.get('patient_name')
        patient_age=request.form.get('patient_age')
        date_of_admission=request.form.get('date_of_admission')
        bed_type=request.form.get('bed_type').split(' ')[0]
        address=request.form.get('address')
        city=request.form.get('city')
        state=request.form.get('state')
        cur = mysql.connection.cursor()
        print(address)
        z=cur.execute("SELECT * FROM patient WHERE ws_ssn= %s",[ssn_id])
        if(len(ssn_id)==9 and z==0):
            cur.execute("insert into patient(ws_ssn,ws_pat_name,ws_age,ws_adrs,ws_doj,ws_rtype,city,state,status) values (%s,%s,%s,%s,%s,%s,%s,%s,'Active')",(ssn_id,patient_name,patient_age,address,date_of_admission,bed_type,city,state))
            mysql.connection.commit()
            cur.close()
            return "Patient Created Successfully"
    return render_template('02 Create Patient.html')



@app.route('/Update_Patient',methods=['GET', 'POST'])
def updatepatient():
    if request.method=="POST":
        if "patient_id" in request.form:
            pid=request.form.get('pid')
            cur = mysql.connection.cursor()
            z=cur.execute("SELECT * FROM patient WHERE ws_pat_id= %s",[pid])
            if z>0:
                cust = cur.fetchone()
                print(cust[7])
                return render_template('03 Update Patient.html',data=cust)
        else:
            ssn_id=request.form.get('ssn_id')
            if ssn_id !=None:
                patient_name=request.form.get('patient_name')
                patient_age=request.form.get('patient_age')
                date_of_admission=request.form.get('date_of_admission')
                bed_type=request.form.get('bed_type').split(' ')[0]
                address=request.form.get('address')
                city=request.form.get('city')
                state=request.form.get('state')
                cur = mysql.connection.cursor()
                print(address)
                queryres=cur.execute("SELECT * FROM patient WHERE ws_ssn= %s",[ssn_id])
                if(len(ssn_id)==9 and queryres!=0):
                    fetchvalue=cur.fetchone()
                    cur.execute("update patient set ws_pat_name=%s,ws_age=%s,ws_adrs=%s,ws_doj=%s,ws_rtype=%s,city=%s,state=%s,status=%s where ws_ssn=%s",[patient_name,patient_age,address,date_of_admission,bed_type,city,state,fetchvalue[9],ssn_id])
                    mysql.connection.commit()
                    cur.close()
                    return "Patient Updated Successfully"
                else:
                    return "No Patient Exists"
            else:
                return "No Patient Exists"
    return render_template('03 Update Patient.html',data=None)



@app.route('/Delete_Patient',methods=['GET', 'POST'])
def deletepatient():
    if request.method=="POST":
        if "patient_id" in request.form:
            pid=request.form.get('pid')
            cur = mysql.connection.cursor()
            z=cur.execute("SELECT * FROM patient WHERE ws_pat_id= %s",[pid])
            if z>0:
                cust = cur.fetchone()
                print(cust)
                return render_template('04 Delete Patient.html',data=cust)
        else:
            ssn_id=request.form.get('ssn_id')
            if ssn_id !=None:
                cur = mysql.connection.cursor()
                queryres=cur.execute("SELECT * FROM patient WHERE ws_ssn= %s",[ssn_id])
                if(len(ssn_id)==9 and queryres!=0):
                    cur.execute("delete from patient where ws_ssn=%s",[ssn_id])
                    mysql.connection.commit()
                    cur.close()
                    return "Patient Record Deleted Successfully"
                else:
                    return "No Patient Exists"
            else:
                    return "No Patient Exists"
    return render_template('04 Delete Patient.html',data=None)


app.route("/View_Patient")
def view_page(data = None):
    cur = mysql.connection.cursor()
    cur.execute("Select * from patient where status= %s" , ("Active",))
    result=cur.fetchall()
    data=list(list())
    for x in result:
        data.append(list(x)) 
    return render_template("06 View Patients.html", data =data)


@app.route("/Search_Patient")
def Search_Patient(data = None):        
    cur = mysql.connection.cursor()
    entered_id= request.args.get('patient_id')
    if(entered_id):
        cur.execute("Select * from patient where ws_pat_id = " + str(entered_id) )
        result = cur.fetchone()
        if result:
            data = list(result)   
            return render_template("05 Search Patient.html", data = data)
        else:
            flash("No patient with that ID!")
            return redirect("/Search_Patient")
    return render_template("05 Search Patient.html", data=data)


if __name__=="__main__":
    app.run(debug=False)