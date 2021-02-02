import requests
from bs4 import BeautifulSoup
import pymysql
import re

# css选择器定位标签
def get_informations(html,names,others,values,quotes):
    soup = BeautifulSoup(html, "lxml")
    name_list = soup.select('div.hd > a > span:nth-of-type(1)')
    for each in name_list:
        movie = each.text.strip()
        names.append(movie)
    #日期+地区+类型
    date_list=soup.select('div.bd > p:nth-of-type(1)')
    for each in date_list:
        other = ("".join((each.text.strip()).split("\n")[1].split())).split("/")
        others.append(other)
        '''
        dates.append(others[0])
        areas.append(others[1])
        genres.append(others[2])
        dates.append((re.findall('\d\d\d\d',other)[0]))   #单独正则表达式提取时间
        '''
    #分值
    value_list=soup.select('div.bd > div > span.rating_num')
    for each in value_list:
        value = each.text.strip()
        values.append(value)
    #语录
    '''quote_list=soup.select('div.info > div.bd > p.quote > span')
    quote_list = []      #该方法对空信息无法提取，且会出现错位现象''' 
    for i in range(1, 26):
        q = soup.select('div > div.article > ol > li:nth-of-type('+str(i)+') > div > div.info > div.bd > p.quote > span')
        #语录关键词索引目录 根据序号进行提取，避免空字符无法提取
        if len(q) > 0:
            quote = q[0].text.strip()
        else:
            quote = ''     
        quotes.append(quote)
 
def get_movies(names,others,values,quotes):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'Host': 'movie.douban.com'
    }
    for i in range(0,10):
        #逐页进行提取
        link = 'https://movie.douban.com/top250?start='+str(i*25)
        r = requests.get(link, headers=headers, timeout=10)
        get_informations(r.text,names,others,values,quotes)

def main():
    names=[]  #记录电影名
    others=[] #记录其他信息
    values=[] #记录评分
    quotes=[] #记录语录
    get_movies(names,others,values,quotes)
    numlist=[]
    for j in range(len(names)):
        numlist.append(j+1)
    connent = pymysql.connect(host='localhost', user='root', passwd='981121', db='test', charset='utf8') #db为所使用的数据库
    cursor = connent.cursor()
    for i in range(len(names)):
        sql="insert into test values("+str(numlist[i])+","+"'"+names[i]+"'"+","+str(values[i])+","+str(re.findall('\d{4}',others[i][0])[0])+","+'"'+others[i][1]+'"'+","+'"'+others[i][2]+'"'+","+'"'+quotes[i]+'"'+")"
        #test为表名，其结构为test(id,name,value,date,area,genre,quote)
        #由于list[0]和list[1]的元素类型是整型，所以需要将其转化为字符串，list[2]本身为字符串类型，但需要加入单引号''，
        #sql语句中values的值为字符串的拼接，每个从列表中获取的元素为表的一个字段
        #print(sql)   #在控制台上打印sql语句
        cursor.execute(sql)
        connent.commit()   #提交任务，数据才会写入数据库
if __name__=='__main__':
    main()

