# logagg-fs
[Fuse file system](https://en.wikipedia.org/wiki/Filesystem_in_Userspace)  for`logagg`. Captures logs when it is written to a file and caches them.

## Components/Architecture/Terminology
* **mountpoint**: directory where logs are being written
* **logcache**: data directory for logagg-fs
* **logcache/mirror**: directory which is mounted to the mountpoint directory
* **logcache/logs**: directory where logs are cached
* **logcache/trackfiles.txt**: file where file-patterns to be cached are mentioned
* **mountpoint/.update**: file that is responsible to update the state to logagg-fs if new file pattern is added to `logcache/trackfiles.txt`

## Features
* Guarantees capturing every log line
* Rotation proof
* One time set-up
* Supports file patterns; i.e. `/var/log/syslog*`; rather than fpaths

## Limitations
* No way of getting logs before start-up of the program
* Manual update after any file pattern is added to `logcache/trackfiles.txt`

## Prerequisites
* Expected restart of server after mounting to non-empty directories like /var/log/
* Copy files in mountpoint before mounting if mountpoint not-empty

## Installation
### Dependencies
```bash=
$ sudo apt install libfuse-dev python3-dev python3-pip pkg-config build-essential python3-pip
$ pip3 install setuptools
```

### Install logagg-fs
- **NOTE:** Make sure you are a root user.

#### Root user
```bash=
$ sudo bash
```
#### Clone repository and install it
```bash=
$ git clone https://github.com/supriyopaul/logagg_fs.git
$ cd logagg_fs
$ pip3 install .
```
#### Check installation
```bash=
$ logagg-fs -h
Usage: 
    Logagg Log collection FUSE filesystem

    logagg-fs [mountpoint] [options]

Options:
    --version              show program's version number and exit
    -h, --help             show this help message and exit
    -o opt,[opt...]        mount options
    -o root=PATH           mountpoint
    -o loglevel=DEBUG/INFO
                           level of logger
    -o logfile=PATH        file path to store logs
Usage: 
    Logagg Log collection FUSE filesystem

    logagg-fs [mountpoint] [options]

Options:
    --version              show program's version number and exit
    -h, --help             show this help message and exit
    -o opt,[opt...]        mount options
    -o root=PATH           mountpoint
    -o loglevel=DEBUG/INFO
                           level of logger
    -o logfile=PATH        file path to store logs
```

### Setting up  logagg-fs for mounting /logcache to /var/log
- **NOTE:** Do not stor the log file path of logagg-fs logs to `mountpoint` directory. Here /var/log is `mountpoint`
#### Make a directory where log files are cached
```bash=
$ mkdir /logcache/
```

#### Mount /logcache/mirror to /var/log/ directory using `fstab`
```bash=
$ vim /etc/fstab
# Add the line "/usr/local/bin/logagg-fs /var/log/ fuse rw,user,auto,exec,nonempty,allow_other,root=/logcache/,loglevel=INFO,logfile=/logcache/fuse.log 0 0" to /etc/fstab
```
![image](https://user-images.githubusercontent.com/33823698/45282589-fd569880-b4f8-11e8-99e4-0207d2bbbf9f.png)
#### Setting up logrotate for the log file of logagg-fs (Optional)

Create configuration file of logrotate
```bash
$ vim /etc/logrotate.d/logagg-fs
```
Write the following lines in the file
```
/logcache/fuse.log {
weekly
rotate 3
size 10M
compress
delaycompress
}
```
#### Run & Reboot to load the configuration in /etc/fstab

- **IMPORTANT:** If mountpoint is being used by other programs copy files to a temp directory.
```bash=
$ mkdir ~/temp
$ cp -R /var/log/ ~/temp/
```
Command to mount from fstab file
```bash=
$ mount -a
```
Copy back files if any
```bash=
$ cp -R ~/temp/log /var/
```
Reboot to make changes to take effect
```bash=
$ reboot
```
## Usage
Check if file system is mirrored properly
```bash=
$ ls /var/log/
$ # The same as:
$ ls /logcache/mirror/
```
```bash=
$ cat /logcache/mirror/test
cat: /logcache/mirror/test: No such file or directory
$ echo "testing.." > /var/log/test
$ cat /logcache/mirror/test
testing..
```

Check caching of log files
```bash=
$ ls /logcache/logs/ # No logs yet
$ # Now add the files to be tracked in logcache/trackfiles.txt file
$ echo "/var/log/syslog" >> /logcache/trackfiles.txt
$ # Takes atmost 10sec to update state
$ ls /logcache/logs/ # To see the cached log-files
f5fdf6ea0ea92860c6a6b2b354bfcbbc.1536590719.4519932.log
$ tail -f /logcache/logs/* # The contents of the file are being written simultaneously to cached files
```
* Just remove the file pattern from `/logcache/trackfiles.txt` to stop caching of logs

* To unmount directory
```bash=
$ umount /var/log
```
Or Delete configuration from /etc/fstab
```bash=
$ reboot
```

