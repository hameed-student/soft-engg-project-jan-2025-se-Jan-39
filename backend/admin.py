from app import db, User, app

def create_admin():
    with app.app_context():
        if User.query.filter_by(role="admin").first() is None:
            email = "admin@admin.com"
            password = "Pass@123"
            name = "ADMIN"
            role = "admin"
            user = User(name=name, email=email, role=role)
            user.set_password(password)
            db.session.add(user)
        user = User(name="student", email="student@app.com", role="student")
        user.set_password("Pass@123")
        db.session.add(user)
        user = User(name="support", email="support@app.com", role="support_staff")
        user.set_password("Pass@123")
        db.session.add(user)
        db.session.commit()
        print("demo data added to db...")
        
if __name__ == '__main__':
    create_admin()

