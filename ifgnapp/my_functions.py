import string, random
from datetime import datetime as dt
from django.db.models import F, Q
import  re, random
from django.utils.text import slugify
from django.db.models import Max
from PIL import Image
from django.http import HttpResponse, HttpResponseRedirect, FileResponse


def rand_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
     """
     used to generate random  string with a given lenght.
     """
     return ''.join(random.choice(chars) for _ in range(size))

def break_txt(txt):
     """To break text contents before display. It replaces all break spaces with the `<br>` tag so it will be displayed properly in the html DOM"""
     my_txt = str(repr(txt))
     from ast import literal_eval
     ## break text....
     if '\\n' and '\\r' in my_txt:
          new_txt = my_txt.replace('\\n', '<br>').replace('\\r', '')
          return literal_eval(new_txt)
     elif '\\r' in my_txt:
          new_txt = my_txt.replace('\\r', '<br>')
          return literal_eval(new_txt)
     elif '\\r' in my_txt:
          new_txt = my_txt.replace('\\r', '<br>')
          return literal_eval(new_txt)
     else:
          new_txt = my_txt.replace('\\n', '<br>')
          return literal_eval(new_txt)



def format_txt(txt):
     """To format and edit text"""
     my_txt = str((txt))
     # ##h1 and ##eh1
     # check if the tag is added corectly..
     if '##h1' in my_txt:
          if '##eh1' not in my_txt:
               raise ValueError('Please check and close one of your ##h1/##eh1 tag correctly!')
     if '##h2' in my_txt:
          if '##eh2' not in my_txt:
               raise ValueError('Please check and close one of your ##h2/##eh2 tag correctly!')
     if '##h3' in my_txt:
          if '##eh3' not in my_txt:
               raise ValueError('Please check and close one of your ##h3/##eh3 tag correctly!')
     if '##h4' in my_txt:
          if '##eh4' not in my_txt:
               raise ValueError('Please check and close one of your ##h4/##eh4 tag correctly!')
     if '##pr' in my_txt:
          if '##epr' not in my_txt:
               raise ValueError('Please check and close one of your ##pr/##epr tag correctly!')
     if '##dv' in my_txt:
          if '##edv' not in my_txt:
               raise ValueError('Please check and close one of your ##dv/##edv tag correctly!')
     if '##b' in my_txt:
          if '##eb' not in my_txt:
               raise ValueError('Please check and close one of your ##b/##eb tag correctly!')
     if '##ar' in my_txt:
          if '##ear' not in my_txt:
               raise ValueError('Please check and close one of your ##ar/##ear tag correctly!')
     if '##ul' in my_txt:
          if '##eul' not in my_txt:
               raise ValueError('Please check and close one of your ##ul/##eul tag correctly!')
     
     if '##lis' in my_txt:
          if '##elis' not in my_txt:
               raise ValueError('Please check and close one of your ##lis/##elis tag correctly!')
     
     if '##olis' in my_txt:
          if '##eolis' not in my_txt:
               raise ValueError('Please check and close one of your ##olis/##eolis tag correctly!')
     
     if '##sp' in my_txt:
          if '##esp' not in my_txt:
               raise ValueError('Please check and close one of your ##sp/##esp tag correctly!')
     
     # replace html tags
     my_txt = my_txt.replace('##h1', '<h1>').replace('##eh1', '</h1>').replace('##h2', '<h2>').replace('##eh2', '</h2>')
     my_txt = my_txt.replace('##h3', '<h3>').replace('##eh3', '</h3>').replace('##h4', '<h4>').replace('##eh4', '</h4>')
     my_txt = my_txt.replace('##pr', '<p>').replace('##epr', '</p>').replace('##b', '<b>').replace('##eb', '</b>')
     my_txt = my_txt.replace('##nl', '<br>').replace('##ar', '<article>').replace('##ear', '</article>')
     my_txt = my_txt.replace('##dv', '<div>').replace('##edv', '</div>')
     my_txt = my_txt.replace('##olis', '<ol>').replace('##eolis', '</ol>')
     my_txt = my_txt.replace('##lis', '<li>').replace('##elis', '</li>')
     my_txt = my_txt.replace('##ulis', '<ul>').replace('##eulis', '</ul>')
     my_txt = my_txt.replace('##qt', '<q>').replace('##eqt', '</q>')
     my_txt = my_txt.replace('##it', '<i>').replace('##eit', '</i>')
     my_txt = my_txt.replace('##sp', '<span>').replace('##esp', '</span>')

     return my_txt



def check_comment(tx):
     """use to check if a text contains some special characters, and if yes it replaces them with empty space."""
     text_tocheck = tx.translate(str.maketrans({
        ';': '',  '<': '',  '>': '', '+': '',  '-': '',  
        '~': '',    '|': '',   '^': '', '[': '', ']': '',   
        ')': '',    '(': '',  '$': '', '`': '',  
        '+': '',  '=': '', '/': '', '\\': '', '{': '', '}': '', 
     }))
     text_count = len(text_tocheck)
     if text_count > 500:
          text_tocheck = ''
          return
     else: 
          return text_tocheck
     # return text_tocheck

def convert_promote(prom):
     """use to convert yes to True and no to False"""
     promote_txt = str(prom)
     if promote_txt == 'yes':
          new_promote = True
     elif promote_txt == 'no':
          new_promote = False 
     else:
          raise ValueError('invalid format')       
     return new_promote

def email_checker(e):
    """ regex for validating email addresses, it takes just one arg which is the email and return the email or invalid if the email is not valid,"""
    email = str(e)
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
     #    print(f"Email is valid and is {email}")
        return email
    else:
     #    print("Email is invalid")
        return 'invalid'

# email_checker('king@gmail.com')

def handle_time(ti):
     """used to remake date from user-uploads"""
     rets = ('unknown time format!')
     try:
          check_time = str(ti).replace('{ch}'.format(ch="/"), '-').replace(';', '-').replace(',', '-')
          has_formated_tm = dt.strptime(str(check_time), '%Y-%m-%d')
          if has_formated_tm:
               rets = has_formated_tm
          else:
               pass
     except:
          pass
     return rets


def check_text(tx):
     """use to check if a text some special characters, and if yes it converts them back to text"""
     text_tocheck = tx.translate(str.maketrans({
        ';': 'semicolonChar',  '<': 'lessthanChar',  '>': 'graterChar',  
        '~': 'homeChar',    '|': 'pipChar',   '^': 'uptickChar',  
        ':': 'cholonChar',    '%': 'moduloChar',  '$': 'dollarChar',  
        '#': 'hashtagChar',  '*': 'wildChart',    '`': 'backtickChar',  
        '+': 'plusChar',  '=': 'equalChar',
     }))
     text_count = len(text_tocheck)
     if text_count > 90:
          text_tocheck = ''
          return
     else: 
          return text_tocheck
     # return text_tocheck

 
def date_converter(dt_val, _typ):
     """Used to get gap in days 
     >> requires 2 params(`dt_val, _typ`)
     >> value of `dt_val` is `the date in "2020-10-25"` format
     >> value of `_typ` is `F` for future or `B` for past"""
     try:
          today_date = dt.now()
          if str(_typ) == "F":
               date_to_format = dt.strptime(dt_val, "%Y-%m-%d")
               format_date = date_to_format - today_date
               return {
                    "status": True,
                    "type": "FUTURE",
                    "data": format_date.days
               }
          else:
               date_to_format = dt.strptime(dt_val, "%Y-%m-%d")
               format_date = today_date - date_to_format
               # print(format_date)
               if format_date.days == 0: 
                    format_date = str('today')
                    # print('today')
               elif format_date.days == 1:
                    format_date = str('yesterday')
               elif format_date.days < 0:
                    format_date = str('today')
               else:
                    format_date = '{day} days ago'.format(day=format_date.days) 
                    return format_date

               return {
                    "status": True,
                    "type": "PAST",
                    "data": format_date,
               }
     except:
          return {
               "status": False,
               "type": "ERROR",
               "data": ""
          }
# print(f'\n>>: {date_converter("2021-07-18", "B")}')


def text_filter(txt, _max=None):
    """This function is convinient for removing special charaters from a give sentence.
    Usage:: The first parameter is you sentence, and the secound parameter is the maximum lenght you want the text in your first parameter to be. And when the lenght is set and your input passes it, it will not get errors rather it cut of the extra text away and retun the exact lenght that is specified. 
     Note the "",?,#,_!,@,&,*" will not be removed from the text.  """
    txt = str(txt)
    limit = _max
    filtered_txt = ''
    try:
        # first we try filtering the text with translate(), this will never fail but if it fails, we regex below..
        filtered_txt = txt.translate(str.maketrans({
        ';': '', '<': '',  '>': '', '+': '',  '-': ' ', ':': '', '`': '',
        '~': '', '|': '',   '^': '', '[': '', ']': '', '¢':'','=': '',  
        ')': '', '(': '',  '$': '', '`': '', '§':'','%':'','¥':'','€':'',  
        '+': '', '=': '', '/': '', '\\': '', '{': '', '}': '','°':'','£':'', 
        }))
        if limit is not None:
            limit = int(limit)
            filtered_txt = filtered_txt[0:limit]
        else:
            pass
    except:    
        # lets go with regex incase it escape the first one..
        filtered_txt = re.sub('[^A-Za-z0-9 ]+', '', txt)
        if limit is not None:
            limit = int(_max)
            filtered_txt = filtered_txt[0:limit]
        else:
            pass    
    # print(f'Our filtered text is == {filtered_txt}, while our initial text is == {txt}')
    return filtered_txt 

def loop_model(m_name, dump_list):
    m_n = m_name
    _d_lst = dump_list
    for h in m_n:
        _d_lst.append(h)
    return _d_lst

def rem_words(w, _len=None):
    """This function removes letter words if a specified lenght from a given sentence, it takes two args, the first is your sentence and the second(optional) is the lenght of words you wish to remove. But by default it removes all three(3) lettered words and also some other words like "also, where, will, when, that, some, when, such, they, them" respectively """
    _w = str(w).split(' ')
    _nw = []
    try:
        _len = 3 if _len == None else int(_len)
    except:
        _len = 3    
    _ls_str = ''
    for i in _w:
        if len(i) <=_len or i == 'also' or i == 'that' or i == 'does' or i =='where' or i == 'will' or i == 'when' or i=='such' or i=='they' or i=='them':
            continue
        else:
            _nw.append(i)
    _ls_str = str(_nw).replace(',', '').replace('[', '').replace(']', '').replace('"', '').replace("'", '') 
    print(_ls_str)     
    return _ls_str  

def img_color_reader(img):
	# Get width and height of Image
	width, height = img.size

	# Initialize Variable
	r_total = 0
	g_total = 0
	b_total = 0
	count = 0

	# Iterate through each pixel
	for x in range(0, width):
		for y in range(0, height):
			# r,g,b value of pixel
			r, g, b = img.getpixel((x, y))

			r_total += r
			g_total += g
			b_total += 9
			count += 1

	return (r_total/count, g_total/count, b_total/count)

my_txt = "who we are, and how we are going to make impact is what they don't know"
# my_match = re.sub('[a-zA-Z0-9"\')()]{16,20}?', 'ugo', my_txt)
# print(my_match)