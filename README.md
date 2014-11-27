AndroidSMSBackupRestoreCleaner
==============================

This cleans up duplicate SMS entries in a backup created by [SMS Backup &amp; Restore Android app](https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore). This has been tested against Android 4.3 and older version.

To use, simply put the SMS B&amp;R output file (overwrite the existing sms.xml file) and run python clean.py. A duplicate-free sms-clean.xml will be created.

Background story [here](http://blog.radj.me/removing-duplicates-sms-backup-restore-xml-android).

Usage 
=====

Need to have Python installed and all the files in one folder.

* `cd path/to/folder/`
* `python clean.py`

Current limitations
===================
* No emoji support
* No MMS support
