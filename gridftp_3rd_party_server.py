from flask import Flask,request
import os,mysql.connector

app = Flask(__name__)
ID = 'Change it to mysql ID'
PW = 'Change it to mysql PW'


@app.route("/info")
def info():
    cnx = mysql.connector.connect(user=ID,password=PW,host='127.0.0.1',database='test')
    cur = cnx.cursor()
    cur.execute("SELECT * FROM tbl_DTN;")
    rv = cur.fetchall()
    cnx.close()
    return str(rv)

@app.route("/log")
def log():
    cnx = mysql.connector.connect(user=ID,password=PW,host='127.0.0.1',database='test')
    cur = cnx.cursor()
    cur.execute("SELECT * FROM testlog2;")
    rv = cur.fetchall()
    cnx.close()
    return str(rv)
    
@app.route("/transfer", methods=["GET","POST"])
def transfer():
    content = request.json
    Source = content['Source']
    Dest = content['Dest']
    if request.method == "POST":
        a=os.popen("globus-url-copy -vb ftp://"+Source+" ftp://"+Dest).read()
        if a.split()[len(a.split())-7]=="bytes":
            rate=float(a.split()[len(a.split())-6])
            size=float(a.split()[len(a.split())-8]) / 1048576
            time=size/rate
        else :
            rate=0
            size=0
            time=0
        cnx = mysql.connector.connect(user=ID,password=PW,host='127.0.0.1',database='test')
        cur = cnx.cursor()
        i=0
        while i<len(a.split()) and a.split()[i]=="Source:":
            source=a.split()[i+1]
            dest=a.split()[i+3]
            data=a.split()[i+4]
            cur.execute("insert into testlog2 value(null,now(),'"+source+"','"+dest+"','"+data+"',"+str(rate)+","+str(size)+","+str(time)+");")
            i=i+5
        cnx.commit()
        cnx.close()
        return "%s" %a
    else:
        a=os.popen("globus-url-copy -list ftp://"+Source).read()+os.popen("globus-url-copy -list ftp://"+Dest).read()
        return "%s" %a

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=22641,debug=None)
