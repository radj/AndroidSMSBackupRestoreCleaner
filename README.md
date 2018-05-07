AndroidSMSBackupRestoreCleaner
==============================

This program combines multiple backups created by [SMS Backup &amp; Restore Android app](https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore). This has been tested against Android 4.3 and older version.

Usage can be found by using `python clean.py --help`, which produces this output at the time of writing:
```
$ python clean.py --help
usage: clean.py [-h] [-i infile [infile ...]] [-o outfile]

Combine XML files created with the program SMS Backup and restore.

optional arguments:
  -h, --help            show this help message and exit
  -i infile [infile ...], --input infile [infile ...]
                        the input files to combine
  -o outfile, --output outfile
                        the output file to write
```

[Background story here](http://blog.radj.me/removing-duplicates-sms-backup-restore-xml-android).

Big thanks to [`radj`](https://github.com/radj) for [the original project](https://github.com/radj/AndroidSMSBackupRestoreCleaner) .

# Example Usage

Need to have Python 2.x installed.

## With single file
`python clean.py -i ~/SMSBackupRestore/big_backup.xml -o output_file.xml`

## With directory
`python clean.py -i /path/to/directory -o output_file.xml`

## Multiple inputs
`python clean.py -i backup1.xml backup2.xml backup3.xml -o ~/Backups/output_file.xml`

## Mixed
`python clean.py -i backup1.xml ~/SMSBackupRestore/sms-*.xml -o ~/Backups/output_file.xml`

## With emoji
Emoji needs the `lxml` package. Use `pip install lxml` to install it first, then use as normal.

# Current limitations
* Python 2 only. (For now?)
* ~~No emoji support~~ Now supports emoji! See above.
* No MMS duplicate filtering. It just maintains the MMS entries as is.

# DB info

'''

CREATE TABLE smss(protocol text, address text, date text, type text, subject text, body text, toa text, sc_toa text, service_center text, read text, status text, locked text, date_sent text, readable_date text, contact_name text, primary key (address, date));;

CREATE TABLE mmss(text_only text, ct_t text,
 using_mode text, msg_box text, secret_mode text,
  v text, retr_txt_cs text, ct_cls text, favorite text,
   d_rpt_st text, deletable text, st text, sim_imsi text,
    creator text, tr_id text, sim_slot text,
     read text, m_id text, callback_set text, m_type text, retr_txt text,
      locked text, resp_txt text, rr_st text, safe_message text,
       retr_st text, reserved text, msg_id text, hidden text,
        sub text, rr text, seen text, ct_l text, from_address text,
         m_size text, exp text, sub_cs text, sub_id text, resp_st text,
          date text, app_id text, date_sent text, pri text, address text,
           read_status text, d_tm text, d_rpt text, device_name text,
            spam_report text, rpt_a text, m_cls text, readable_date text,
             contact_name text, network_type text, privacy_mode text,
                  id integer,
                  primary key (address, date));
                  
CREATE TABLE parts(seq text,
ct text,
name text,
chset text,
cd text,
fn text,
cid text,
cl text,
ctt_s text,
ctt_t text,
text text,
data text,
fk_id_mms integer,
primary key (data, text, name));

CREATE TABLE addrs(address text,
type text,
charset text,
fk_id_mms integer,
primary key (fk_id_mms, charset, type, address));

'''