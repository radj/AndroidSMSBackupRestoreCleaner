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
