from utils import role_jwt_required
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from models import (db, Users, Profiles, Tournaments, Flights, Swaps, Buy_ins,
    Transactions, Devices)


# @role_jwt_required(['user'])
def SetupAdmin(app):

    class ExcludedModelView(ModelView):
        form_excluded_columns = ['created_at', 'updated_at', 'password', 'counter_swap2']
    
    admin = Admin(app, name='Swap Profit', template_mode='bootstrap3')

    admin.add_view( ExcludedModelView( Users, db.session ))
    admin.add_view( ExcludedModelView( Profiles, db.session ))
    admin.add_view( ExcludedModelView( Tournaments, db.session ))
    admin.add_view( ExcludedModelView( Flights, db.session ))
    admin.add_view( ExcludedModelView( Swaps, db.session ))
    admin.add_view( ExcludedModelView( Buy_ins, db.session ))
    admin.add_view( ExcludedModelView( Transactions, db.session ))
    admin.add_view( ExcludedModelView( Devices, db.session ))

    return admin