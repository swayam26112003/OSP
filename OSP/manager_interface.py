from flask import render_template, url_for, redirect, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from wtforms import *
from flask_bcrypt import Bcrypt
from OSP.Classes import Manager,User,Orderdetails,Products,Negotiations
from OSP.Forms import RegisterManagerForm,LoginManagerForm
from . import app,db

bcrypt = Bcrypt(app)

login_manager2 = LoginManager()
login_manager2.init_app(app)
login_manager2.login_view = 'loginmanager'

@login_manager2.user_loader
def load_manager(user_id):
    return Manager.query.get(int(user_id))

global manager_in





manager_in = Manager()




@app.route('/loginmanager', methods=['GET', 'POST'])
def loginmanager():
    form = LoginManagerForm()
    if form.validate_on_submit():
        global manager_in
        manager_in = Manager.query.filter_by(Email=form.email.data).first()
        if manager_in:
            if bcrypt.check_password_hash(manager_in.Password, form.password.data):
                login_user(manager_in)

                return redirect(url_for('home_manager'))
            else:
                return render_template('loginmanager.html', form=form, error="Incorrect Password")
        else:
            return render_template('loginmanager.html', form=form, error="No account with this email id exist!!")

    return render_template('loginmanager.html', form=form)


@app.route('/home_manager', methods=['GET', 'POST'])
def home_manager():
    global manager_in
    Users = User.query.filter_by(IsBuyer=True).all()
    Sellers = User.query.filter_by(IsSeller=True).all()
    Items = Products.query.all()
    sellersi = []
    for item in Items:
        sellersi.append(User.query.filter_by(User_id=item.Sellerid).first())
    Orders = Orderdetails.query.all()
    Selled_Products = []
    Seller_Products = []
    Buyer_Products = []
    for order in Orders:
        Selled_Products.append(Products.query.filter_by(Pid=order.pid).first())
        Buyer_Products.append(User.query.filter_by(User_id=order.cid).first())
        Seller_Products.append(User.query.filter_by(
            User_id=Selled_Products[-1].Sellerid).first())

    return render_template('home_manager.html', manager=manager_in, Users=Users, Sellersa=Sellers, items=Items, Sellers=sellersi, Selled_Products=Selled_Products, Seller_Products=Seller_Products, Buyer_Products=Buyer_Products, Orderlist=Orders)


@app.route('/home_manager/manager_details', methods=['GET', 'POST'])
def manager_details():
    global manager_in
    return render_template('manager_account.html', manager=manager_in)


@app.route('/home_manager/manage_customer', methods=['GET', 'POST'])
def manage_customer():
    global manager_in
    Users = User.query.all()

    return render_template('manage_customer.html', manager=manager_in, Users=Users)

@app.route('/home_manager/manage_product', methods=['GET', 'POST'])
def manage_product():
    global manager_in
    Items = Products.query.all()
    sellersi = []
    for item in Items:
        sellersi.append(User.query.filter_by(User_id=item.Sellerid).first())
    return render_template('manage_product.html', manager=manager_in, items=Items, Sellers=sellersi)

@app.route('/logoutmanager', methods=['GET', 'POST'])
def logoutmanager():
    logout_user()
    return redirect(url_for('loginmanager'))


@ app.route('/registermanager', methods=['GET', 'POST'])
def registermanager():
    form = RegisterManagerForm()

    if form.validate_on_submit():
        existing_user_email = Manager.query.filter_by(
            Email=form.email.data).first()
        if existing_user_email:
            return render_template('registermanager.html', error="Account with this email ID already exists", form=form)
        if form.password.data != form.re_password.data:
            return render_template('registermanager.html', error="Passwords to not match", form=form)
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_manager = Manager(Name=form.managername.data, Email=form.email.data, Password=hashed_password, Phone_num=form.phone_no.data,
                              Street=form.street.data, City=form.city.data, State=form.state.data, PIN=form.pin.data, Gender=form.Gender.data, Dob=form.dob.data)
        db.session.add(new_manager)
        db.session.commit()
        return redirect(url_for('loginmanager'))

    return render_template('registermanager.html', form=form)


@app.route('/home_manager/manage_customer/delete/<id>', methods=['GET', 'POST'])
def deleteuser(id):
    user = User.query.filter_by(User_id=id).first()
    user.IsBuyer = False
    db.session.commit()

    return redirect(url_for('manage_customer'))


@app.route('/home_manager/manage_customer/activate/<id>', methods=['GET', 'POST'])
def activateuser(id):
    user = User.query.filter_by(User_id=id).first()
    user.IsBuyer = True
    db.session.commit()
    return redirect(url_for('manage_customer'))


@app.route('/home_manager/manage_seller/<id>', methods=['GET', 'POST'])
def deleteseller(id):
    user = User.query.filter_by(User_id=id).first()
    user.IsSeller = False
    db.session.commit()
    products = Products.query.filter_by(Sellerid=user.User_id).all()
    for product in products:
        Orders = Orderdetails.query.filter_by(pid=product.Pid).all()
        for order in Orders:
            if order.Status == 0:
                product.quantity += order.quantity
                db.session.commit()
                db.session.delete(order)
                db.session.commit()
    return redirect(url_for('manage_customer'))

@app.route('/home_manager/manage_seller/activate/<id>', methods=['GET', 'POST'])
def activateseller(id):
    user = User.query.filter_by(User_id=id).first()
    user.IsSeller = True
    db.session.commit()
    return redirect(url_for('manage_customer'))


@app.route('/home_manager/manage_product/<id>', methods=['GET', 'POST'])
def deleteproduct(id):
    product = Products.query.filter_by(Pid=id).first()
    product.status = False
    db.session.commit()
    Orders = Orderdetails.query.filter_by(pid=product.Pid).all()
    for order in Orders:
        if order.Status == 0:
            product.quantity += order.quantity
            db.session.commit()
            db.session.delete(order)
            db.session.commit()
    return redirect(url_for('manage_product'))


@app.route('/home_manager/manage_product/activate/<id>', methods=['GET', 'POST'])
def activateproduct(id):
    product = Products.query.filter_by(Pid=id).first()
    product.status = True
    db.session.commit()
    return redirect(url_for('manage_product'))

@ app.route('/home_manager/negotiations_all_product', methods=['GET', 'POST'])
def all_product_manager():
    global manager_in
    manager_in = Manager.query.filter_by(Email=manager_in.Email).first()

    products=Products.query.all()
    return render_template('all_products_manager.html',manager=manager_in,products=products)

@app.route('/home_manager/negotiations/<int:id>',methods=['GET','POST'])
def seenegotiations_manager(id):
    global manager_in
    convo=Negotiations.query.filter_by(Pid=id).all()
    manager_in = Manager.query.filter_by(Email=manager_in.Email).first()

    convcustomer=[]
    for c in convo:
        if c.buyer_id not in convcustomer:
            convcustomer.append(c.buyer_id)
    customers=[]
    for i in convcustomer:
        customers.append(User.query.filter_by(User_id=i).first())
    seller=User.query.filter_by(User_id=Products.query.filter_by(Pid=id).first().Sellerid).first()
    return render_template('seenegotiations_manager.html',customers=customers,product=Products.query.filter_by(Pid=id).first(),seller=seller,manager=manager_in)

@app.route('/home_manager/negotiation_manager/<int:id>/<int:pid>',methods=['GET','POST'])
def negotiation_manager(id,pid):
    global manager_in
    manager_in = Manager.query.filter_by(Email=manager_in.Email).first()

    product=Products.query.filter_by(Pid=pid).first()
    seller=User.query.filter_by(User_id=product.Sellerid).first()

    customer=User.query.filter_by(User_id=id).first()
    convo=Negotiations.query.all()
    convo1=[]
    for c in convo:
        if c.Pid==pid:
            if c.seller_id==product.Sellerid:
                if c.buyer_id==customer.User_id and c not in convo1:
                    convo1.append(c)
    
    for c in convo1:
       if c.price!=-1:
        return render_template('negotiate_manager.html',product=product,manager=manager_in,customer=customer,convo=convo1,flag=1,seller=seller)
    
    return render_template('negotiate_manager.html',product=product,manager=manager_in,customer=customer,convo=convo1,flag=0,seller=seller)

@app.route('/home_manager/send_message_manager/<int:id>/<int:cid>',methods=['GET','POST'])
def send_message_manager(id,cid):
    global manager_in
    manager_in = Manager.query.filter_by(Email=manager_in.Email).first()
    mess=request.form['mess']
    product=Products.query.filter_by(Pid=id).first()
    seller=User.query.filter_by(User_id=product.Sellerid).first()
    customer=User.query.filter_by(User_id=cid).first()
    newc=Negotiations(Pid=id,seller_id=product.Sellerid,buyer_id=cid,Message=mess,sender_id=manager_in.Manager_id,price=-1,ismanager=1)
    db.session.add(newc)
    db.session.commit()
    convo=Negotiations.query.all()
    convo1=[]
    for c in convo:
        if c.Pid==id:
            if c.seller_id==product.Sellerid:
                if c.buyer_id==customer.User_id and c not in convo1:
                    convo1.append(c)
    
    return render_template('negotiate_manager.html',product=product,manager=manager_in,customer=customer,convo=convo1,flag=0,seller=seller)