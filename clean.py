import sqlite3
import xml.etree.ElementTree as XML
import logging as log
from datetime import datetime

time_start = datetime.now()
log.basicConfig(level=log.DEBUG, format='%(asctime)s %(message)s')
log.debug('Starting Operation...')

conn = sqlite3.connect('sms.db')

####
#
# Parse the XML and filter out duplicates with date and target
# 
####
log.debug("Parsing XML...")  
tree = XML.parse('sms.xml')
root = tree.getroot()
log.debug("Done.")

log.debug("Loading data into DB...")
conn.execute('DELETE FROM messages')
num_skipped = 0
for child in root:
	if child.tag == "mms":
		log.debug("Skipping MMS element %s" % str(child))
		num_skipped += 1
		continue

	columns = ', '.join(child.attrib.keys())
	placeholders = ', '.join('?' * len(child.attrib))
	sql = 'INSERT INTO messages ({}) VALUES ({})'.format(columns, placeholders)

	try:
		conn.execute(sql, child.attrib.values())
	except sqlite3.IntegrityError as e:
		# This is a duplicate error. Skip this sms entry. Filter this nosy dupe out!
		#log.info("Skipping: Found IntegrityError when processing child: " + str(child))
		#log.info("\tException: " + e.message)
		num_skipped += 1
		pass
	except sqlite3.OperationalError as e:
		log.info("Skipping: Found OperationalError when processing child (%s): %s" % (child.tag, str(child)))
		log.info("\tException: " + e.message)
		num_skipped += 1
		pass

log.debug("Done. Skipped entries: " + str(num_skipped))
conn.commit()


####
#
# Write it back to file
# 
####
log.debug("Rewriting into optimized XML...")
newroot = XML.Element("smses")

cursor = conn.execute("SELECT COUNT() FROM messages")
smscount = cursor.fetchone()
newroot.set("count", "%d" % smscount[0])
log.debug("Attempting to write new XML for SMS count: " + str(smscount[0]))

# Get the rows
cursor = conn.execute("SELECT * FROM messages")
for row in cursor:
	#newfile.write("<sms protocol=\"%s\" body=\"%s\"/>\n" % (row[0], row[5]))
	smsElement = XML.SubElement(newroot, "sms")
	smsElement.set("protocol", row[0])
	smsElement.set("address", row[1])
	smsElement.set("date", row[2])
	smsElement.set("type", row[3])
	smsElement.set("subject", row[4])
	smsElement.set("body", row[5])
	smsElement.set("toa", row[6])
	smsElement.set("sc_toa", row[7])
	smsElement.set("service_center", row[8])
	smsElement.set("read", row[9])
	smsElement.set("status", row[10])
	smsElement.set("locked", row[11])
	smsElement.set("date_sent", row[12])
	smsElement.set("readable_date", row[13])
	smsElement.set("contact_name", row[14])

newtree = XML.ElementTree(newroot)
newtree.write("sms-new.xml")
time_end = datetime.now()
log.debug('Operation completed in %d seconds.' % ((time_end - time_start).total_seconds()))

conn.close()