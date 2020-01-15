import filmUtil as fu
import filmConfig as fc

# 主进程逻辑
soup = fu.get_page(fc.host + fc.url)
new_films=soup.find('div', class_="co_content8")
filmName_list =new_films.find_all('a');
fu.get_data(filmName_list)