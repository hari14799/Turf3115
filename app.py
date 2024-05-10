from flask import Flask,render_template,url_for,redirect,session,request,flash
from flask_mysqldb import MySQL
from flask_mail import Mail,Message


app=Flask(__name__)

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="sakthi"
app.config["MYSQL_DB"]="admin"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)

@app.route("/")
def index():
     return render_template("index.html")    
   

@app.route("/login",methods=["GET","POST"])
def ulogin():
    if 'ulogin' in request.form:
          if request.method=="POST":
               uemail=request.form["uemail"]
               upwd=request.form["upwd"]
               
               try:
                    cur=mysql.connection.cursor()
                    cur.execute("select * from  users where mail=%s and upassword=%s",[uemail,upwd])
                    res=cur.fetchone()
                    
                    if res:
                         
                         session ["uname"]=res["uname"]
                         session ["uid"]=res["uid"]
                         session ["umail"]=res["mail"]
                         return redirect(url_for("userdetails",id=session["uid"]))
                    else:
                         flash("INVALID CREDENTIALS")
                         return render_template("login.html")
                     
               except Exception as e:
                    print(e)
                    
               finally:
                    mysql.connection.commit()
                    cur.close()    
                       
    return render_template("login.html")                 

@app.route("/register",methods=["GET","POST"])
def uregister():
     if 'uregister' in request.form:
          if request.method=="POST":
               uname=request.form["uname"]
               password=request.form["upass"] 
               
               address=request.form["uaddr"]
               contact=request.form["ucontact"]
               umail=request.form["umail"]
               cur=mysql.connection.cursor()
               cur.execute('insert into users(uname,upassword,uaddr,contact,mail) values(%s,%s,%s,%s,%s)',[uname,password,address,contact,umail])
               mysql.connection.commit()
              
               
               app.config['MAIL_SERVER']='smtp.gmail.com'  
               app.config['MAIL_PORT']=465  
               app.config['MAIL_USERNAME'] ='sportsclub3115@gmail.com'
               app.config['MAIL_PASSWORD'] ='lkbq ewpe spbz qsya'
               app.config['MAIL_USE_TLS'] = False  
               app.config['MAIL_USE_SSL'] = True  
               mail=Mail(app) 

               msg=Message('WELCOME TO SPORTSCLUB TURF UNIVERSE',sender='sportsclub3115@gmail.com',recipients=[umail])    
               msg.body="REGISTERED SUCCESSFULLY"
                         
                         
               mail.send(msg)
               
         
               
          return render_template("login.html")         
     return render_template("register.html") 

@app.route("/admin",methods=["GET","POST"])
def admin():
                        
      if 'adminlogin' in request.form:  
         if request.method=="POST":
            adname=request.form["adminname"]
            adpwd=request.form["adminpwd"] 
            if (adname=="spoclub" and adpwd=="spo123"):
                 return redirect(url_for("admin"))                            
      
          
          
      cur=mysql.connection.cursor()
      sql="select * from users"
      cur.execute(sql)
      res=cur.fetchall()
      mysql.connection.commit()
      return render_template("admin.html",datas=res)







@app.route("/user/<string:id>")
def userdetails(id):
     cur=mysql.connection.cursor()
     sql="select * from booking where bid=%s" 
     cur.execute(sql,[id]) 
     res=cur.fetchall()    
     return render_template("user.html",datas=res)

@app.route("/logout")
def logout():
     session.clear()
     return redirect(url_for("index"))



@app.route("/contactus",methods=["POST","GET"])
def contact():
     if request.method=="POST":
          fmail=request.form.get('fmail')
         
          fpwd=request.form.get('fpwd')
          message=request.form.get('message')
          body=request.form.get('body')
          app.config['MAIL_SERVER']='smtp.gmail.com'  
          app.config['MAIL_PORT']=465  
          app.config['MAIL_USERNAME'] =fmail
          app.config['MAIL_PASSWORD'] =fpwd 
          app.config['MAIL_USE_TLS'] = False  
          app.config['MAIL_USE_SSL'] = True  
          
          mail=Mail(app) 

          msg=Message(message,sender=fmail,recipients=['sportsclub3115@gmail.com'])    
          msg.body=body
          mail.send(msg)
     return render_template("contactus.html")     
 
@app.route("/allsports")
def sports():
     return render_template("allsports.html")

@app.route("/cricket/<string:umail>",methods=["POST","GET"])
def cricket(umail):
      cur=mysql.connection.cursor()
      cur.execute("select * from  cricket where tdate=(select current_date() from dual) ")
      res=cur.fetchone()
      cur.close()
      
      con=mysql.connection.cursor()
      con.execute("select * from  cricket1 where tdate=(select current_date() from dual) ")
      res1=con.fetchone()
      con.close()
      
      
      
      
     
      if 'cricket' in request.form:
         if request.method=="POST":
           bookid=request.form["bid"]
           bookdate=request.form["bdate"]
           bookslot=request.form["btime"]
           sname=request.form["sport"]
           amount=request.form["amt"]
           
          
          
           cur=mysql.connection.cursor()
           cur.execute('insert into booking(bid,bdate,btime,sport,amount) values(%s,%s,%s,%s,%s)',[bookid,bookdate,bookslot,sname,amount])  
           mysql.connection.commit()
           
           app.config['MAIL_SERVER']='smtp.gmail.com'  
           app.config['MAIL_PORT']=465  
           app.config['MAIL_USERNAME'] ='sportsclub3115@gmail.com'
           app.config['MAIL_PASSWORD'] ='lkbq ewpe spbz qsya'
           app.config['MAIL_USE_TLS'] = False  
           app.config['MAIL_USE_SSL'] = True  
           mail=Mail(app) 

           msg=Message('WELCOME TO SPORTSCLUB TURF UNIVERSE',sender='sportsclub3115@gmail.com',recipients=[umail])    
           msg.body="YOUR SLOT HAS BEEN BOOKED SUCCESSFULLY"
            
           mail.send(msg)             
                         
             
               
               
          
           if bookslot=="05:00 AM - 06:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set FIVEAM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set FIVEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
           
           elif bookslot=="06:00 AM - 07:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set SIXAM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set SIXAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
           elif bookslot=="07:00 AM - 08:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set SEVENAM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set SEVENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
           elif bookslot=="08:00 AM - 09:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set EIGHTAM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set EIGHTAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
           elif bookslot=="09:00 AM - 10:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set NINEAM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set NINEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
           elif bookslot=="10:00 AM - 11:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set TENAM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set TENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
           elif bookslot=="11:00 AM - 12:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set ELEAM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set ELEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()             
           
           elif bookslot=="12:00 PM - 01:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set TWEPM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set TWEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()    

           elif bookslot=="01:00 PM - 02:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set ONEPM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set ONEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
           elif bookslot=="02:00 PM - 03:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set TWOPM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set TWOPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="03:00 PM - 04:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set THREEPM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set THREEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="04:00 PM - 05:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set FOURPM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set FOURPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="05:00 PM - 06:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set FIVEPM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set FIVEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="06:00 PM - 07:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set SIXPM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set SIXPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="07:00 PM - 08:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set SEVENPM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set SEVENPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="08:00 PM - 09:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set EIGHTPM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set EIGHTPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="09:00 PM - 10:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set NINEPM="red" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set NINEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
                      
           else :    
              cur=mysql.connection.cursor()
              cur.execute('update cricket set TENPM="red" where tdate=%s',[bookdate])
              cur.execute('update cricket1 set TENPM="hide" where tdate=%s',[bookdate])
              mysql.connection.commit()   
           return redirect(url_for("cricket", umail=session ["umail"]))  
         
      elif 'choosedate' in request.form:
          cdate=request.form["demo"]  
          cur=mysql.connection.cursor()
          cur.execute("select * from  cricket where tdate=%s",[cdate])
          res=cur.fetchone()
          
          con=mysql.connection.cursor()
          con.execute("select * from  cricket1 where tdate=%s",[cdate])
          res1=con.fetchone()
          con.close()
          return render_template("cricket.html",datas=res,seldate=cdate,values=res1,umail=umail)      
      return render_template("cricket.html",datas=res,values=res1,umail=umail)         


          
     
          
          
@app.route("/football/<string:umail>",methods=["POST","GET"])
def football(umail):
     
     cur=mysql.connection.cursor()
     cur.execute("select * from  football where tdate=(select current_date() from dual) ")
     res=cur.fetchone()
     cur.close()
     
     
     con=mysql.connection.cursor()
     con.execute("select * from  football1 where tdate=(select current_date() from dual) ")
     res1=con.fetchone()
     con.close()
    
          
     if 'football' in request.form:
      if request.method=="POST":
          bookid=request.form["bid"]
          bookdate=request.form["bdate"]
          bookslot=request.form["btime"]
          sname=request.form["sport"]
          amount=request.form["amt"]
     
          cur=mysql.connection.cursor()
          cur.execute('insert into booking(bid,bdate,btime,sport,amount) values(%s,%s,%s,%s,%s)',[bookid,bookdate,bookslot,sname,amount])  
          mysql.connection.commit()
          
          app.config['MAIL_SERVER']='smtp.gmail.com'  
          app.config['MAIL_PORT']=465  
          app.config['MAIL_USERNAME'] ='sportsclub3115@gmail.com'
          app.config['MAIL_PASSWORD'] ='lkbq ewpe spbz qsya'
          app.config['MAIL_USE_TLS'] = False  
          app.config['MAIL_USE_SSL'] = True  
          mail=Mail(app) 

          msg=Message('WELCOME TO SPORTSCLUB TURF UNIVERSE',sender='sportsclub3115@gmail.com',recipients=[umail])    
          msg.body="YOUR SLOT HAS BEEN BOOKED SUCCESSFULLY"
            
          mail.send(msg)             
                         
     
          if bookslot=="05:00 AM - 06:00 AM":
           cur=mysql.connection.cursor()
           cur.execute('update football set FIVEAM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set FIVEAM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit()
          
          elif bookslot=="06:00 AM - 07:00 AM":
           cur=mysql.connection.cursor()
           cur.execute('update football set SIXAM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set SIXAM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit()
          
          elif bookslot=="07:00 AM - 08:00 AM":
           cur=mysql.connection.cursor()
           cur.execute('update football set SEVENAM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set SEVENAM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit()
          
          elif bookslot=="08:00 AM - 09:00 AM":
           cur=mysql.connection.cursor()
           cur.execute('update football set EIGHTAM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set EIGHTAM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit()  
          
          elif bookslot=="09:00 AM - 10:00 AM":
           cur=mysql.connection.cursor()
           cur.execute('update football set NINEAM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set NINEAM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit()  
          
          elif bookslot=="10:00 AM - 11:00 AM":
           cur=mysql.connection.cursor()
           cur.execute('update football set TENAM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set TENAM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit()   
          
          elif bookslot=="11:00 AM - 12:00 PM":
           cur=mysql.connection.cursor()
           cur.execute('update football set ELEAM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set ELEAM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit()             
          
          elif bookslot=="12:00 PM - 01:00 PM":
           cur=mysql.connection.cursor()
           cur.execute('update football set TWEPM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set TWEPM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit()    

          elif bookslot=="01:00 PM - 02:00 PM":
           cur=mysql.connection.cursor()
           cur.execute('update football set ONEPM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set ONEPM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit()   
          
          elif bookslot=="02:00 PM - 03:00 PM":
           cur=mysql.connection.cursor()
           cur.execute('update football set TWOPM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set TWOPM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit() 
          
          elif bookslot=="03:00 PM - 04:00 PM":
           cur=mysql.connection.cursor()
           cur.execute('update football set THREEPM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set THREEPM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit() 
          
          elif bookslot=="04:00 PM - 05:00 PM":
           cur=mysql.connection.cursor()
           cur.execute('update football set FOURPM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set FOURPM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit() 
          
          elif bookslot=="05:00 PM - 06:00 PM":
           cur=mysql.connection.cursor()
           cur.execute('update football set FIVEPM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set FIVEPM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit() 
          
          elif bookslot=="06:00 PM - 07:00 PM":
           cur=mysql.connection.cursor()
           cur.execute('update football set SIXPM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set SIXPM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit() 
          
          elif bookslot=="07:00 PM - 08:00 PM":
           cur=mysql.connection.cursor()
           cur.execute('update football set SEVENPM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set SEVENPM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit() 
          
          elif bookslot=="08:00 PM - 09:00 PM":
           cur=mysql.connection.cursor()
           cur.execute('update football set EIGHTPM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set EIGHTPM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit() 
          
          elif bookslot=="09:00 PM - 10:00 PM":
           cur=mysql.connection.cursor()
           cur.execute('update football set NINEPM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set NINEPM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit() 
                    
          else :    
           cur=mysql.connection.cursor()
           cur.execute('update football set TENPM="red" where tdate=%s',[bookdate])
           cur.execute('update football1 set TENPM="hide" where tdate=%s',[bookdate])
           mysql.connection.commit()
          return redirect(url_for("football",umail=session ["umail"])) 
                    
     elif 'choosedate' in request.form:
          cdate=request.form["demo"]  
          cur=mysql.connection.cursor()
          cur.execute("select * from  football where tdate=%s",[cdate])
          res=cur.fetchone()
          cur.close()
          
          con=mysql.connection.cursor()
          con.execute("select * from  football1 where tdate=%s",[cdate])
          res1=con.fetchone()
          con.close()
          
          return render_template("football.html",datas=res,seldate=cdate,values=res1,umail=umail)  

          
     return render_template("football.html",datas=res,values=res1,umail=umail)
          
@app.route("/volleyball/<string:umail>",methods=["POST","GET"])
def volleyball(umail):
       
     cur=mysql.connection.cursor()
     cur.execute("select * from  volleyball where tdate=(select current_date() from dual) ")
     res=cur.fetchone()
     
     con=mysql.connection.cursor()
     con.execute("select * from  volleyball1 where tdate=(select current_date() from dual) ")
     res1=con.fetchone()
     con.close()
     if 'volleyball' in request.form: 
      if request.method=="POST":
          bookid=request.form["bid"]
          bookdate=request.form["bdate"]
          bookslot=request.form["btime"]
          sname=request.form["sport"]
          amount=request.form["amt"]
          
          cur=mysql.connection.cursor()
          cur.execute('insert into booking(bid,bdate,btime,sport,amount) values(%s,%s,%s,%s,%s)',[bookid,bookdate,bookslot,sname,amount])  
          mysql.connection.commit()
          
          app.config['MAIL_SERVER']='smtp.gmail.com'  
          app.config['MAIL_PORT']=465  
          app.config['MAIL_USERNAME'] ='sportsclub3115@gmail.com'
          app.config['MAIL_PASSWORD'] ='lkbq ewpe spbz qsya'
          app.config['MAIL_USE_TLS'] = False  
          app.config['MAIL_USE_SSL'] = True  
          mail=Mail(app) 

          msg=Message('WELCOME TO SPORTSCLUB TURF UNIVERSE',sender='sportsclub3115@gmail.com',recipients=[umail])    
          msg.body="YOUR SLOT HAS BEEN BOOKED SUCCESSFULLY"
            
          mail.send(msg)
          
          if bookslot=="05:00 AM - 06:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set FIVEAM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set FIVEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
           
          elif bookslot=="06:00 AM - 07:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set SIXAM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set SIXAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
          elif bookslot=="07:00 AM - 08:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set SEVENAM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set SEVENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
          elif bookslot=="08:00 AM - 09:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set EIGHTAM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set EIGHTAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
          elif bookslot=="09:00 AM - 10:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set NINEAM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set NINEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
          elif bookslot=="10:00 AM - 11:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set TENAM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set TENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
          elif bookslot=="11:00 AM - 12:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set ELEAM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set ELEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()             
           
          elif bookslot=="12:00 PM - 01:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set TWEPM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set TWEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()    

          elif bookslot=="01:00 PM - 02:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set ONEPM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set ONEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
          elif bookslot=="02:00 PM - 03:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set TWOPM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set TWOPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="03:00 PM - 04:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set THREEPM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set THREEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="04:00 PM - 05:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set FOURPM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set FOURPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="05:00 PM - 06:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set FIVEPM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set FIVEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="06:00 PM - 07:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set SIXPM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set SIXPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="07:00 PM - 08:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set SEVENPM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set SEVENPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="08:00 PM - 09:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set EIGHTPM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set EIGHTPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="09:00 PM - 10:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set NINEPM="red" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set NINEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
                      
          else :    
              cur=mysql.connection.cursor()
              cur.execute('update volleyball set TENPM="red" where tdate=%s',[bookdate])
              cur.execute('update volleyball1 set TENPM="hide" where tdate=%s',[bookdate])
              mysql.connection.commit()  
          return redirect(url_for("volleyball",umail=session ["umail"]))
      
     elif 'choosedate' in request.form:
          cdate=request.form["demo"]  
          cur=mysql.connection.cursor()
          cur.execute("select * from  volleyball where tdate=%s",[cdate])
          res=cur.fetchone()
          cur.close()
          
          con=mysql.connection.cursor()
          con.execute("select * from  volleyball1 where tdate=%s",[cdate])
          res1=con.fetchone()
          con.close()
          
          return render_template("volleyball.html",datas=res,seldate=cdate,values=res1,umail=umail)           


          
     return render_template("volleyball.html",datas=res,values=res1,umail=umail)      

@app.route("/basketball/<string:umail>",methods=["POST","GET"])
def basketball(umail):
       
     cur=mysql.connection.cursor()
     cur.execute("select * from  basketball where tdate=(select current_date() from dual) ")
     res=cur.fetchone()
     
     con=mysql.connection.cursor()
     con.execute("select * from  basketball1 where tdate=(select current_date() from dual) ")
     res1=con.fetchone()
     con.close()
     
     if 'basketball' in request.form: 
      if request.method=="POST":
          bookid=request.form["bid"]
          bookdate=request.form["bdate"]
          bookslot=request.form["btime"]
          sname=request.form["sport"]
          amount=request.form["amt"]
          
          cur=mysql.connection.cursor()
          cur.execute('insert into booking(bid,bdate,btime,sport,amount) values(%s,%s,%s,%s,%s)',[bookid,bookdate,bookslot,sname,amount])  
          mysql.connection.commit()
          
          app.config['MAIL_SERVER']='smtp.gmail.com'  
          app.config['MAIL_PORT']=465  
          app.config['MAIL_USERNAME'] ='sportsclub3115@gmail.com'
          app.config['MAIL_PASSWORD'] ='lkbq ewpe spbz qsya'
          app.config['MAIL_USE_TLS'] = False  
          app.config['MAIL_USE_SSL'] = True  
          mail=Mail(app) 

          msg=Message('WELCOME TO SPORTSCLUB TURF UNIVERSE',sender='sportsclub3115@gmail.com',recipients=[umail])    
          msg.body="YOUR SLOT HAS BEEN BOOKED SUCCESSFULLY"
            
          mail.send(msg)
          
          if bookslot=="05:00 AM - 06:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set FIVEAM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set FIVEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
           
          elif bookslot=="06:00 AM - 07:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set SIXAM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set SIXAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
          elif bookslot=="07:00 AM - 08:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set SEVENAM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set SEVENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
          elif bookslot=="08:00 AM - 09:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set EIGHTAM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set EIGHTAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
          elif bookslot=="09:00 AM - 10:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set NINEAM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set NINEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
          elif bookslot=="10:00 AM - 11:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set TENAM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set TENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
          elif bookslot=="11:00 AM - 12:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set ELEAM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set ELEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()             
           
          elif bookslot=="12:00 PM - 01:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set TWEPM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set TWEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()    

          elif bookslot=="01:00 PM - 02:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set ONEPM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set ONEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
          elif bookslot=="02:00 PM - 03:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set TWOPM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set TWOPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="03:00 PM - 04:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set THREEPM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set THREEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="04:00 PM - 05:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set FOURPM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set FOURPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="05:00 PM - 06:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set FIVEPM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set FIVEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="06:00 PM - 07:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set SIXPM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set SIXPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="07:00 PM - 08:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set SEVENPM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set SEVENPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="08:00 PM - 09:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set EIGHTPM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set EIGHTPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="09:00 PM - 10:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set NINEPM="red" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set NINEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
                      
          else :    
              cur=mysql.connection.cursor()
              cur.execute('update basketball set TENPM="red" where tdate=%s',[bookdate])
              cur.execute('update basketball1 set TENPM="hide" where tdate=%s',[bookdate])
              mysql.connection.commit() 
          return redirect(url_for("basketball",umail=session["umail"]))   
               
     elif 'choosedate' in request.form:
          cdate=request.form["demo"]  
          cur=mysql.connection.cursor()
          cur.execute("select * from  basketball where tdate=%s",[cdate])
          res=cur.fetchone()
          cur.close()
          
          con=mysql.connection.cursor()
          con.execute("select * from  basketball1 where tdate=%s",[cdate])
          res1=con.fetchone()
          con.close()
          
          return render_template("basketball.html",datas=res,seldate=cdate,values=res1,umail=umail) 

          
     return render_template("basketball.html",datas=res,values=res1,umail=umail)     


@app.route("/handball/<string:umail>",methods=["POST","GET"])
def handball(umail):
       
     cur=mysql.connection.cursor()
     cur.execute("select * from  handball where tdate=(select current_date() from dual) ")
     res=cur.fetchone()
     cur.close()
     
     con=mysql.connection.cursor()
     con.execute("select * from  handball1 where tdate=(select current_date() from dual) ")
     res1=con.fetchone()
     con.close()
     
     if 'handball' in request.form:    
      if request.method=="POST":
          bookid=request.form["bid"]
          bookdate=request.form["bdate"]
          bookslot=request.form["btime"]
          sname=request.form["sport"]
          amount=request.form["amt"]
          
          cur=mysql.connection.cursor()
          cur.execute('insert into booking(bid,bdate,btime,sport,amount) values(%s,%s,%s,%s,%s)',[bookid,bookdate,bookslot,sname,amount])  
          mysql.connection.commit()
          
          app.config['MAIL_SERVER']='smtp.gmail.com'  
          app.config['MAIL_PORT']=465  
          app.config['MAIL_USERNAME'] ='sportsclub3115@gmail.com'
          app.config['MAIL_PASSWORD'] ='lkbq ewpe spbz qsya'
          app.config['MAIL_USE_TLS'] = False  
          app.config['MAIL_USE_SSL'] = True  
          mail=Mail(app) 

          msg=Message('WELCOME TO SPORTSCLUB TURF UNIVERSE',sender='sportsclub3115@gmail.com',recipients=[umail])    
          msg.body="YOUR SLOT HAS BEEN BOOKED SUCCESSFULLY"
            
          mail.send(msg)
          
          if bookslot=="05:00 AM - 06:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set FIVEAM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set FIVEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
           
          elif bookslot=="06:00 AM - 07:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set SIXAM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set SIXAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
          elif bookslot=="07:00 AM - 08:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set SEVENAM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set SEVENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
          elif bookslot=="08:00 AM - 09:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set EIGHTAM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set EIGHTAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
          elif bookslot=="09:00 AM - 10:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set NINEAM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set NINEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
          elif bookslot=="10:00 AM - 11:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set TENAM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set TENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
          elif bookslot=="11:00 AM - 12:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set ELEAM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set ELEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()             
           
          elif bookslot=="12:00 PM - 01:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set TWEPM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set TWEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()    

          elif bookslot=="01:00 PM - 02:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set ONEPM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set ONEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
          elif bookslot=="02:00 PM - 03:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set TWOPM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set TWOPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="03:00 PM - 04:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set THREEPM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set THREEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="04:00 PM - 05:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set FOURPM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set FOURPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="05:00 PM - 06:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set FIVEPM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set FIVEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="06:00 PM - 07:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set SIXPM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set SIXPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="07:00 PM - 08:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set SEVENPM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set SEVENPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="08:00 PM - 09:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set EIGHTPM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set EIGHTPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="09:00 PM - 10:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update handball set NINEPM="red" where tdate=%s',[bookdate])
               cur.execute('update handball1 set NINEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
                      
          else :    
              cur=mysql.connection.cursor()
              cur.execute('update handball set TENPM="red" where tdate=%s',[bookdate])
              cur.execute('update handball1 set TENPM="hide" where tdate=%s',[bookdate])
              mysql.connection.commit()
          return redirect(url_for("handball",umail=session["umail"])) 
                   
     elif 'choosedate' in request.form:
          cdate=request.form["demo"]  
          cur=mysql.connection.cursor()
          cur.execute("select * from  handball where tdate=%s",[cdate])
          res=cur.fetchone()
          cur.close()
          
          con=mysql.connection.cursor()
          con.execute("select * from  handball1 where tdate=%s",[cdate])
          res1=con.fetchone()
          con.close()
          
          return render_template("handball.html",datas=res,seldate=cdate,values=res1)

          
     return render_template("handball.html",datas=res,values=res1)   

@app.route("/kabaddi/<string:umail>",methods=["POST","GET"])
def kabaddi(umail):
       
     cur=mysql.connection.cursor()
     cur.execute("select * from kabaddi where tdate=(select current_date() from dual) ")
     res=cur.fetchone()
     
     con=mysql.connection.cursor()
     con.execute("select * from  kabaddi1 where tdate=(select current_date() from dual) ")
     res1=con.fetchone()
     con.close()
     
     if 'kabaddi' in request.form:
      if request.method=="POST":
          bookid=request.form["bid"]
          bookdate=request.form["bdate"]
          bookslot=request.form["btime"]
          sname=request.form["sport"]
          amount=request.form["amt"]
          
          cur=mysql.connection.cursor()
          cur.execute('insert into booking(bid,bdate,btime,sport,amount) values(%s,%s,%s,%s,%s)',[bookid,bookdate,bookslot,sname,amount])  
          mysql.connection.commit()
          
          app.config['MAIL_SERVER']='smtp.gmail.com'  
          app.config['MAIL_PORT']=465  
          app.config['MAIL_USERNAME'] ='sportsclub3115@gmail.com'
          app.config['MAIL_PASSWORD'] ='lkbq ewpe spbz qsya'
          app.config['MAIL_USE_TLS'] = False  
          app.config['MAIL_USE_SSL'] = True  
          mail=Mail(app) 

          msg=Message('WELCOME TO SPORTSCLUB TURF UNIVERSE',sender='sportsclub3115@gmail.com',recipients=[umail])    
          msg.body="YOUR SLOT HAS BEEN BOOKED SUCCESSFULLY"
            
          mail.send(msg)
          
          if bookslot=="05:00 AM - 06:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set FIVEAM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set FIVEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
           
          elif bookslot=="06:00 AM - 07:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set SIXAM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set SIXAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
          elif bookslot=="07:00 AM - 08:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set SEVENAM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set SEVENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
          elif bookslot=="08:00 AM - 09:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set EIGHTAM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set EIGHTAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
          elif bookslot=="09:00 AM - 10:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set NINEAM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set NINEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
          elif bookslot=="10:00 AM - 11:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set TENAM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set TENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
          elif bookslot=="11:00 AM - 12:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set ELEAM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set ELEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()             
           
          elif bookslot=="12:00 PM - 01:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set TWEPM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set TWEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()    

          elif bookslot=="01:00 PM - 02:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set ONEPM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set ONEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
          elif bookslot=="02:00 PM - 03:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set TWOPM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set TWOPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="03:00 PM - 04:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set THREEPM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set THREEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="04:00 PM - 05:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set FOURPM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set FOURPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="05:00 PM - 06:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set FIVEPM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set FIVEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="06:00 PM - 07:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set SIXPM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set SIXPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="07:00 PM - 08:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set SEVENPM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set SEVENPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="08:00 PM - 09:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set EIGHTPM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set EIGHTPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
          elif bookslot=="09:00 PM - 10:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update kabaddi set NINEPM="red" where tdate=%s',[bookdate])
               cur.execute('update kabaddi1 set NINEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
                      
          else :    
              cur=mysql.connection.cursor()
              cur.execute('update kabaddi set TENPM="red" where tdate=%s',[bookdate])
              cur.execute('update kabaddi1 set TENPM="hide" where tdate=%s',[bookdate])
              mysql.connection.commit()        
          return redirect(url_for("kabaddi",umail=session["umail"])) 
      
     elif 'choosedate' in request.form:
          cdate=request.form["demo"]  
          cur=mysql.connection.cursor()
          cur.execute("select * from  kabaddi where tdate=%s",[cdate])
          res=cur.fetchone()
          cur.close()
          
          con=mysql.connection.cursor()
          con.execute("select * from  kabaddi1 where tdate=%s",[cdate])
          res1=con.fetchone()
          con.close()
          
          return render_template("kabaddi.html",datas=res,seldate=cdate,values=res1,umail=umail)
          
     return render_template("kabaddi.html",datas=res,values=res1,umail=umail)     





@app.route("/cricket1",methods=["POST","GET"])
def cricket1():
         
      cur=mysql.connection.cursor()
      cur.execute("select * from  cricket where tdate=(select current_date() from dual) ")
      res=cur.fetchone()
      cur.close()
      con=mysql.connection.cursor()
      con.execute("select * from  cricket1 where tdate=(select current_date() from dual)")
      res1=con.fetchone()
      con.close()
      
     
      if 'cricket' in request.form:
         if request.method=="POST":
           
           bookdate=request.form["bdate"]
           bookslot=request.form["btime"]
         
          
          
           
       
               
          
           if bookslot=="05:00 AM - 06:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set FIVEAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set FIVEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
           
           elif bookslot=="06:00 AM - 07:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set SIXAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set SIXAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
           elif bookslot=="07:00 AM - 08:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set SEVENAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set SEVENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
           elif bookslot=="08:00 AM - 09:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set EIGHTAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set EIGHTAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
           elif bookslot=="09:00 AM - 10:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set NINEAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set NINEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
           elif bookslot=="10:00 AM - 11:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set TENAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set TENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
           elif bookslot=="11:00 AM - 12:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set ELEAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set ELEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()             
           
           elif bookslot=="12:00 PM - 01:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set TWEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set TWEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()    

           elif bookslot=="01:00 PM - 02:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set ONEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set ONEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
           elif bookslot=="02:00 PM - 03:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set TWOPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set TWOPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="03:00 PM - 04:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set THREEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set THREEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="04:00 PM - 05:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set FOURPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set FOURPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="05:00 PM - 06:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set FIVEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set FIVEEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="06:00 PM - 07:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set SIXPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set SIXPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="07:00 PM - 08:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set SEVENPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set SEVENPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="08:00 PM - 09:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set EIGHTPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set EIGHTPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="09:00 PM - 10:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update cricket set NINEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update cricket1 set NINEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
                      
           else :    
              cur=mysql.connection.cursor()
              cur.execute('update cricket set TENPM="yellow" where tdate=%s',[bookdate])
              cur.execute('update cricket1 set TENPM="hide" where tdate=%s',[bookdate])
              mysql.connection.commit()   
           return redirect(url_for("cricket1" ))  
         
      elif 'choosedate' in request.form:
          cdate=request.form["demo"]  
          cur=mysql.connection.cursor()
          cur.execute("select * from  cricket where tdate=%s",[cdate])
          res=cur.fetchone()
          
          con=mysql.connection.cursor()
          con.execute("select * from  cricket1 where tdate=%s",[cdate])
          res1=con.fetchone()
          con.close()
          return render_template("cricket1.html",datas=res,seldate=cdate,values=res1)      
      return render_template("cricket1.html",datas=res,values=res1)         


@app.route("/football1",methods=["POST","GET"])
def football1():
         
      cur=mysql.connection.cursor()
      cur.execute("select * from  football where tdate=(select current_date() from dual) ")
      res=cur.fetchone()
      cur.close()
      
      con=mysql.connection.cursor()
      con.execute("select * from  football1 where tdate=(select current_date() from dual)")
      res1=con.fetchone()
      con.close()
      
     
      if 'football' in request.form:
         if request.method=="POST":
           
           bookdate=request.form["bdate"]
           bookslot=request.form["btime"]
         
          
          
           
             
           
               
          
           if bookslot=="05:00 AM - 06:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update football set FIVEAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set FIVEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
           
           elif bookslot=="06:00 AM - 07:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update football set SIXAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set SIXAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
           elif bookslot=="07:00 AM - 08:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update football set SEVENAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set SEVENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
           elif bookslot=="08:00 AM - 09:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update football set EIGHTAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set EIGHTAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
           elif bookslot=="09:00 AM - 10:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update football set NINEAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set NINEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
           elif bookslot=="10:00 AM - 11:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update football set TENAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set TENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
           elif bookslot=="11:00 AM - 12:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update football set ELEAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set ELEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()             
           
           elif bookslot=="12:00 PM - 01:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update football set TWEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set TWEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()    

           elif bookslot=="01:00 PM - 02:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update football set ONEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set ONEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
           elif bookslot=="02:00 PM - 03:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update football set TWOPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set TWOPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="03:00 PM - 04:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update football set THREEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set THREEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="04:00 PM - 05:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update football set FOURPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set FOURPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="05:00 PM - 06:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update football set FIVEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set FIVEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="06:00 PM - 07:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update football set SIXPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set SIXPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="07:00 PM - 08:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update football set SEVENPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set SEVENPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="08:00 PM - 09:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update football set EIGHTPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set EIGHTPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="09:00 PM - 10:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update football set NINEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update football1 set NINEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
                      
           else :    
              cur=mysql.connection.cursor()
              cur.execute('update football set TENPM="yellow" where tdate=%s',[bookdate])
              cur.execute('update football1 set TENPM="hide" where tdate=%s',[bookdate])
              mysql.connection.commit()   
           return redirect(url_for("football1" ))  
         
      elif 'choosedate' in request.form:
          cdate=request.form["demo"]  
          cur=mysql.connection.cursor()
          cur.execute("select * from  football where tdate=%s",[cdate])
          res=cur.fetchone()
          
          con=mysql.connection.cursor()
          con.execute("select * from  football1 where tdate=%s",[cdate])
          res1=con.fetchone()
          con.close()
          
          return render_template("football1.html",datas=res,seldate=cdate,values=res1)      
      return render_template("football1.html",datas=res,values=res1)         


@app.route("/basketball1",methods=["POST","GET"])
def basketball1():
         
      cur=mysql.connection.cursor()
      cur.execute("select * from  basketball where tdate=(select current_date() from dual) ")
      res=cur.fetchone()
      cur.close()
      con=mysql.connection.cursor()
      con.execute("select * from  basketball1 where tdate=(select current_date() from dual)")
      res1=con.fetchone()
      con.close()
      
     
      if 'basketball' in request.form:
         if request.method=="POST":
           
           bookdate=request.form["bdate"]
           bookslot=request.form["btime"]
         
          
          
           
          
               
          
           if bookslot=="05:00 AM - 06:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set FIVEAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set FIVEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
           
           elif bookslot=="06:00 AM - 07:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set SIXAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set SIXAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
           elif bookslot=="07:00 AM - 08:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set SEVENAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set SEVENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
           elif bookslot=="08:00 AM - 09:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set EIGHTAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set EIGHTAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
           elif bookslot=="09:00 AM - 10:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set NINEAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set NINEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
           elif bookslot=="10:00 AM - 11:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set TENAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set TENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
           elif bookslot=="11:00 AM - 12:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set ELEAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set ELEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()             
           
           elif bookslot=="12:00 PM - 01:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set TWEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set TWEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()    

           elif bookslot=="01:00 PM - 02:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set ONEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set ONEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
           elif bookslot=="02:00 PM - 03:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set TWOPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set TWOPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="03:00 PM - 04:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set THREEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set THREEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="04:00 PM - 05:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set FOURPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set FOURPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="05:00 PM - 06:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set FIVEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set FIVEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="06:00 PM - 07:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set SIXPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set SIXPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="07:00 PM - 08:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set SEVENPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set SEVENPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="08:00 PM - 09:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set EIGHTPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set EIGHTPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="09:00 PM - 10:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update basketball set NINEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update basketball1 set NINEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
                      
           else :    
              cur=mysql.connection.cursor()
              cur.execute('update basketball set TENPM="yellow" where tdate=%s',[bookdate])
              cur.execute('update basketball1 set TENPM="hide" where tdate=%s',[bookdate])
              mysql.connection.commit()   
           return redirect(url_for("basketball1" ))  
         
      elif 'choosedate' in request.form:
          cdate=request.form["demo"]  
          cur=mysql.connection.cursor()
          cur.execute("select * from  basketball where tdate=%s",[cdate])
          res=cur.fetchone()
          
          con=mysql.connection.cursor()
          con.execute("select * from  basketball1 where tdate=%s",[cdate])
          res1=con.fetchone()
          con.close()
          
          return render_template("basketball1.html",datas=res,seldate=cdate,values=res1)      
      return render_template("basketball1.html",datas=res,values=res1)         
              
     
@app.route("/volleyball1",methods=["POST","GET"])
def volleyball1():
         
      cur=mysql.connection.cursor()
      cur.execute("select * from  volleyball where tdate=(select current_date() from dual) ")
      res=cur.fetchone()
      cur.close()
      con=mysql.connection.cursor()
      con.execute("select * from  volleyball1 where tdate=(select current_date() from dual)")
      res1=con.fetchone()
      con.close()
      
     
      if 'volleyball' in request.form:
         if request.method=="POST":
           
           bookdate=request.form["bdate"]
           bookslot=request.form["btime"]
         
          
          
           
          
               
          
           if bookslot=="05:00 AM - 06:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set FIVEAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set FIVEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
           
           elif bookslot=="06:00 AM - 07:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set SIXAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set SIXAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
           elif bookslot=="07:00 AM - 08:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set SEVENAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set SEVENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()
               
           elif bookslot=="08:00 AM - 09:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set EIGHTAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set EIGHTAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
           elif bookslot=="09:00 AM - 10:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set NINEAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set NINEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()  
               
           elif bookslot=="10:00 AM - 11:00 AM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set TENAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set TENAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
           elif bookslot=="11:00 AM - 12:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set ELEAM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set ELEAM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()             
           
           elif bookslot=="12:00 PM - 01:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set TWEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set TWEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()    

           elif bookslot=="01:00 PM - 02:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set ONEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set ONEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit()   
               
           elif bookslot=="02:00 PM - 03:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set TWOPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set TWOPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="03:00 PM - 04:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set THREEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set THREEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="04:00 PM - 05:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set FOURPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set FOURPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="05:00 PM - 06:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set FIVEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set FIVEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="06:00 PM - 07:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set SIXPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set SIXPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="07:00 PM - 08:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set SEVENPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set SEVENPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="08:00 PM - 09:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set EIGHTPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set EIGHTPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
               
           elif bookslot=="09:00 PM - 10:00 PM":
               cur=mysql.connection.cursor()
               cur.execute('update volleyball set NINEPM="yellow" where tdate=%s',[bookdate])
               cur.execute('update volleyball1 set NINEPM="hide" where tdate=%s',[bookdate])
               mysql.connection.commit() 
                      
           else :    
              cur=mysql.connection.cursor()
              cur.execute('update volleyball set TENPM="yellow" where tdate=%s',[bookdate])
              cur.execute('update volleyball1 set TENPM="hide" where tdate=%s',[bookdate])
              mysql.connection.commit()   
           return redirect(url_for("volleyball1" ))  
         
      elif 'choosedate' in request.form:
          cdate=request.form["demo"]  
          cur=mysql.connection.cursor()
          cur.execute("select * from  volleyball where tdate=%s",[cdate])
          res=cur.fetchone()
          cur.close()
          
          con=mysql.connection.cursor()
          con.execute("select * from  volleyball1 where tdate=%s",[cdate])
          res1=con.fetchone()
          con.close()
          
          return render_template("volleyball1.html",datas=res,seldate=cdate,values=res1)      
      return render_template("volleyball1.html",datas=res,values=res1)         
              
@app.route("/handball1",methods=["POST","GET"])
def handball1():

 cur=mysql.connection.cursor()
 cur.execute("select * from  handball where tdate=(select current_date() from dual) ")
 res=cur.fetchone()
 cur.close()
 con=mysql.connection.cursor()
 con.execute("select * from  handball1 where tdate=(select current_date() from dual)")
 res1=con.fetchone()
 con.close()


 if 'handball' in request.form:
   if request.method=="POST":

      bookdate=request.form["bdate"]
      bookslot=request.form["btime"]







      if bookslot=="05:00 AM - 06:00 AM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set FIVEAM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set FIVEAM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()

      elif bookslot=="06:00 AM - 07:00 AM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set SIXAM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set SIXAM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()

      elif bookslot=="07:00 AM - 08:00 AM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set SEVENAM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set SEVENAM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()

      elif bookslot=="08:00 AM - 09:00 AM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set EIGHTAM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set EIGHTAM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()  

      elif bookslot=="09:00 AM - 10:00 AM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set NINEAM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set NINEAM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()  

      elif bookslot=="10:00 AM - 11:00 AM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set TENAM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set TENAM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()   

      elif bookslot=="11:00 AM - 12:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set ELEAM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set ELEAM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()             

      elif bookslot=="12:00 PM - 01:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set TWEPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set TWEPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()    

      elif bookslot=="01:00 PM - 02:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set ONEPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set ONEPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()   

      elif bookslot=="02:00 PM - 03:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set TWOPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set TWOPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 

      elif bookslot=="03:00 PM - 04:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set THREEPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set THREEPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 

      elif bookslot=="04:00 PM - 05:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set FOURPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set FOURPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 

      elif bookslot=="05:00 PM - 06:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set FIVEPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set FIVEEPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 

      elif bookslot=="06:00 PM - 07:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set SIXPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set SIXPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 

      elif bookslot=="07:00 PM - 08:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set SEVENPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set SEVENPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 

      elif bookslot=="08:00 PM - 09:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set EIGHTPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set EIGHTPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 

      elif bookslot=="09:00 PM - 10:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update handball set NINEPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set NINEPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 
          
      else :    
          cur=mysql.connection.cursor()
          cur.execute('update handball set TENPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update handball1 set TENPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()   
      return redirect(url_for("handball1" ))  

 elif 'choosedate' in request.form:
     cdate=request.form["demo"]  
     cur=mysql.connection.cursor()
     cur.execute("select * from  handball where tdate=%s",[cdate])
     res=cur.fetchone()
     cur.close()
     
     con=mysql.connection.cursor()
     con.execute("select * from  handball1 where tdate=%s",[cdate])
     res1=con.fetchone()
     con.close()
     
     return render_template("handball1.html",datas=res,seldate=cdate,values=res1)      
 return render_template("handball1.html",datas=res,values=res1)          


@app.route("/kabaddi1",methods=["POST","GET"])
def kabaddi1():

 cur=mysql.connection.cursor()
 cur.execute("select * from  kabaddi where tdate=(select current_date() from dual) ")
 res=cur.fetchone()
 cur.close()
 con=mysql.connection.cursor()
 con.execute("select * from  kabaddi1 where tdate=(select current_date() from dual)")
 res1=con.fetchone()
 con.close()


 if 'kabaddi' in request.form:
   if request.method=="POST":

      bookdate=request.form["bdate"]
      bookslot=request.form["btime"]







      if bookslot=="05:00 AM - 06:00 AM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set FIVEAM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set FIVEAM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()

      elif bookslot=="06:00 AM - 07:00 AM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set SIXAM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set SIXAM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()

      elif bookslot=="07:00 AM - 08:00 AM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set SEVENAM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set SEVENAM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()

      elif bookslot=="08:00 AM - 09:00 AM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set EIGHTAM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set EIGHTAM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()  

      elif bookslot=="09:00 AM - 10:00 AM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set NINEAM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set NINEAM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()  

      elif bookslot=="10:00 AM - 11:00 AM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set TENAM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set TENAM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()   

      elif bookslot=="11:00 AM - 12:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set ELEAM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set ELEAM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()             

      elif bookslot=="12:00 PM - 01:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set TWEPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set TWEPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()    

      elif bookslot=="01:00 PM - 02:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set ONEPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set ONEPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()   

      elif bookslot=="02:00 PM - 03:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set TWOPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set TWOPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 

      elif bookslot=="03:00 PM - 04:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set THREEPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set THREEPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 

      elif bookslot=="04:00 PM - 05:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set FOURPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set FOURPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 

      elif bookslot=="05:00 PM - 06:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set FIVEPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set FIVEPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 

      elif bookslot=="06:00 PM - 07:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set SIXPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set SIXPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 

      elif bookslot=="07:00 PM - 08:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set SEVENPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set SEVENPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 

      elif bookslot=="08:00 PM - 09:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set EIGHTPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set EIGHTPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 

      elif bookslot=="09:00 PM - 10:00 PM":
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set NINEPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set NINEPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit() 
          
      else :    
          cur=mysql.connection.cursor()
          cur.execute('update kabaddi set TENPM="yellow" where tdate=%s',[bookdate])
          cur.execute('update kabaddi1 set TENPM="hide" where tdate=%s',[bookdate])
          mysql.connection.commit()   
      return redirect(url_for("kabaddi1" ))  

 elif 'choosedate' in request.form:
     cdate=request.form["demo"]  
     cur=mysql.connection.cursor()
     cur.execute("select * from  kabaddi where tdate=%s",[cdate])
     res=cur.fetchone()
     cur.close()
     
     con=mysql.connection.cursor()
     con.execute("select * from  kabaddi1 where tdate=%s",[cdate])
     res1=con.fetchone()
     con.close()
     return render_template("kabaddi1.html",datas=res,seldate=cdate,values=res1)      
 return render_template("kabaddi1.html",datas=res,values=res1) 


@app.route("/cancel")
def cancel():
  
    con=mysql.connection.cursor()
    con.execute('update football set FIVEAM="green" where tdate="2024-03-16"')
    
    con.execute('delete from booking where bdate="2024-03-16"')
    con.close()
    return redirect(url_for("userdetails",id=session["uid"]))
    
            
            
                        
            

   
if(__name__=='__main__'):
     app.secret_key="flask"
     app.run(debug=True)