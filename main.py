#print("yes")
#from crypt import methods
from cProfile import label
from unicodedata import name
from flask import Flask, flash ,render_template, request ,redirect, url_for ,session

import psycopg2
import os
import secrets
app = Flask(__name__)


conn=psycopg2.connect("dbname='d1m8odf2nbe0jt' user='idlxsyofckzrsu' port='5432 ' host='ec2-52-30-133-191.eu-west-1.compute.amazonaws.com' password='377cc0aab4454edd009635c4786b072f4e75ef0d07fc222ff7020a6c6d950a4a'")
app.config['SECRET_KEY'] = 'clintoo1111david222'
#app.config['SECRET_KEY'] = 'clintoo111david0000'
#conn=psycopg2.connect("dbname='duka' user='postgres' host='localhost' password='5132'")


@app.route('/t')
def hello_world():
    return 'Hello, clintoo!'



 


@app.route('/')
def home():
    return  render_template("home.html") 

@app.route('/modal fade')
def modal():
    return render_template("inventory.html")

@app.route('/inventory')
def prods():
   prod =[(1,"omo", 45 ,56,43,"quality" ),(2,"rice" ,50,60, 4,"98BA" ),
   (3,"bread" ,78, 98, 6, "quality" ),(4,"tv" ,20000,59000,1, "brand new"),(5,"phone",1000,15000,"brand new")
   ]
   cur=conn.cursor()
   cur.execute("SELECT *from products")
   rows = cur.fetchall()
   print(rows)
   return render_template("inventory.html",y=rows)

@app.route('/dashboard')
def dashboard():
    cur=conn.cursor()
    

    cur.execute(" SELECT extract(month from s.created_at) as months, sum(s.quantity) as quantity ,  sum ((p.sp-p.bp) *s.quantity)  from sales as s join products as p on p.id=s.product_id group by months order by months asc")
    dash = cur.fetchall()

    label=[]
    data=[]
    for i in dash:
      label.append(i[0])
      data.append(i[2])
    print(dash)

    return render_template("dashboard.html" ,label=label ,data=data)
 



@app.route('/sales' '/<int:pid>')
def  sales(pid):
     cur=conn.cursor()
     cur.execute("SELECT p.name, sum(s.quantity) as quantity , sum ((p.sp-p.bp) *s.quantity)  from sales as s join products as p on p.id=s.product_id group by p.name where id=%s",[pid])
     rows = cur.fetchall()
     print(rows)
     return render_template("sales.html" ,x=rows)

# @app.route('/sales')
# def  sale(pid):
#      cur=conn.cursor()
#      cur.execute("SELECT p.name, sum(s.quantity) as quantity , sum ((p.sp-p.bp) *s.quantity)  from sales as s join products as p on p.id=s.product_id group by p.name where id=%s",[pid])
#      rows = cur.fetchall()
#      print(rows)
#      return render_template("sales.html" ,x=rows)


@app.route('/add_items' ,methods=['GET','POST'])
def form():
  cur=conn.cursor()

  if request.method=='POST':    
     name=request.form["name"]
     bp=request.form["bp"],
     sp=request.form["sp"]
   
     query="INSERT INTO products( name, bp, sp )VALUES ( %s, %s, %s )"
     row= (name,bp,sp)
     cur.execute(query ,row)
     conn.commit()
     flash('welcome')

     return redirect(url_for ("prods")) 

  else:

     flash("try again")


@app.route('/make_sales', methods=["POST"])  
def makes_sales():
   cur=conn.cursor()
   if request.method=="POST":
      quantity=request.form['quantity']
      product_id=request.form['product_id']
      query="insert into sales( quantity, product_id ) values(%s ,%s)"
      row=( quantity, product_id)
      cur.execute(query,row)
      conn.commit()
      flash("welcome")
      return redirect(url_for("sales"))

   else: 
     flash ("try again") 


@app.route("/edit" ,methods=["get","post"])
def edit():
    cur=conn.cursor()
    if request.method=="POST":

      name=request.form["name"]
      bp=request.form["bp"],
      sp=request.form["sp"],
      id=request.form["id"]

      query=" UPDATE products SET name=name, bp=bp, sp=sp, WHERE id=%s ;"
      row=( id, name ,bp,sp ) 
      cur.execute(query ,row)
      conn.commit()
      flash("welcome")

      return redirect(url_for(prods))

    else:
        flash("sorry")



app.run(debug=True)
