from . import app,db
from .Classes import Cart,User,OPtobepassed,Orderdetails,Products
from .user_interface import *
from .manager_interface import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/osp_db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

def update():
    orders=Orderdetails.query.all()
    from datetime import datetime

# datetime object containing current date and time
    now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    for order in orders:
        # order_date = datetime.strptime(str(order.date), '%y-%m-%d %H:%M:%S')
        # print(1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111)
        # print((order.date.date()))
        # print((now.date()))
        x=(-1)*int(((order.date).date()-now.date()).days)
        print(x)
        if x>=3:
            order.Status=1
            db.session.commit()



@app.route('/')
def home():
    update()
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
