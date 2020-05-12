from nCovNews import db

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



class User(db.Model):  # ���������� user���Զ����ɣ�Сд�����
    id = db.Column(db.Integer, primary_key=True)  # ����
    name = db.Column(db.String(20))  # ����

class Movie(db.Model):  # ���������� movie
    id = db.Column(db.Integer, primary_key=True)  # ����
    title = db.Column(db.String(60))  # ��Ӱ����
    year = db.Column(db.String(4))  # ��Ӱ���

def sample():
    db.drop_all()
    db.create_all()

    user = User(name='Grey Li')  # ����һ�� User ��¼
    m1 = Movie(title='Leon', year='1994')  # ����һ�� Movie ��¼
    m2 = Movie(title='Mahjong', year='1996')  # �ٴ���һ�� Movie ��¼
    db.session.add(user)  # ���´����ļ�¼��ӵ����ݿ�Ự
    db.session.add(m1)
    db.session.add(m2)
    db.session.commit()  # �ύ���ݿ�Ự��ֻ��Ҫ��������һ�μ���

    movie = Movie.query.first()  # ��ȡ Movie ģ�͵ĵ�һ����¼������ģ����ʵ����
    print(movie.id)
    list = Movie.query.all()  # ��ȡ Movie ģ�͵����м�¼�����ذ������ģ����ʵ�����б�
    print(list)
    num = Movie.query.count()  # ��ȡ Movie ģ�����м�¼������
    print(num)
    tmp = Movie.query.get(1)  # ��ȡ����ֵΪ 1 �ļ�¼
    print(tmp)
    tmp = Movie.query.filter_by(title='Mahjong').first()  # ��ȡ title �ֶ�ֵΪ Mahjong �ļ�¼
    print(tmp)
    tmp = Movie.query.filter(Movie.title=='Mahjong').first()  # ��ͬ������Ĳ�ѯ����ʹ�ò�ͬ�Ĺ��˷���
    print(tmp)