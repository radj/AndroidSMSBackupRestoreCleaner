import sqlite3

try:
    import xml.etree.cElementTree as XML
except ImportError:
    import xml.etree.ElementTree as XML
import logging as log
from datetime import datetime
import argparse
import glob, fnmatch, os


def main(xml_filenames, output_filename):
    try:
        time_start = datetime.now()
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(message)s')
        log.debug('Starting Operation...')
        conn = sqlite3.connect('sms.db')
        conn.execute('DELETE FROM messages')
        mms_list = []
        root = XML.Element("smses")

        for xml_filename in xml_filenames:
            log.debug("Parsing XML file: ")
            tree = XML.parse(xml_filename)
            log.debug("Done.")
            mms_list = mms_list + load_into_db(conn, tree)

        add_sms(conn, root)
        conn.close()
        append_mms(mms_list, root)
        write_file(output_filename, root)
        time_end = datetime.now()
        log.debug('Operation completed in %d seconds.' % ((time_end - time_start).total_seconds()))
    finally:
        if 'conn' in locals():
            conn.close()


def write_file(output_filename, root):
    tree = XML.ElementTree(root)
    tree.write(output_filename, xml_declaration=True, encoding="UTF-8")


def append_mms(mms_list, root):
    log.debug("Adding skipped %d MMS into new XML..." % len(mms_list))
    for mms in mms_list:
        root.append(mms)


def add_sms(conn, root):
    log.debug("Rewriting into optimized XML...")
    cursor = conn.execute("SELECT COUNT() FROM messages")
    sms_count = cursor.fetchone()
    root.set("count", "%d" % sms_count[0])
    log.debug("Attempting to write new XML for SMS count: " + str(sms_count[0]))
    # Get the rows
    cursor = conn.execute("SELECT * FROM messages")
    for row in cursor:
        # newfile.write("<sms protocol=\"%s\" body=\"%s\"/>\n" % (row[0], row[5]))
        sms_element = XML.SubElement(root, "sms")
        sms_element.set("protocol", row[0])
        sms_element.set("address", row[1])
        sms_element.set("date", row[2])
        sms_element.set("type", row[3])
        sms_element.set("subject", row[4])
        sms_element.set("body", row[5])
        sms_element.set("toa", row[6])
        sms_element.set("sc_toa", row[7])
        sms_element.set("service_center", row[8])
        sms_element.set("read", row[9])
        sms_element.set("status", row[10])
        sms_element.set("locked", row[11])
        sms_element.set("date_sent", row[12])
        sms_element.set("readable_date", row[13])
        sms_element.set("contact_name", row[14])
    conn.commit()


def load_into_db(conn, tree):
    root = tree.getroot()
    log.debug("Loading MMS data into DB...")
    num_skipped = 0
    mms_list = []
    for child in root:
        if child.tag == "mms":
            log.debug("Skipping MMS element %s" % str(child))
            mms_list.append(child)
            num_skipped += 1
            continue

        columns = ', '.join(child.attrib.keys())
        placeholders = ', '.join('?' * len(child.attrib))
        sql = 'INSERT INTO messages ({}) VALUES ({})'.format(columns, placeholders)

        try:
            conn.execute(sql, child.attrib.values())
        except sqlite3.IntegrityError:
            # This is a duplicate error. Skip this sms entry. Filter this nosy dupe out!
            # log.info("Skipping: Found IntegrityError when processing child: " + str(child))
            # log.info("\tException: " + e.message)
            num_skipped += 1
            pass
        except sqlite3.OperationalError as e:
            log.info("Skipping: Found OperationalError when processing child (%s): %s" % (child.tag, str(child)))
            log.info("\tException: " + e.message)
            num_skipped += 1
            pass
    root.clear()  # Clear this super huge tree. We don't need it anymore
    log.debug("Done skipping MMS. Skipped entries: " + str(num_skipped))
    conn.commit()
    return mms_list


def parse_args():
    parser = argparse.ArgumentParser(description='Combine XML files created with the program SMS Backup and restore.')
    parser.add_argument('-i', '--input', metavar='infile', type=str, nargs='+',
                        help='the input files to combine')
    parser.add_argument('-o', '--output', metavar='outfile', type=str, nargs=1,
                        help='the output file to write')

    args = parser.parse_args()

    input_files = []

    for current_path in args.input:
        temp_path = os.path.abspath(os.path.expandvars(os.path.expanduser(current_path)))
        unfiltered_list1 = glob.glob(temp_path)

        try:
            unfiltered_list2 = [os.path.normpath(os.path.join(temp_path, x)) for x in os.listdir(temp_path)]
        except OSError:
            unfiltered_list2 = []

        unfiltered_list = list(set(unfiltered_list1) | set(unfiltered_list2))
        filtered_list = fnmatch.filter(unfiltered_list, "*.xml")
        input_files = input_files + filtered_list

    return input_files, args.output


if __name__ == "__main__":
    (xml_filenames, output_filename) = parse_args()
    main(xml_filenames, output_filename)
