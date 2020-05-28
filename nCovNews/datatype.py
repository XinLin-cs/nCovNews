from nCovNews import db

class USER(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    userid = db.Column( db.String(20) )  
    name = db.Column( db.String(20) )  
    password = db.Column( db.String(20) ) 

class PROVINCE(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    date = db.Column( db.Date )  
    name = db.Column( db.String(20) )  
    confirmed = db.Column( db.Integer )  
    cures = db.Column( db.Integer )  
    deaths = db.Column( db.Integer )
    asymptomatic = db.Column( db.Integer )  

class CHINATOTAL(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    date = db.Column( db.Date )  
    confirmed = db.Column( db.Integer )  
    suspected = db.Column( db.Integer ) 
    suspectedInc = db.Column( db.Integer )
    cures = db.Column( db.Integer )  
    deaths = db.Column( db.Integer ) 
    asymptomatic = db.Column( db.Integer )  

class COUNTRY(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    date = db.Column( db.Date )  
    name = db.Column( db.String(20) )  
    continent = db.Column( db.String(20) )  
    confirmed = db.Column( db.Integer )  
    cures = db.Column( db.Integer )  
    deaths = db.Column( db.Integer )  

class CONTIENT(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    date = db.Column( db.Date )  
    name = db.Column( db.String(20) )  
    confirmed = db.Column( db.Integer )  
    cures = db.Column( db.Integer )  
    deaths = db.Column( db.Integer )  

class WORLDTOTAL(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    date = db.Column( db.Date )  
    confirmed = db.Column( db.Integer )  
    cures = db.Column( db.Integer )  
    deaths = db.Column( db.Integer ) 

class NEWS(db.Model):
    id = db.Column(db.Integer, primary_key=True)   
    date = db.Column( db.FLOAT ) 
    title = db.Column( db.String(20) )  
    summary = db.Column( db.String(20) )  
    info = db.Column( db.String(20) )  
    url = db.Column( db.String(20) )  

class FAKENEWS(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column( db.String(20) )  
    summary = db.Column( db.String(20) )  
    info = db.Column( db.String(20) )  

class INFORMATION(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column( db.String(20) )  
    summary = db.Column( db.String(20) )  
    info = db.Column( db.String(20) )  

class DISCUSS(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    date = db.Column( db.DateTime )  
    userid = db.Column( db.String(20) )
    username = db.Column( db.String(20) )  
    word = db.Column( db.String(20) )   
    likes = db.Column( db.Integer ) 
    replyto = db.Column( db.Integer ) 