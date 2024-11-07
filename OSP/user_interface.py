from flask import render_template, url_for, redirect, request
from flask_login import login_user,LoginManager, logout_user, current_user
from wtforms import *
from flask_bcrypt import Bcrypt
from .Classes import Cart,User,OPtobepassed,Orderdetails,Products,Negotiations
from .Forms import RegisterUserForm,LoginUserForm,ProductForm,ChangeProductForm
from . import app,db

bcrypt = Bcrypt(app)

login_manager1 = LoginManager()
login_manager1.init_app(app)
login_manager1.login_view = 'login'

@login_manager1.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


global user
user = User()

@app.route('/login_user', methods=['GET', 'POST'])
def login():
    form = LoginUserForm()
    if form.validate_on_submit():
        global user
        user = User.query.filter_by(Email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.Password, form.password.data):
                login_user(user)
                return redirect(url_for('home_user'))
            else:
                return render_template('login.html', form=form, error="Incorrect Password")
        else:
            return render_template('login.html', form=form, error="No account with this email id exist!!")

    return render_template('login.html', form=form)

@app.route('/home_user', methods=['GET', 'POST'])

def home_user():
    global user
    user=User.query.filter_by(Email=user.Email).first()
    return render_template('home_user.html', user=user)

@ app.route('/register_user', methods=['GET', 'POST'])
def register():
    form = RegisterUserForm()

    if form.validate_on_submit():
        existing_user_email = User.query.filter_by(
            Email=form.email.data).first()
        if existing_user_email:
            return render_template('register.html', error="Account with this email ID already exists", form=form)
        if form.password.data != form.re_password.data:
            return render_template('register.html', error="Passwords to not match", form=form)
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(Name=form.username.data, Email=form.email.data, Password=hashed_password, Phone_num=form.phone_no.data,
                        Street=form.street.data, City=form.city.data, State=form.state.data, PIN=form.pin.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)




@app.route('/logout_user', methods=['GET', 'POST'])

def logout():
    logout_user()
    return redirect(url_for('login'))



@ app.route('/home_user/sell_product', methods=['GET', 'POST'])

def sellproduct():
    
    global user
    if user.IsSeller==0:
        return "You cannot Sell items right now,Please contact us for more information"
    form = ProductForm()
    if form.validate_on_submit():
        
        new_product= Products(Name=form.Productname.data,Sellerid=user.User_id,Price=form.price.data,Image_url=form.image.data,mfgdate=form.Mfgdate.data,mfgcompany=form.Mfgcompany.data,sellercity=user.City,quantity=form.Quantity.data,weight=form.weight.data,Description=form.Description.data,Category=form.Category.data)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('sellproduct', user=user,success="Product added successfully",form=form))

   
    return render_template('sellproduct.html', user=user,form=form)


@ app.route('/home_user/sell_product/add_to_list', methods=['GET', 'POST'])

def addtosell():
    global user
    user=User.query.filter_by(Email=user.Email).first()
    if user.IsSeller==0:
        return "You cannot Sell items right now,Please contact us for more information"
    
    return render_template('addtosell.html', user=user)
@app.route('/home_user/viewproduct/buycart',methods=['GET','POST'])
def buycart():
    global user
    user=User.query.filter_by(Email=user.Email).first()
    cart=Cart.query.filter_by(userid=user.User_id).all()
    l=len(cart)
    global total_cost
    total_cost=0
    for order in cart:
        total_cost+=Products.query.filter_by(Pid=order.pid).first().Price*order.quantity
    if len(cart)==0:
        return render_template('cart.html',user=user,error="Cart is empty! Add something to cart to buy",total_cost=total_cost)
    alpha=0
    if(total_cost<=User.query.filter_by(Email=user.Email).first().balance):
            for order in cart:
                product=Products.query.filter_by(Pid=order.pid).first()
                if User.query.filter_by(Email=user.Email).first().balance>=order.quantity*product.Price and order.quantity<=product.quantity:
                    alpha=alpha+1
                    user1 = User.query.filter_by(Email=user.Email).first()
                    user1.balance=user1.balance-(order.quantity*(product.Price))
                    db.session.commit()
                    seller1=User.query.filter_by(User_id=product.Sellerid).first()
                    seller1.balance=seller1.balance+(order.quantity*(product.Price))
                    db.session.commit()


                    product.quantity=product.quantity-order.quantity
                    db.session.commit()
                    new_order=Orderdetails(pid=product.Pid,cid=user.User_id,quantity=order.quantity,Status=0)
                    db.session.add(new_order)
                    db.session.commit()
                    db.session.delete(order)
                    db.session.commit()
                total_cost=0
    else:
        cart1=Cart.query.filter_by(userid=user.User_id).all()
        products=[]
        for order in cart1:
            products.append(Products.query.filter_by(Pid=order.pid).first())
        return render_template('cart.html', user=user,cart1=cart1,products=products,total_cost=total_cost,error="Insufficient Balance")
    
    if(alpha==l):
        return render_template('cart.html',user=user,error="Successfully bought all products in the cart",total_cost=total_cost)
    else:
        total_cost=0
        cart1=Cart.query.filter_by(userid=user.User_id).all()
        for order in cart1:
            total_cost+=Products.query.filter_by(Pid=order.pid).first().Price*order.quantity
        
        products=[]
        for order in cart1:
            products.append(Products.query.filter_by(Pid=order.pid).first())
        return render_template('cart.html', user=user,cart1=cart1,products=products,total_cost=total_cost,error="The Items remaining in cart are not available in required quantity,please delete them from cart and add them again from the product page.Remaining Items have been bought")

# @app.route('/home_user/viewproduct/buycart',methods=['GET','POST'])

# def buycart():
#     global user
#     user=User.query.filter_by(Email=user.Email).first()
#     cart=Cart.query.filter_by(userid=user.User_id).all()
#     global total_cost
#     total_cost=0
#     for order in cart:
#         total_cost+=Products.query.filter_by(Pid=order.pid).first().Price*order.quantity
    
#     if(total_cost<=User.query.filter_by(Email=user.Email).first().balance):
#             for order in cart:
#                 product=Products.query.filter_by(Pid=order.pid).first()
#                 if User.query.filter_by(Email=user.Email).first().balance>=order.quantity*product.Price:
#                     user1 = User.query.filter_by(Email=user.Email).first()
#                     user1.balance=user1.balance-(order.quantity*(product.Price))
#                     db.session.commit()
#                     seller1=User.query.filter_by(User_id=product.Sellerid).first()
#                     seller1.balance=seller1.balance+(order.quantity*(product.Price))
#                     db.session.commit()


#                     product.quantity=product.quantity-order.quantity
#                     db.session.commit()
#                     new_order=Orderdetails(pid=product.Pid,cid=user.User_id,quantity=order.quantity,Status=0)
#                     db.session.add(new_order)
#                     db.session.commit()
#                 db.session.delete(order)
#                 db.session.commit()
#                 total_cost=0
#     else:
#         cart1=Cart.query.filter_by(userid=user.User_id).all()
#         products=[]
#         for order in cart1:
#             products.append(Products.query.filter_by(Pid=order.pid).first())
#         return render_template('cart.html', user=user,cart1=cart1,products=products,total_cost=total_cost,error="Insufficient Balance")
    
#     return render_template('cart.html',user=user,error="Successfully bought all products in the cart",total_cost=total_cost)


@app.route('/SalesStatus')

def salesstatus():
    global user
    user=User.query.filter_by(Email=user.Email).first()
    l1=[]#l1 has all buying instances of the products uploaded by this user_id,render these as it is along with quantities bought in each
    l2=[]#l2 has products in the unsold product data base uploaded by this user
    l3=[]#l2 has products in the unsold product data base uploaded by this user
    all_products=Products.query.all()
    all_orders=Orderdetails.query.all()
    for x in all_orders:
        product=Products.query.filter_by(Pid=x.pid).first()
        if product.Sellerid==user.User_id:
            l1.append(x)
            l3.append(product)

    for p in all_products:
        if p.Sellerid==user.User_id and p.quantity>0:
            l2.append(p)
    return render_template('Sales_Status.html',user=user,l1=l1,l2=l2,l3=l3)

@app.route('/search', methods=['POST'])

def search():
    global user
    user=User.query.filter_by(Email=user.Email).first()
    if user.IsBuyer==0:
        return "You cannot Search for or buy items right now,Please contact us for more information"
    query=request.form['search']#it will come into this route with search and query set from url_for so no need to worry about query being none
    if(len(query)!=0):
        all_products = Products.query.all()
        l1=[]    
        for p in all_products:
            if p.Sellerid!=user.User_id and (query.lower() in (str(p.Name)).lower() or query.lower() in (str(p.Category)).lower()):
                if not p in l1:
                    if p.quantity>0 and p.status==1:
                        seller=User.query.filter_by(User_id=p.Sellerid).first()
                        if seller.City!=user.City and p.weight>100:
                            continue
                        else:
                            l1.append(p)
        if len(l1)==0:
            return "Product Not Found"
        return render_template('search.html',query=query,l1=l1,user=user)
    else:
        return "Search Something!!"
    
@app.route('/home_user/cart', methods=['GET', 'POST'])

def cart():
    global user
    user=User.query.filter_by(Email=user.Email).first()
    cart=Cart.query.filter_by(userid=user.User_id).all()
    total_cost=0
    for order in cart:
        total_cost+=Products.query.filter_by(Pid=order.pid).first().Price*order.quantity 
    if user.IsBuyer==0:
        return "You cannot Search for or buy items right now,Please contact us for more information"
    cart1=Cart.query.filter_by(userid=user.User_id).all()
    products=[]
    for order in cart1:
        products.append(Products.query.filter_by(Pid=order.pid).first())
    return render_template('cart.html', user=user,cart1=cart1,products=products,total_cost=total_cost)

@app.route('/home_user/cart/<id>', methods=['GET', 'POST'])
def deletecart(id):
    cart1=Cart.query.filter_by(cartid=id).first()
    db.session.delete(cart1)
    db.session.commit() 
    global user
    user=User.query.filter_by(Email=user.Email).first()
    cart=Cart.query.filter_by(userid=user.User_id).all()
    total_cost=0
    for order in cart:
        total_cost+=Products.query.filter_by(Pid=order.pid).first().Price*order.quantity 
    if user.IsBuyer==0:
        return "You cannot Search for or buy items right now,Please contact us for more information"
    cart1=Cart.query.filter_by(userid=user.User_id).all()
    products=[]
    for order in cart1:
        products.append(Products.query.filter_by(Pid=order.pid).first())
    return render_template('cart.html', user=user,cart1=cart1,products=products,total_cost=total_cost)


@app.route('/orderdetails', methods=['GET', 'POST'])

def orderstatus():
    global user
    user=User.query.filter_by(Email=user.Email).first()
    allmatching=Orderdetails.query.filter_by(cid=user.User_id).all()
    #print(allmatching)
    newlist=[]
    for x in allmatching:
        product=Products.query.filter_by(Pid=x.pid).first()
        seller=User.query.filter_by(User_id=product.Sellerid).first()
        if x.Status==1 or (x.Status==0 and product.status==1):
            print("hello world"+seller.Email)
            if x.Price==-1:
                new=OPtobepassed(x.oid,product.Name,product.Sellerid,seller.Email,product.Price,x.quantity,x.Status)
            else:
                new=OPtobepassed(x.oid,product.Name,product.Sellerid,seller.Email,x.Price,x.quantity,x.Status)
            print(new.email)
            newlist.append(new)
    return render_template('orderdetails.html',list1=newlist,user=user)

    return render_template('orderdetails.html')
@app.route('/userdetails', methods=['GET', 'POST'])
def userdetails():
    global user
    user=User.query.filter_by(Email=user.Email).first()
    return render_template('user_details.html',user=user)

@app.route('/home_user/settings', methods=['GET', 'POST'])

def settings():
    global user
    user=User.query.filter_by(Email=user.Email).first()
    return render_template('settings.html',user=user)


@app.route('/home_user/viewproduct/<int:PID>',methods=['GET','POST'])

def viewproduct(PID):
    global user
    user=User.query.filter_by(Email=user.Email).first()
    product=Products.query.filter_by(Pid=PID).first()
    return render_template('viewproduct.html',product=product,user=user)
@app.route('/home_user/viewproduct/buyproduct/<int:pid>/<int:quantity>',methods=['GET','POST'])
def buyproduct(pid,quantity):
    global user
    user=User.query.filter_by(Email=user.Email).first()
    product=Products.query.filter_by(Pid=pid).first()
    if user.balance>=quantity*product.Price:
        user1 = User.query.filter_by(Email=user.Email).first()
        user1.balance=user1.balance-(quantity*(product.Price))
        db.session.commit()
        print(user.balance)
        product.quantity=product.quantity-quantity
        db.session.commit()
        new_order=Orderdetails(pid=product.Pid,cid=user.User_id,quantity=quantity,Status=0)
        db.session.add(new_order)
        db.session.commit()

        return render_template('buyproduct.html',product=product,name=user.Name,quantity=quantity,user=user)
    else: 
        return "Insufficient Balance"
    
global total_cost
total_cost=0
@app.route('/home_user/viewproduct/addtocart/<int:pid>/<int:quantity>',methods=['GET','POST'])
def addtocart(pid,quantity):
    global user
    global total_cost
    x=Cart.query.filter_by(userid=user.User_id,pid=pid).first()
    if x is not None:
        x.quantity=x.quantity+quantity
        db.session.commit()

    else:
        cart=Cart(pid=pid,userid=user.User_id,quantity=quantity)
        db.session.add(cart)
    
    user=User.query.filter_by(Email=user.Email).first()
   
    cart=Cart.query.filter_by(userid=user.User_id).all()
    total_cost=0
    for order in cart:
        total_cost+=Products.query.filter_by(Pid=order.pid).first().Price*order.quantity
    product=Products.query.filter_by(Pid=pid).first()
    db.session.commit()
    cart1=Cart.query.filter_by(userid=user.User_id).all()
    products=[]
    for order in cart1:
        products.append(Products.query.filter_by(Pid=order.pid).first())
    return render_template('cart.html', user=user,cart1=cart1,products=products,total_cost=total_cost)
   

@app.route('/form/<int:pid>', methods=['GET', 'POST'])
def form(pid):
    if request.method == 'POST':
        action = request.form.get('action')
        quantity=request.form.get('quantity')
        if action == 'buynow':
            return redirect(url_for('buyproduct',pid=pid,quantity=quantity))
        elif action == 'addtocart':
            return redirect(url_for('addtocart',pid=pid,quantity=quantity))
        elif action == 'negotiate':
            return redirect(url_for('negotiate',id=pid))

@app.route('/home_user/settings/change_password', methods=['GET', 'POST'])

def change_password():
    global user
    user=User.query.filter_by(Email=user.Email).first()
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        user = User.query.filter_by(User_id=current_user.User_id).first()
        if bcrypt.check_password_hash(user.Password, old_password):
            if len(new_password) >= 8 and new_password == confirm_password:
                hashed_password = bcrypt.generate_password_hash(new_password)
                user.Password = hashed_password
                db.session.commit()
                return redirect(url_for('home'))
            else:
                error = 'New password should be more than or equal to 8 characters long and should match Confirm Password'
                return render_template('change_password.html', error=error,user=user)
        else:
            error = 'Incorrect Old Password'
            return render_template('change_password.html', error=error,user=user)
    else:
        return render_template('change_password.html',user=user)

@app.route('/viewproductsbyCategory/<Category>',methods=['GET','POST'])

def viewcat(Category):
    global user
    user=User.query.filter_by(Email=user.Email).first()
    if user.IsBuyer==0:
        return "You cannot Search for or buy items right now as decided by an appropriate manager"
    all_products = Products.query.all()
    l1=[]
    for p in all_products:
        if  p.Sellerid!=user.User_id and  Category.lower() == (str(p.Category)).lower():
            seller=User.query.filter_by(User_id=p.Sellerid).first()
            if seller.City!=user.City and p.weight>100:
                continue
            else:
                l1.append(p)
    if len(l1)==0:
        return render_template('search.html',query=Category,l1=l1,user=user,message="No product available for this category")

    return render_template('search.html',query=Category,l1=l1,user=user)       

@app.route('/viewbalance/<int:x>')

def viewbalance(x):
    global user
    user=User.query.filter_by(Email=user.Email).first()
    user1=User.query.filter_by(Email=user.Email).first()
    user1.balance=user1.balance+x
    db.session.commit()
    return render_template('viewbalance.html',user=user1)

@ app.route('/home_user/change_product/<id>', methods=['GET', 'POST'])
def changeproduct(id):
    form = ChangeProductForm()
   
    products=Products.query.filter_by(Pid=id).first()
    global user 

    if form.validate_on_submit():
        product=Products.query.filter_by(Pid=id).first()
        if product.Name!=None:
            product.Name=form.Productname.data
            db.session.commit()
        if product.Price!=None:
            product.Price=form.price.data
            db.session.commit()
        if product.mfgdate!=None:
            product.mfgdate=form.Mfgdate.data
            db.session.commit()
        if product.mfgcompany!=None:
            product.mfgCompany=form.Mfgcompany.data
            db.session.commit()
        if product.quantity!=None:
            product.quantity=form.Quantity.data
            db.session.commit()
        if product.Category!=None:
            product.Category=form.Category.data
            db.session.commit()
        if product.weight!=None:
            product.weight=form.weight.data
            db.session.commit()
        return render_template('change_quantity.html',user=user,form=form,product=products,success="Updated Successfully")
        

  
 
    return render_template('change_quantity.html',user=user,form=form,product=products)
@ app.route('/home_user/all_product/<id>', methods=['GET', 'POST'])
def allproduct(id):
    global user
    if user.IsSeller==0:
        return "You cannot update products right now,Please contact us for more information"
    products=Products.query.filter_by(Sellerid=id).all()
    return render_template('all_products.html',user=user,products=products)

@app.route('/home_user/viewproduct/negotiate/<int:id>',methods=['GET','POST'])
def negotiate(id):
    global user
    user=User.query.filter_by(Email=user.Email).first()
    product=Products.query.filter_by(Pid=id).first()
    seller=User.query.filter_by(User_id=product.Sellerid).first()
    convo=Negotiations.query.all()
    convo1=[]
    for c in convo:
        if c.Pid==id:
            if c.seller_id==seller.User_id:
                if c.buyer_id==user.User_id:
                    convo1.append(c)
    for c in convo1:
       if c.price!=-1:
        return render_template('negotiate.html',product=product,user=user,seller=seller,convo=convo1,flag=1,final_price=c.price)
    
    return render_template('negotiate.html',product=product,user=user,seller=seller,convo=convo1,flag=0)

@app.route('/home_user/negotiate_seller',methods=['GET','POST'])
def negotiate_seller():
    global user
    if user.IsSeller==0:
        return "You cannot see negotiations right now,Please contact us for more information"
    products=Products.query.filter_by(Sellerid=user.User_id).all()
    return render_template('all_product_negotiate.html',user=user,products=products)

@app.route('/home_user/negotiations/<int:id>',methods=['GET','POST'])
def seenegotiations(id):
    global user
    convo=Negotiations.query.filter_by(Pid=id).all()
    convcustomer=[]
    for c in convo:
        if c.buyer_id not in convcustomer:
            convcustomer.append(c.buyer_id)
    customers=[]
    for i in convcustomer:
        customers.append(User.query.filter_by(User_id=i).first())
    return render_template('seenegotiations.html',customers=customers,product=Products.query.filter_by(Pid=id).first(),user=user)

@app.route('/home_user/seenegotiation_seller/<int:id>/<int:pid>',methods=['GET','POST'])
def seenegotiation_seller(id,pid):
    global user
    user=User.query.filter_by(Email=user.Email).first()
    product=Products.query.filter_by(Pid=pid).first()
    customer=User.query.filter_by(User_id=id).first()
    convo=Negotiations.query.all()
    convo1=[]
    for c in convo:
        if c.Pid==pid:
            if c.seller_id==user.User_id:
                if c.buyer_id==customer.User_id and c not in convo1:
                    convo1.append(c)
    
    for c in convo1:
       if c.price!=-1:
        return render_template('negotiate_seller.html',product=product,user=user,customer=customer,convo=convo1,flag=1,success="Successfully Set the price")
    
    return render_template('negotiate_seller.html',product=product,user=user,customer=customer,convo=convo1,flag=0)

@app.route('/home_user/viewproduct/send_message_customer/<int:id>',methods=['GET','POST'])
def send_message_customer(id):
    global user
    user=User.query.filter_by(Email=user.Email).first()
    mess=request.form['mess']
    product=Products.query.filter_by(Pid=id).first()
    seller=User.query.filter_by(User_id=product.Sellerid).first()
    newc=Negotiations(Pid=id,seller_id=seller.User_id,buyer_id=user.User_id,Message=mess,sender_id=user.User_id,price=-1)
    db.session.add(newc)
    db.session.commit()
    convo=Negotiations.query.all()
    convo1=[]
    for c in convo:
            if c.Pid==id:
                if c.seller_id==seller.User_id:
                    if c.buyer_id==user.User_id:
                        convo1.append(c)
    
    return render_template('negotiate.html',product=product,user=user,seller=seller,convo=convo1,flag=0)

@app.route('/home_user/send_message_seller/<int:id>/<int:cid>',methods=['GET','POST'])
def send_message_seller(id,cid):
    global user
    user=User.query.filter_by(Email=user.Email).first()
    mess=request.form['mess']
    product=Products.query.filter_by(Pid=id).first()
    customer=User.query.filter_by(User_id=cid).first()
    newc=Negotiations(Pid=id,seller_id=user.User_id,buyer_id=cid,Message=mess,sender_id=user.User_id,price=-1)
    db.session.add(newc)
    db.session.commit()
    convo=Negotiations.query.all()
    convo1=[]
    for c in convo:
        if c.Pid==id:
            if c.seller_id==user.User_id:
                if c.buyer_id==customer.User_id and c not in convo1:
                    convo1.append(c)
    
    return render_template('negotiate_seller.html',product=product,user=user,customer=customer,convo=convo1,flag=0)

@app.route('/home_user/set_price/<int:id>/<int:cid>',methods=['GET','POST'])
def set_final_price(id,cid):
    global user
    user=User.query.filter_by(Email=user.Email).first()
    mess=request.form['price']
    product=Products.query.filter_by(Pid=id).first()
    customer=User.query.filter_by(User_id=cid).first()
    newc=Negotiations(Pid=id,seller_id=user.User_id,buyer_id=cid,Message="Final Price per product is "+mess+"\n Conversation ends here",sender_id=user.User_id,price=mess)
    db.session.add(newc)
    db.session.commit()
    convo=Negotiations.query.all()
    convo1=[]
    flag=1
    for c in convo:
        if c.Pid==id:
            if c.seller_id==user.User_id:
                if c.buyer_id==customer.User_id and c not in convo1:
                    convo1.append(c)
    for c in convo1:
       if c.price!=-1:
        return render_template('negotiate_seller.html',product=product,user=user,customer=customer,convo=convo1,flag=1,success="Successfully Set the price")
           
            
    
    return render_template('negotiate_seller.html',product=product,user=user,customer=customer,convo=convo1)

@app.route('/home_user/viewproduct/negotiate/final_buy/<int:pid>/<int:price>',methods=['GET','POST'])
def final_buy(pid,price):
    if request.method == 'POST':
        quantity=request.form.get('quantity')
    global user
    price=int(price)
    quantity=int(quantity)
    user=User.query.filter_by(Email=user.Email).first()
    product=Products.query.filter_by(Pid=pid).first()
    if user.balance>=quantity*price:
        user1 = User.query.filter_by(Email=user.Email).first()
        user1.balance=user1.balance-(quantity*(price))
        db.session.commit()
        print(user.balance)
        product.quantity=product.quantity-quantity
        db.session.commit()
        new_order=Orderdetails(pid=product.Pid,cid=user.User_id,quantity=quantity,Status=0,Price=price)
        db.session.add(new_order)
        db.session.commit()
        product=Products.query.filter_by(Pid=pid).first()
        seller=User.query.filter_by(User_id=product.Sellerid).first()
        convo=Negotiations.query.all()
        print(len(convo))
        convo1=[]
        for c in convo:
            if c.Pid==pid:
                if c.seller_id==seller.User_id:
                    if c.buyer_id==user.User_id:
                        convo1.append(c)
                        print(c)
   
        return render_template('negotiate.html',product=product,user=user,seller=seller,convo=convo1,flag=1,final_price=price,success="Succeessfully Bought the product")
        
    else: 
        return "Insufficient Balance"