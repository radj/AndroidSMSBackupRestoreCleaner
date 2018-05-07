import sqlite3
try:
    from lxml.etree import ETCompatXMLParser
    custom_parser = ETCompatXMLParser(huge_tree=True, recover=True)
except ImportError:
    custom_parser = None

try:
    import xml.etree.cElementTree as XML
except ImportError:
    import xml.etree.ElementTree as XML
import logging as log
from datetime import datetime
import argparse
import glob, fnmatch, os, re

#    TODO SMSCOUNT backup_set backup_date
#

GLOB_ID_MMS = 0


def main(input_paths, output_path):
    try:
        time_start = datetime.now()
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(message)s')
        log.debug('Starting Operation...')
        conn = sqlite3.connect('sms.db')
        conn.execute('DELETE FROM smss')
        conn.execute("DELETE FROM mmss")
        conn.execute("DELETE FROM parts")
        conn.execute("DELETE FROM addrs")
        mms_list = []
        root = XML.Element("smses")

        for xml_filename in input_paths:
            log.debug("Parsing XML file: ")
            tree = XML.parse(xml_filename, parser=custom_parser)
            log.debug("Done.")
            load_into_db(conn, tree)

        add_sms(conn, root)
        add_mms(conn, root)
        conn.close()
        #append_mms(mms_list, root)
        write_file(output_path, root)
        time_end = datetime.now()
        log.debug('Operation completed in %d seconds.' % ((time_end - time_start).total_seconds()))
    finally:
        if 'conn' in locals():
            conn.close()


def write_file(output_path, root):
    tree = XML.ElementTree(root)
    tree.write(output_path, xml_declaration=True, encoding="UTF-8")


def append_mms(mms_list, root):
    log.debug("Adding skipped %d MMS into new XML..." % len(mms_list))
    for mms in mms_list:
        root.extend(mms)


def add_sms(conn, root):
    log.debug("Rewriting into optimized XML...")
    cursor = conn.execute("SELECT COUNT() FROM smss")
    sms_count = cursor.fetchone()
    root.set("count", "%d" % sms_count[0])
    log.debug("Attempting to write new XML for SMS count: " + str(sms_count[0]))
    # Get the rows
    cursor = conn.execute("SELECT * FROM smss ORDER BY date_sent")
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


def add_mms(conn, root):
    log.debug("Rewriting into optimized XML...")
    cursor = conn.execute("SELECT COUNT() FROM mmss")
    mms_count = cursor.fetchone()
    root.set("count", "%d" % mms_count[0])
    log.debug("Attempting to write new XML for MMS count: " + str(mms_count[0]))
    # Get the rows
    cursorMMS = conn.execute("SELECT * FROM mmss ORDER BY date_sent")
    for rowMMS in cursorMMS:
        mms_element = XML.SubElement(root, "mms")
        # retrocompatibility
        mms_element.set("text_only", rowMMS[0])

        mms_element.set("ct_t", rowMMS[1])

        using_mode = rowMMS[2]
        if using_mode is not None:
            mms_element.set("using_mode", using_mode)

        mms_element.set("msg_box", rowMMS[3])

        secret_mode = rowMMS[4]
        if secret_mode is not None:
            mms_element.set("secret_mode", secret_mode)

        mms_element.set("v", rowMMS[5])

        mms_element.set("retr_txt_cs", rowMMS[6])

        mms_element.set("ct_cls", rowMMS[7])

        favorite = rowMMS[8]
        if favorite is not None:
            mms_element.set("favorite", favorite)

        d_rpt_st = rowMMS[9]
        if d_rpt_st is not None:
            mms_element.set("d_rpt_st", d_rpt_st)

        deletable = rowMMS[10]
        if deletable is not None:
            mms_element.set("deletable", deletable)

        mms_element.set("st", rowMMS[11])

        sim_imsi = rowMMS[12]
        if sim_imsi is not None:
            mms_element.set("sim_imsi", sim_imsi)

        creator = rowMMS[13]
        if creator is not None:
            mms_element.set("creator", creator)

        mms_element.set("tr_id", rowMMS[14])

        sim_slot = rowMMS[15]
        if sim_slot is not None:
            mms_element.set("sim_slot", sim_slot)

        mms_element.set("read", rowMMS[16])

        mms_element.set("m_id", rowMMS[17])

        callback_set = rowMMS[18]
        if callback_set is not None:
            mms_element.set("callback_set", callback_set)

        mms_element.set("m_type", rowMMS[19])

        mms_element.set("retr_txt", rowMMS[20])

        mms_element.set("locked", rowMMS[21])

        mms_element.set("resp_txt", rowMMS[22])

        rr_st = rowMMS[23]
        if rr_st is not None:
            mms_element.set("rr_st", rr_st)

        safe_message = rowMMS[24]
        if safe_message is not None:
            mms_element.set("safe_message", safe_message)

        mms_element.set("retr_st", rowMMS[25])

        reserved = rowMMS[26]
        if reserved is not None:
            mms_element.set("reserved", reserved)

        msg_id = rowMMS[27]
        if msg_id is not None:
            mms_element.set("msg_id", msg_id)

        hidden = rowMMS[28]
        if hidden is not None:
            mms_element.set("hidden", hidden)

        mms_element.set("sub", rowMMS[29])
        mms_element.set("rr", rowMMS[30])
        mms_element.set("seen", rowMMS[31])
        mms_element.set("ct_l", rowMMS[32])

        from_address = rowMMS[33]
        if from_address is not None:
            mms_element.set("from_address", from_address)

        mms_element.set("m_size", rowMMS[34])
        mms_element.set("exp", rowMMS[35])
        mms_element.set("sub_cs", rowMMS[36])
        mms_element.set("sub_id", rowMMS[37])
        mms_element.set("resp_st", rowMMS[38])
        mms_element.set("date", rowMMS[39])

        app_id = rowMMS[40]
        if app_id is not None:
            mms_element.set("app_id", app_id)

        mms_element.set("date_sent", rowMMS[41])
        mms_element.set("pri", rowMMS[42])
        mms_element.set("address", rowMMS[43])
        mms_element.set("read_status", rowMMS[44])
        mms_element.set("d_tm", rowMMS[45])
        mms_element.set("d_rpt", rowMMS[46])

        device_name = rowMMS[47]
        if device_name is not None:
            mms_element.set("device_name", device_name)

        spam_report = rowMMS[48]
        if spam_report is not None:
            mms_element.set("spam_report", spam_report)

        mms_element.set("rpt_a", rowMMS[49])
        mms_element.set("m_cls", rowMMS[50])
        mms_element.set("readable_date", rowMMS[51])
        mms_element.set("contact_name", rowMMS[52])
        network_type = rowMMS[53]
        if network_type is not None:
            mms_element.set("network_type", network_type)
        privacy_mode = rowMMS[54]
        if privacy_mode is not None:
            mms_element.set("privacy_mode", privacy_mode)
        # ----- write parts and addrs
        id_mms = rowMMS[55]
        conn2 = sqlite3.connect('sms.db')
        cursorParts = conn2.execute("SELECT * FROM parts WHERE fk_id_mms ="+str(id_mms))
        parts_root = XML.SubElement(mms_element, "parts")
        for rowPart in cursorParts:
            part_element = XML.SubElement(parts_root, "part")
            part_element.set("seq", rowPart[0])
            part_element.set("ct", rowPart[1])
            part_element.set("name", rowPart[2])
            part_element.set("chset", rowPart[3])
            part_element.set("cd", rowPart[4])
            part_element.set("fn", rowPart[5])
            part_element.set("cid", rowPart[6])
            part_element.set("cl", rowPart[7])
            part_element.set("ctt_s", rowPart[8])
            part_element.set("ctt_t", rowPart[9])
            # could be text or data
            text = rowPart[10]
            if text is not None:
                part_element.set("text", text)
            else:
                part_element.set("text", "null")
            data = rowPart[11]
            if data is not None:
                part_element.set("data", data)
            else:
                part_element.set("data", "null")

        cursorAddrs = conn2.execute("SELECT * FROM addrs WHERE fk_id_mms ="+str(id_mms))
        addrs_root = XML.SubElement(mms_element, "addrs")
        for rowAddr in cursorAddrs:
            addr_element = XML.SubElement(addrs_root, "addr")
            addr_element.set("address", rowAddr[0])
            addr_element.set("type", rowAddr[1])
            addr_element.set("charset", rowAddr[2])
        if 'conn2' in locals():
            conn2.close()
    conn.commit()


def insert_default(conn, sql, vals, child):
    try:
        conn.execute(sql, vals)
    except sqlite3.IntegrityError:
        # This is a duplicate error. Skip this sms entry. Filter this nosy dupe out!
        # log.info("Skipping: Found IntegrityError when processing child: " + str(child))
        # log.info("\tException: " + e.message)
        return False
    except sqlite3.OperationalError as e:
        log.info("Skipping: Found OperationalError when processing child (%s): %s" % (child.tag, str(child)))
        log.info("\tException: " + e.message)
        return False
    return True


def insert_sms(conn, child):
    columns = ', '.join(child.attrib.keys())
    placeholders = ', '.join('?' * len(child.attrib))
    sql = 'INSERT INTO smss ({}) VALUES ({})'.format(columns, placeholders)
    vals = child.attrib.values()
    return insert_default(conn, sql, vals, child)


def mms_compatibility(child, columns):
    oppo_counter = columns.count("oppo")
    columns = re.sub('(oppo_[a-z_]+,)', '', columns)
    log.debug("columns %s" % columns)
    placeholder_counter = (len(child.attrib)+1-oppo_counter)
    placeholders = ', '.join('?' * placeholder_counter)
    sql = 'INSERT INTO mmss ({}) VALUES ({})'.format(columns, placeholders)
    return sql

def insert_mms(conn, child):
    columns = 'id ,'+', '.join(child.attrib.keys())
    sql = mms_compatibility(child, columns)
    #id_mms = conn.execute('SELECT IFNULL(MAX(id), 0) + 1 FROM mmss')
    global GLOB_ID_MMS
    id_mms = GLOB_ID_MMS
    vals = child.attrib.values()
    vals.insert(0, id_mms)
    # ---------- PARTS AND ADDRS ---------------
    rst = insert_default(conn, sql, vals, child)

    GLOB_ID_MMS = GLOB_ID_MMS+1
    if rst:
        child_parts = child.find('parts')
        child_addrs = child.find('addrs')
        if child_parts is not None:
            for child_part in child_parts.findall('part'):
                insert_part(conn, id_mms, child_part)
        if child_addrs is not None:
            for child_addr in child_addrs.findall('addr'):
                insert_addr(conn, id_mms, child_addr)
    return id_mms


def insert_part(conn, id_mms, child_mms):
    columns_part = 'fk_id_mms ,'+', '.join(child_mms.attrib.keys())
    placeholders_part = ', '.join('?' * (len(child_mms.attrib)+1))
    sql = 'INSERT INTO parts ({}) VALUES ({})'.format(columns_part, placeholders_part)
    vals = child_mms.attrib.values()
    vals.insert(0, id_mms)
    return insert_default(conn, sql, vals, child_mms)


def insert_addr(conn, id_mms, child_mms):
    columnsAddr = 'fk_id_mms ,'+', '.join(child_mms.attrib.keys())
    placeholdersAddr = ', '.join('?' * (len(child_mms.attrib)+1))
    sql = 'INSERT INTO addrs ({}) VALUES ({})'.format(columnsAddr, placeholdersAddr)
    vals = child_mms.attrib.values()
    vals.insert(0, id_mms)
    return insert_default(conn, sql, vals, child_mms)


def load_into_db(conn, tree):
    root = tree.getroot()
    log.debug("Loading MMS data into DB...")
    num_skipped = 0
    mms_list = []
    for child in root:
        rst = False
        if child.tag == "mms":
            rst = insert_mms(conn, child)
        elif child.tag == "sms":
            rst = insert_sms(conn, child)
        if not rst:
            num_skipped += 1

    root.clear()  # Clear this super huge tree. We don't need it anymore
    log.debug("Done duplicate check. Skipped duplicate entries: " + str(num_skipped))
    conn.commit()
    return mms_list


def parse_args():
    parser = argparse.ArgumentParser(description='Combine XML files created with the program SMS Backup and restore.')
    parser.add_argument('-i', '--input', metavar='infile', type=str, nargs='+',
                        help='the input files to combine')
    parser.add_argument('-o', '--output', metavar='outfile', type=str, nargs=1,
                        help='the output file to write')

    args = parser.parse_args()

    input_path = set()

    for current_path in args.input:
        temp_path = os.path.abspath(os.path.expandvars(os.path.expanduser(current_path)))

        if os.path.isdir(temp_path):
            unfiltered_list = [os.path.normpath(os.path.join(temp_path, x)) for x in os.listdir(temp_path)]
        else:
            unfiltered_list = glob.glob(temp_path)

        filtered_list = fnmatch.filter(unfiltered_list, "*.xml")
        input_path.update(filtered_list)

    return input_path, os.path.abspath(os.path.expandvars(os.path.expanduser(args.output[0])))


if __name__ == "__main__":
    (input_paths, output_paths) = parse_args()
    main(input_paths, output_paths)
