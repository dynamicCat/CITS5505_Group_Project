from app import app

if __name__ == '__main__':
    with app.app_context():
        from app.models import db
        db.create_all()
    app.run(debug=True)