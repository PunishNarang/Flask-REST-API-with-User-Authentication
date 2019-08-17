from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

#from security import authenticate,identity
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import ItemList,Item
from resources.store import Store, StoreList
from blacklist import BLACKLIST

app  = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'punish'  #app.config['JWT_SECRET_KEY']
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return {
        'description':'The token has expired',
        'error':'Token_expired'
    }, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
        'description':'Signature Verification failed',
        'error':'Invalid_expired'
    }, 401

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return {
        'description':'Request does not contain access token',
        'error':'Authorization_required'
    }, 401

@jwt.needs_fresh_token_loader
def fresh_token_callback():
    return {
        'description':'The Token is not fresh',
        'error':'Fresh_token_required'
    }, 401

@jwt.revoked_token_loader
def revoked_token__callback():
    return {
        'description':'The token has been revoked',
        'error':'token_revoked'
    }, 401


#items = []--->in memory dB
api.add_resource(Store,'/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister,'/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')



if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)
