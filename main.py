import filmUtil as fu
import filmConfig as fc

# 主进程逻辑
# 获取主页精品的各个电影条目
soup = fu.get_page(fc.host + fc.url)
# 解析出详细页的地址
new_films=soup.find('div', class_="co_content8")
filmName_list =new_films.find_all('a');
# 爬取详细页的内容并保存
fu.get_data(filmName_list)