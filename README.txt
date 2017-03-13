This script will help create the monthly newsletters from Kobo. Th explanation to use it is highlighted below.

1) Monthly emails/JIRA tickets will be received containing the HTML files for the newsletter, the email subject names, and the Campaign names.
2) Copy all the HTML files from the email/ticket into the "HTML" folder in the same location as the script
3) Go into the names.txt file and copy paste the Campaign names under the heading "Campaign names"
4) In the same names.txt file, copy and paste the Email subject names under the heading "Email subject names"
5) Open the mailchimp.py file and under the variable testEmail, enter in the TEST emails to send the created newsletters to
6) Go into terminal and change directory to where the mailchimp.py file exists
7) run the command "python mailchimp.py" 
8) If any errors are encountered, it will be displayed in the terminal
9) The campaigns should now be created and available when you log into mailchimp on the web
10) All the test emails mentioned in the script would also receive the newsletters



Shown below is how the names.txt File should look like. notice how the newsletter languages are specified, this is necessary so that the campaign is set to send to the right coutnry mailing list on mailchimp:
Campaign names
Kobo Newsletter - March - (EN)
Kobo Newsletter - March - (ES)
Kobo Newsletter - March - (FR)
Kobo Newsletter - March - (FR CA)
Kobo Newsletter - March - (IT)
Kobo Newsletter - March - (NL)
Kobo Newsletter - March - (TR)

Email subject names
Discover Kobo March 2017 (EN)
Discover Kobo Marzo de 2017 (ES)
Discover Kobo Mars 2017 (FR)
Discover Kobo mars 2017 (QC)
Discover Kobo Marzo 2017 (IT)
Discover Kobo Maart 2017 (NL)
Discover Kobo Mart 2017 (TR)