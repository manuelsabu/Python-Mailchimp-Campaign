# -*- coding: utf-8 -*-
from mailchimp3 import MailChimp
from os import listdir
from os.path import isfile, join
import json, urllib, base64, urllib2, time, codecs, os, time, re, codecs


# DECLARATIONS
username = "''"
# You can find your Api Token on Mail chimp under Profile Name --> Profile --> Extras --> API Keys
apiToken = ''
# Secify API URL to connect to (look in your browser's url when you log into mailchimp)
apiURL = 'https://us8.api.mailchimp.com/3.0'
# Email from Name
fromName = "From Name"
# Email from email
fromEmail = "from@email.com"
# Email addresses to send test Email to
testEmails = ['test@email.com', 'test2@email.com']
# Regex patterns and associated start and end indices for language portion or pattern
# Email subject must contain something like (EN) to specify language
emailSubjectPattern = {"pattern": r"\([A-Z][A-Z]\)", "start":1, "end": 3}
# Email campaign must contain something like (EN) to specify language
campaignNamePattern1 = {"pattern": r"\([A-Z][A-Z]\)", "start":1, "end": 3}
# Special campaign pattern to match something like (FR CA) for quebec
campaignNamePattern2 = {"pattern": r"\([A-Z][A-Z] [A-Z][A-Z]\)", "start":1, "end": 6}
# Pattern to find language in the file name, something like _EN.html
fileNamePattern = {"pattern": r"\_[A-Z][A-Z]\.html", "start":1, "end": 3}


# In this case, we are always making individual campaigns for different mailing groups which are
# grouped based on language, and each have their own footer content to append to the campaign html content files
Languages = {"EN": {"listId": "5b490e612b", "names": "Undefined Campaign Name" ,"subject": "Undefined Subject Name" ,"footer": '<center> <br> <br> <br> <br> <br> <br> <table border="0" cellpadding="0" cellspacing="0" width="100%" id="canspamBarWrapper" style="background-color:#FFFFFF; border-top:1px solid #E5E5E5;"> <tr> <td align="center" valign="top" style="padding-top:20px; padding-bottom:20px;"> <table border="0" cellpadding="0" cellspacing="0" id="canspamBar"> <tr> <td align="center" valign="top" style="color:#606060; font-family:Helvetica, Arial, sans-serif; font-size:11px; line-height:150%; padding-right:20px; padding-bottom:5px; padding-left:20px; text-align:center;"> You have signed up to recieve emails from Kobo at <a href="mailto:*|EMAIL|*" target="_blank" style="color:#404040 !important;">*|EMAIL|*</a> - <a href="*|UNSUB|*" style="color:#404040 !important;">Click here to unsubscribe</a> <br>   *|LIST:ADDRESSLINE|* <br> <br> </td> </tr> </table> </td> </tr> </table> <style type="text/css"> @media only screen and (max-width: 480px){ table[id="canspamBar"] td{font-size:14px !important;} table[id="canspamBar"] td a{display:block !important; margin-top:10px !important;} } </style> </center>'}, 
"FR": {"listId": "f5bac6fdfb", "names": "Undefined Campaign Name" ,"subject": "Undefined Subject Name" ,"footer": '<center> <br> <br> <br> <br> <br> <br> <table border="0" cellpadding="0" cellspacing="0" width="100%" id="canspamBarWrapper" style="background-color:#FFFFFF; border-top:1px solid #E5E5E5;"> <tr> <td align="center" valign="top" style="padding-top:20px; padding-bottom:20px;"> <table border="0" cellpadding="0" cellspacing="0" id="canspamBar"> <tr> <td align="center" valign="top" style="color:#606060; font-family:Helvetica, Arial, sans-serif; font-size:11px; line-height:150%; padding-right:20px; padding-bottom:5px; padding-left:20px; text-align:center;"> Vous vous êtes inscrit pour recevoir un courriel de Kobo sur <a href="mailto:*|EMAIL|*" target="_blank" style="color:#404040 !important;">*|EMAIL|*</a> - <a href="*|UNSUB|*" style="color:#404040 !important;">Cliquez ici pour vous désabonner</a> <br>   *|LIST:ADDRESSLINE|* <br> <br> </td> </tr> </table> </td> </tr> </table> <style type="text/css"> @media only screen and (max-width: 480px){ table[id="canspamBar"] td{font-size:14px !important;} table[id="canspamBar"] td a{display:block !important; margin-top:10px !important;} } </style> </center>'}, 
"TR": {"listId": "ab5a002d81", "names": "Undefined Campaign Name" ,"subject": "Undefined Subject Name" ,"footer": '<center> <br> <br> <br> <br> <br> <br> <table border="0" cellpadding="0" cellspacing="0" width="100%" id="canspamBarWrapper" style="background-color:#FFFFFF; border-top:1px solid #E5E5E5;"> <tr> <td align="center" valign="top" style="padding-top:20px; padding-bottom:20px;"> <table border="0" cellpadding="0" cellspacing="0" id="canspamBar"> <tr> <td align="center" valign="top" style="color:#606060; font-family:Helvetica, Arial, sans-serif; font-size:11px; line-height:150%; padding-right:20px; padding-bottom:5px; padding-left:20px; text-align:center;"> Sen <a href="mailto:*|EMAIL|*" target="_blank" style="color:#404040 !important;">*|EMAIL|*</a> için Kobo e-posta almak için imzaladı - <a href="*|UNSUB|*" style="color:#404040 !important;">üyelikten çıkmak için buraya tıklayın</a> <br>   *|LIST:ADDRESSLINE|* <br> <br> </td> </tr> </table> </td> </tr> </table> <style type="text/css"> @media only screen and (max-width: 480px){ table[id="canspamBar"] td{font-size:14px !important;} table[id="canspamBar"] td a{display:block !important; margin-top:10px !important;} } </style> </center>'}, 
"ES": {"listId": "d3ebcc1806", "names": "Undefined Campaign Name" ,"subject": "Undefined Subject Name" ,"footer": '<center> <br> <br> <br> <br> <br> <br> <table border="0" cellpadding="0" cellspacing="0" width="100%" id="canspamBarWrapper" style="background-color:#FFFFFF; border-top:1px solid #E5E5E5;"> <tr> <td align="center" valign="top" style="padding-top:20px; padding-bottom:20px;"> <table border="0" cellpadding="0" cellspacing="0" id="canspamBar"> <tr> <td align="center" valign="top" style="color:#606060; font-family:Helvetica, Arial, sans-serif; font-size:11px; line-height:150%; padding-right:20px; padding-bottom:5px; padding-left:20px; text-align:center;"> Usted se suscribió para recibir correo electrónico de Kobo a <a href="mailto:*|EMAIL|*" target="_blank" style="color:#404040 !important;">*|EMAIL|*</a> - <a href="*|UNSUB|*" style="color:#404040 !important;">Haga clic aquí para cancelar su suscripción</a> <br>   *|LIST:ADDRESSLINE|* <br> <br> </td> </tr> </table> </td> </tr> </table> <style type="text/css"> @media only screen and (max-width: 480px){ table[id="canspamBar"] td{font-size:14px !important;} table[id="canspamBar"] td a{display:block !important; margin-top:10px !important;} } </style> </center>'}, 
"NL": {"listId": "e37a0e6b72", "names": "Undefined Campaign Name" ,"subject": "Undefined Subject Name" ,"footer": '<center> <br> <br> <br> <br> <br> <br> <table border="0" cellpadding="0" cellspacing="0" width="100%" id="canspamBarWrapper" style="background-color:#FFFFFF; border-top:1px solid #E5E5E5;"> <tr> <td align="center" valign="top" style="padding-top:20px; padding-bottom:20px;"> <table border="0" cellpadding="0" cellspacing="0" id="canspamBar"> <tr> <td align="center" valign="top" style="color:#606060; font-family:Helvetica, Arial, sans-serif; font-size:11px; line-height:150%; padding-right:20px; padding-bottom:5px; padding-left:20px; text-align:center;"> Je hebt je aangemeld voor e-mails van Kobo op <a href="mailto:*|EMAIL|*" target="_blank" style="color:#404040 !important;">*|EMAIL|*</a> - <a href="*|UNSUB|*" style="color:#404040 !important;">Klik hier om je weer af te melden</a> <br>   *|LIST:ADDRESSLINE|* <br> <br> </td> </tr> </table> </td> </tr> </table> <style type="text/css"> @media only screen and (max-width: 480px){ table[id="canspamBar"] td{font-size:14px !important;} table[id="canspamBar"] td a{display:block !important; margin-top:10px !important;} } </style> </center>'}, 
"IT": {"listId": "1f674899bb", "names": "Undefined Campaign Name" ,"subject": "Undefined Subject Name" ,"footer": '<center> <br> <br> <br> <br> <br> <br> <table border="0" cellpadding="0" cellspacing="0" width="100%" id="canspamBarWrapper" style="background-color:#FFFFFF; border-top:1px solid #E5E5E5;"> <tr> <td align="center" valign="top" style="padding-top:20px; padding-bottom:20px;"> <table border="0" cellpadding="0" cellspacing="0" id="canspamBar"> <tr> <td align="center" valign="top" style="color:#606060; font-family:Helvetica, Arial, sans-serif; font-size:11px; line-height:150%; padding-right:20px; padding-bottom:5px; padding-left:20px; text-align:center;"> Ti sei registrato per la ricezione di email Kobo all’indirizzo <a href="mailto:*|EMAIL|*" target="_blank" style="color:#404040 !important;">*|EMAIL|*</a> - <a href="*|UNSUB|*" style="color:#404040 !important;">Clicca qui per annullare la registrazione</a> <br>   *|LIST:ADDRESSLINE|* <br> <br> </td> </tr> </table> </td> </tr> </table> <style type="text/css"> @media only screen and (max-width: 480px){ table[id="canspamBar"] td{font-size:14px !important;} table[id="canspamBar"] td a{display:block !important; margin-top:10px !important;} } </style> </center>'}, 
"QC": {"listId": "41fecfbdcc", "names": "Undefined Campaign Name" ,"subject": "Undefined Subject Name" ,"footer": '<center> <br> <br> <br> <br> <br> <br> <table border="0" cellpadding="0" cellspacing="0" width="100%" id="canspamBarWrapper" style="background-color:#FFFFFF; border-top:1px solid #E5E5E5;"> <tr> <td align="center" valign="top" style="padding-top:20px; padding-bottom:20px;"> <table border="0" cellpadding="0" cellspacing="0" id="canspamBar"> <tr> <td align="center" valign="top" style="color:#606060; font-family:Helvetica, Arial, sans-serif; font-size:11px; line-height:150%; padding-right:20px; padding-bottom:5px; padding-left:20px; text-align:center;"> Vous vous êtes inscrit pour recevoir un courriel de Kobo sur <a href="mailto:*|EMAIL|*" target="_blank" style="color:#404040 !important;">*|EMAIL|*</a> - <a href="*|UNSUB|*" style="color:#404040 !important;">Cliquez ici pour vous désabonner</a> <br>   *|LIST:ADDRESSLINE|* <br> <br> </td> </tr> </table> </td> </tr> </table> <style type="text/css"> @media only screen and (max-width: 480px){ table[id="canspamBar"] td{font-size:14px !important;} table[id="canspamBar"] td a{display:block !important; margin-top:10px !important;} } </style> </center>'}}

# MAILCHIMP CONFIG
chimpConfig = {
    "headers" : { #configure the http request headers that will be sent to the MailChimp API
    "content-type": "application/json", "Authorization": "Basic " + base64.encodestring(str(username + ':' + apiToken)).replace('\n', '')
    },
    "url": apiURL + '/campaigns',
}


def createCampaign(filename, lang):	
	# HOW TO CREATE A NEW CAMPAIGN
	chimpConfig["url"] = apiURL + '/campaigns'
	#encode data into string (json lib would probably make this easier)
	datas = json.dumps({"recipients":{"list_id":Languages[lang]["listId"]},
		"type":"regular",
		"settings":{"subject_line":"NOT CREATED","title":Languages[lang]["names"], "reply_to":fromEmail,"from_name":fromName, "auto_footer":False}})
        
	#build and execute request
	request = urllib2.Request(chimpConfig["url"], datas, chimpConfig["headers"])
	result1 = urllib2.urlopen(request)
	campaignId = json.loads(result1.read())['id']
	print "Create Campaign: ", Languages[lang]["names"]

	# HOW TO EDIT A CAMPAIGN
	#edit the subject line
	chimpConfig["url"] = apiURL + '/campaigns/' + campaignId
	subject_line = "\"" + Languages[lang]["subject"] + "\""
	datas = json.dumps({"settings": {"subject_line": subject_line}})
	req2 = urllib2.Request(chimpConfig["url"], datas, chimpConfig["headers"])
	req2.get_method = lambda : 'PATCH'
	result2 = urllib2.urlopen(req2)
	print "Created Campaign Email with subject line: ", subject_line


	# HOW TO INSERT NEW HTML CONTENT INTO CAMPAIGN CONTENT
	html_file=codecs.open(htmlDir + '/' + filename, 'r')
	html = str(html_file.read())
	#insert footer after the last </table> element in the document
	pos = html.rfind("</table>")
	html = html[:pos+8] + Languages[lang]["footer"] + html[pos+9:]

	chimpConfig["url"] = apiURL + "/campaigns/"+ campaignId + "/content"
	datas = json.dumps({"html": html})
	req4 = urllib2.Request(chimpConfig["url"], datas, chimpConfig["headers"])
	req4.get_method = lambda : 'PUT'
	result4 = urllib2.urlopen(req4)
	print "Inserted html content into email"


	# SENDING TEST EMAIL
	chimpConfig["url"] = apiURL + "/campaigns/"+ campaignId + "/actions/test"
	datas = json.dumps({"test_emails": testEmails, "send_type": "html"})
	req5 = urllib2.Request(chimpConfig["url"], datas, chimpConfig["headers"])
	req5.get_method = lambda : 'POST'
	result5 = urllib2.urlopen(req5)
	print "Test Emails sent to: ", testEmails, "\n"


##----------------------- Script Begins ---------------------------------##

# Look for a folder named HTML containing all the html files
htmlDir = os.path.join(os.path.dirname(__file__), 'HTML')
# List all the files in the HTML Folder
htmlFiles = [f for f in listdir(htmlDir) if isfile(join(htmlDir, f))]

# Looking for Email Subject names and Campaign names in a separate file
# and associating it to the right language in the dictionary
with codecs.open('names.txt') as f:
	key = "names"

	for line in f:
		line = line.decode('utf-8').strip()
		if 'email subject names' in line.lower():
			key = 'subject'
			continue

		elif 'campaign names' in line.lower():
			key = 'names'
			continue

		if key == "names":
			lang = re.findall(campaignNamePattern1['pattern'], line)
			if lang :
				Languages[lang[0][campaignNamePattern1['start']:campaignNamePattern1['end']]][key] = line
			# Special case for quebec newsletter	
			lang = re.findall(campaignNamePattern2['pattern'],line)
			if lang and lang[0][campaignNamePattern2['start']:campaignNamePattern2['end']] == 'FR CA':
				Languages["QC"][key] = line

		elif key == "subject":
			lang = re.findall(emailSubjectPattern['pattern'],line)
			if lang:
				line = line.replace(lang[0], '').strip()
				Languages[lang[0][emailSubjectPattern['start']:emailSubjectPattern['end']]][key] = line
			else:
				print("Subject language in line: '", line, "' must be of the format '(EN)'")

# Create a capaign for each html file in the HTML directory
for file in htmlFiles:
	if(file.endswith('.html')):
		# Look to make sure that the language is specified in the html filename in the format '_EN.html'
		lang = re.findall(fileNamePattern['pattern'],file)
		if lang and (lang[0][fileNamePattern['start']: fileNamePattern['end']] in Languages):
			lang = lang[0][fileNamePattern['start']: fileNamePattern['end']]
			createCampaign(file, lang)
		else:
			print ("File: '", file, "' must specify language in the format '****_EN.html'")


