# Import any DAObject classes that you will need
from docassemble.base.util import Individual, Person, DAObject
# Import the SQLObject and some associated utility functions
from docassemble.base.sql import alchemy_url, connect_args, upgrade_db, SQLObject, SQLObjectRelationship
# Import SQLAlchemy names
from sqlalchemy import Column, ForeignKey, Integer, String, Float, VARCHAR ,create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker  

# Only allow these names (DAObject classes) to be imported with a modules block
__all__ = ['Transaction'] 

metadata_obj = MetaData(schema="payment")

# Create the base class for SQLAlchemy table definitions
Base = declarative_base(metadata=metadata_obj) 
 
class TransactionModel(Base): 
    __tablename__ = 'Transaction_tbl' 
    id = Column(Integer, primary_key=True)
    Token = Column(String(250))
    Amount = Column(Integer)  
    Response = Column(String(250)) 
    Card_id = Column(String(250))
    Brand = Column(String(250))
    MaskedCard = Column(String(250))
    ExpiryMonth = Column(String(250))
    ExpiryYear = Column(String(250))
    Fingerprint = Column(String(250))
    Card_Object = Column(String(250))
    Country = Column(String(250))
    Charge_Object = Column(String(250))
    Charge_id = Column(String(250))
    Status = Column(String(250))

# Form the URL for connecting to the database based on the "demo db" directive in the Configuration
url = alchemy_url('demo db')
 
# Build the "engine" for connecting to the SQL server, using the URL for the database.
conn_args = connect_args('demo db')
if url.startswith('postgres'):
    engine = create_engine(url, connect_args=conn_args, pool_pre_ping=False)
else: 
    engine = create_engine(url, pool_pre_ping=False)
 
# Create the tables  
Base.metadata.create_all(engine)

# Get SQLAlchemy ready
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)()

# Perform any necessary database schema updates using alembic, if there is an alembic
# directory and alembic.ini file in the package.
upgrade_db(url, __file__, engine, version_table='auto', conn_args=conn_args)

class Transaction(DAObject, SQLObject):
    _model = TransactionModel
    _session = DBSession 
    _required = ['id'] 
    _uid = 'id' 

    def init(self, *pargs, **kwargs, ):
        super().init(*pargs, **kwargs)
        self.sql_init() 

    def db_get(self, column):
        if column == 'Token':     
            return self.token
        if column == 'Amount':     
            return self.amount
        if column == 'Response':     
            return self.response   
        raise Exception("Invalid column " + column)
        
    def db_set(self, column, value):
        if column == 'Token':
            self.token = value
        if column == 'Amount':
            self.amount = value
        if column == 'Response':
            self.response = value
 

    def db_null(self, column):   
        if column == 'Token': 
                del self.token
        if column == 'Amount': 
                del self.amount
        if column == 'Response': 
                del self.response   


     




        
    
    