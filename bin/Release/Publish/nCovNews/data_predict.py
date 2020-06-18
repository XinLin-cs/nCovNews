# 指数平滑法：a平滑系数

# 1次指数平滑法
def result1(timeseries,data,a=0.5):
    num = []
    for item in data:
        num.append(item[1])
    s = [num[1]]
    for i in range(0,len(timeseries)-1):
        if i>=len(data)-1:
            num.append(s[i])
        s.append( a * num[i+1] + ( 1 - a ) * s[i] )
    reslist=[]
    for i in range(0,len(timeseries)-1):
        reslist.append([timeseries[i+1],int(s[i])])
    return reslist

# 2次指数平滑法
def result2(timeseries,data,a=0.5):
    num = []
    for item in data:
        num.append(item[1])
    s = [num[1]]
    ss = [num[1]]
    for i in range(0,len(timeseries)-1):
        if i>=len(data)-1:
            x = 2 * s[i] - ss[i]
            y = a / (1-a) * ( s[i] - ss[i] )
            num.append(x+y)
        s.append( a * num[i+1] + ( 1 - a ) * s[i] )
        ss.append( a * s[i+1] + ( 1 - a ) * ss[i] )
    reslist=[]
    for i in range(0,len(timeseries)-1):
        x = 2 * s[i] - ss[i]
        y = a / (1-a) * ( s[i] - ss[i] )
        reslist.append([timeseries[i+1],int(x+y)])
    return reslist

# 3次指数平滑法
def result3(timeseries,data,a=0.5):
    num = []
    for item in data:
        num.append(item[1])
    s = [num[1]]
    ss = [num[1]]
    sss = [num[1]]
    for i in range(0,len(timeseries)-1):
        if i>=len(data)-1:
            x = 3 * s[i] - 3 * ss[i] + sss[i]
            y = a / (2*(1-a)*(1-a)) * ((6-5*a)*s[i]-(10-8*a)*ss[i]+(4-3*a)*sss[i])
            z = a*a / (2*(1-a)*(1-a)) * (s[i]-2*ss[i]+sss[i])
            num.append(x+y+z)
        s.append( a * num[i+1] + ( 1 - a ) * s[i] )
        ss.append( a * s[i+1] + ( 1 - a ) * ss[i] )
        sss.append( a * ss[i+1] + ( 1 - a ) * sss[i] )
    reslist=[]
    for i in range(0,len(timeseries)-1):
        x = 3 * s[i] - 3 * ss[i] + sss[i]
        y = a / (2*(1-a)*(1-a)) * ((6-5*a)*s[i]-(10-8*a)*ss[i]+(4-3*a)*sss[i])
        z = a*a / (2*(1-a)*(1-a)) * (s[i]-2*ss[i]+sss[i])
        reslist.append([timeseries[i+1],int(x+y+z)])
    return reslist
