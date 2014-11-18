from flask import render_template
from flask import request
from app import app
import pymongo, datetime
from pymongo import MongoClient
import operator
import statistics
import re
from nlp_module import nlpClassify

DEBUG = False

client = MongoClient('mongodb://dev.proptiger-ws.com:27017/')
db5 = client['analytics5']
actions = db5.actions
people   = db5.people



#Assigning Values to the conversations
talkValues = {}
##################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
##################################
talkValues['No Relevant conversation'] = 2
talkValues['Sorry Not able to classify'] = 1
##

#Reading event Values from a file 
with open('/home/sysadmin/user-analytics/app/static/event_value.txt') as f:
  evListBuyer    = {}
  evListSearcher = {}
  for line in f.readlines():
    e,buyerVal,searcherVal = line.rstrip().split(',')
    evListBuyer[e]    = float(buyerVal)
    evListSearcher[e] = 10 - evListBuyer[e]
##    
  

  
#Reading buyers from a file
with open('/home/sysadmin/user-analytics/app/static/buyers.txt') as f:
  buyers = []
  for line in f.readlines():
    buyers.append(line.rstrip())    
##

#################################################
#################Main Routes#####################
#################################################    
@app.route('/')
@app.route('/index')
def index():  
  return render_template("index.html")

@app.route('/about')
def about():
  return render_template("about.html")

@app.route('/score_card')
def score_card():
  return render_template("score_card.html")

PER_PAGE = 100
@app.route('/registered_users')
@app.route('/registered_users/<alph>/', defaults={'page': 1})
@app.route('/registered_users/<alph>/<int:page>')
def reg_users(alph = None,page=None):  
  if alph:        
    num_of_records_to_skip = 0
    pages_required = 1
    regx_name  = re.compile('^'+alph, re.IGNORECASE)  
    tot_num_of_users = people.find({'name':regx_name},{'name':1,'_id':0}).count()
        
    if tot_num_of_users > PER_PAGE:      
      pages_required = tot_num_of_users/PER_PAGE + 1      
      num_of_records_to_skip = PER_PAGE*(page-1)
    dict_users = people.find({'name':regx_name},{'name':1}).sort('name').skip(num_of_records_to_skip).limit(PER_PAGE) 
    users = []
    for d_user in dict_users:
      users.append((d_user['_id'],d_user['name']))
    users_len = len(users)
    return render_template('registered_users_list.html',users_len=users_len,users=users,alph=alph,pages = pages_required)    
  else:
    return render_template("registered_users.html")

@app.route('/registered_users/buyers')
def reg_user_buyers():
  buyer_names = []
  for buyer_id in buyers:
    info = people.find_one({'_id':buyer_id})
    if info:
      buyer_names.append(info['name'])
    else:
      buyer_names.append('Not found')              
  rows = len(buyers)/3  
  return render_template("buyers.html",buyer_names=buyer_names, buyers = buyers, rows = rows)


@app.route('/evm')
def evm():
  evmList = []
  for e in evListBuyer:
    evmList.append((e,evListBuyer[e],evListSearcher[e]))    
  return render_template("evm.html", evmList=evmList)

@app.route('/feedback')
def feedback():
  return render_template("feedback.html")


@app.route('/search_results')
def search_results():
  
  email  = str(request.args.get('email'))
  name   = str(request.args.get('name'))
  number = str(request.args.get('number'))    
  
  #if email =
  regx_email = re.compile(email, re.IGNORECASE)
  regx_name  = re.compile(name, re.IGNORECASE)  
  regx_number= re.compile(number, re.IGNORECASE)
  ##################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
##################################
    
  for doc in document:
    results.append(doc)
    
  return render_template("search_results.html", results = results)


@app.route('/user')
@app.route('/user/<id>')
def user_activity(id=None):  
  try:    
    if id:            
      document = actions.find({"distinct_id":id})
    else:      
      id  = str(request.args.get('distinct_id'))
      document = actions.find({"distinct_id":id})
    
    if DEBUG:
      print 'checkpoint1'
    #PEOPLE_INFO 
    info = people.find_one({'_id':id})      
    pers_info = {}    
    pers_info['name']   = 'not found'
    pers_info['Mobile'] = 'not found'
    pers_info['email']  = 'not found'
    pers_info['status'] = 'not found'
     
    ##TO DO LATER
    ##Change this dumb piece of code
    if info:
      pers_info['name']	 = info['name']
      pers_info['Mobile']= info['Mobile']
      pers_info['email'] = info['email']
      ##################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
##################################
	pers_info['status'] = 'Case Logged In'
      elif status_code == 21:
	pers_info['status'] = 'Bank Processing'
      elif status_code == 22:
	pers_info['status'] = 'Sanctioned'
      elif status_code == 23:
	pers_info['status'] = 'Disbursement Required'
      elif status_code == 24:
	pers_info['status'] = 'Disbursed'
      elif status_code == 25:
	pers_info['status'] = 'Not Interested'
      elif status_code == 26:
	pers_info['status'] = 'Not Eligible'
      else :
	pers_info['status'] = 'Something weird -'+str(status_code)
  
    
    if DEBUG:
      print 'checkpoint2'              
    ##PEOPLE_INFO_END  
    
    #E_LIST
    if document:
      e_list = []
      conv_list = []
      vListBuyer    = []
      vListSearcher = []
      for event in document:
	if 'event' in event:
	  e_name = str(event['event'])
	  temp = datetime.datetime.fromtimestamp(int(event['time']) )	  
	  vListBuyer.append(evListBuyer[e_name])
	  vListSearcher.append(evListSearcher[e_name])
	  e_time = (temp.year,temp.month,temp.day,temp.hour,temp.minute,temp.second)
	  e_list += [{'e_name':e_name,'e_time': e_time, 'type':1}]      
##################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
##################################
	  
    else :
      return "not found" 
    e_list = sorted(e_list, key=lambda k: k['e_time'])
    ##E_LIST_END               
    
    
    #DET_VIEW_LIST 
    det_view_list = []
    for e in e_list:
      if e['type'] == 1:
	time  = e['e_time']
	event = e['e_name']
	category = 'Online Event'
	score = evListBuyer[e['e_name']]
      else:
	time  = e['e_time']
	event = e['e_name']
	category = nlpClassify(e['e_name'])
	score = talkValues[category]	
      det_view_list.append((time,event,category,score))
    ##DET_VIEW_LIST_END    
    
    conv_analysis_list = [(conv,nlpClassify(conv)) for conv in conv_list]  
    analysis_list = [nlpClassify(conv) for conv in conv_list]  
  
    #CALCULATING SCORE 
    buyer_score = 0    
    if 'Booking Related'  in analysis_list:
      buyer_score = 9
    elif 'Payment Related' in analysis_list:
      buyer_score = 8
    elif 'Site Visit Related' in analysis_list:
      buyer_score = 6
    elif 'Property being discussed' in analysis_list:
      buyer_score = 4
    elif 'No Relevant conversation' in analysis_list:
      buyer_score = 2
    else:
      buyer_score = 1
    
    
    if DEBUG:
      print 'checkpoint3'    
      
    #Calculations
    report = {}
  
    t = e_list[-1]['e_time']   
    ##################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
##################################
    
    
    report['mean'] =  buyer_score + online_mean_score*(10.0-buyer_score)/10.0
    #report['searcherScore'] =  statistics.mean(vListSearcher)    
    report['searcherScore'] = 10.0-report['mean']
    if DEBUG:
      print 'checkpoint4'    
        
  except Exception,e:
    print Exception, e
  
  return render_template("user_timeline.html",det_view_list = det_view_list, conv_analysis_list =conv_analysis_list, report = report, pers_info = pers_info, e_coda_list = e_list, did = id )

#################################################
##################Lab Routes#####################
#################################################
@app.route('/lab')
def lab():
  return  'Lab Home Page'

@app.route('/lab/detailed_analysis/<id>')
def detailed_analysis(id=None):  
  
  document = actions.find({"distinct_id":id})
  
  #CONVERSATION_LIST
  conv_list = []
  if document:          
    for event in document:
      if 'event' in event:
	pass
      else:  	
	conv_list.append(event['description'])	  	    
  ##END CONVERSATION_LIST
  ##TODO CATCH ELSE CASE
  
  conv_analysis_list = [(conv,nlpClassify(conv)) for conv in conv_list]  
  
  #CALCULATING SCORE 
  buyer_score = 0
  analysis_list = [x[1] for x in conv_analysis_list]
  if 'Booking Related'  in analysis_list:
    ##################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
####################################################################
########## CODE REMOVED ##########
##################################
  elif 'No Relevant conversation' in analysis_list:
    buyer_score = 2
  else:
    buyer_score = 1
    
  ##END CALCULATING SCORE
  
  return render_template("detailed_analysis.html",conv_analysis_list=conv_analysis_list,buyer_score=buyer_score)