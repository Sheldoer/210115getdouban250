# getdouban250
读取豆瓣250电影信息存入仓库
实现方法与所涉及函数与库：
1.实现方法
采用beautiful soup库对豆瓣https://movie.douban.com/top250页面进行信息读取
根据目录来选取自己所采集的信息
把采集的信息放入列表，然后对数据库进行输入
2.涉及函数与库
所用的库包含requests库：对页面进行提取
beautiful soup库：对采集信息的提取
re库：部分信息补充方法
pymysql库：对数据库进行输入
