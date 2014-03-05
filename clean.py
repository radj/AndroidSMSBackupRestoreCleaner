import sqlite3
import xml.etree.ElementTree as XML

conn = sqlite3.connect('sms.db')

####
#
# Parse the XML and filter out duplicates with date and target
# 
####
print "Parsing XML..." ,  
tree = XML.parse('sms.xml')
#tree = XML.parse('sample.xml')
root = tree.getroot()
print "Done."

print "Loading data into DB..." ,
conn.execute('DELETE FROM messages')
for child in root:
	columns = ', '.join(child.attrib.keys())
	placeholders = ', '.join('?' * len(child.attrib))
	sql = 'INSERT INTO messages ({}) VALUES ({})'.format(columns, placeholders)
	try:
		conn.execute(sql, child.attrib.values())
	except sqlite3.IntegrityError:
		pass
print "Done."
conn.commit()


####
#
# Write it back to file
# 
####
print "Rewriting into optimized XML..." ,
newroot = XML.Element("smses")

cursor = conn.execute("SELECT COUNT() FROM messages")
smscount = cursor.fetchone()
newroot.set("count", "%d" % smscount[0])

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
print "Done."


conn.close()