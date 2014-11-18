#! /usr/bin/env python
# Author : Khaleeque Ansari
# Company: www.proptiger.com
# This is nlp module written for parsing and 
# understanding Proptiger CRM conversation flow

#IS VALID
def isValid(talk):  
  if 'switch' in talk:
    return False
  elif 'pick' in talk:
    return False
  elif 'back' in talk:
    return False
  elif 'reachable' in talk:
    return False
  elif 'busy' in talk:
    return False
  elif 'disconnected' in talk:
    return False    
  elif 'call' in talk:
    if ('later' in talk) or ('after' in talk) or ('not' in talk):
      return False
  elif 'number' in talk:
    if ('invalid' in talk) or ('wrong' in talk):
      return False
  elif 'not' in talk:
    if ('interest' in talk) or ('look' in talk) or ('recieve' in talk):    
      return False
  return True  
##END IS VALID

#IS PROPERTY BEING DISCUSSED
def isPropertyBeingDiscussed(talk):
  if 'floor' in talk:
    return True
  if 'project' in talk:
    return True
  if 'bhk' in talk:
    return True
  if 'sector' in talk:
    return True
  if 'villa' in talk:
    return True
  if 'developers' in talk:
    return True
  if 'builders' in talk:
    return True
  elif 'property' in talk:
    return True
  return False
##END IS PROPERTY BEING DISCUSSED

#SITE VISIT RELATED
def isSiteVisitRelated(talk):
  if 'site' in talk or 'visit' in talk or 'coming' in talk:
    return True
  return False
##END SITE VISIT RELATED

#PAYMENT RELATED
def isPaymentRelated(talk):
  if 'cheque' in talk or 'RTGS' in talk :
    return True
  return False
##END PAYMENT RELATED

#BOOKING RELATED
def isBookingRelated(talk):
  if 'book' in talk or 'block' in talk :
    return True
  return False
##END BOOKING RELATED

###
## this classify function takes text
## as input and returns a tag for that text
## as whether it is site visit related or
## peoperty discussion
###
#CLASSIFY
def nlpClassify(text):
  try:
    text = (text).lower()
    #print text
    if isValid(text):
      if isBookingRelated(text):
	return 'Booking Related'
      elif isPaymentRelated(text):
	return 'Payment Related'
      elif isSiteVisitRelated(text):
	return 'Site Visit Related'
      elif isPropertyBeingDiscussed(text):
	#print 'Property being discussed'
	return 'Property being discussed'      
      else:
	#if 'property' in text:
	return 'Sorry Not able to classify'
	#print 'Sorry Not able to classify'
    else:
      #print 'Irrelevant text'
      return 'No Relevant conversation'
    #print '##'
  except Exception, e:
    return 'Error Occurred'    
##END CLASSIFY


