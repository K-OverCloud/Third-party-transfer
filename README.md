# Third-party-transfer

## Overview ##
Third party transfer solutions for high-speed transmission links DTN (KISTI)


## Requirements
* Python
* Flask:A Python Microframework
* MySQL
* pipenv
* Cent 7 
* cURL
* GridFTP


## Install 

Mysql install 
(Option) If you have MySQL, Skip following commands

```
$ sudo yum install mysql
$ sudo systemctl start mysqld
```
mysql: create database & user
```
$ mysql -u root
mysql> create database test;
mysql> use test;
mysql> GRANT ALL ON *.* To '계정명'@'localhost' IDENTIFIED BY '패스워드';
```

mysql: create table
```
mysql> 
CREATE TABLE `tbl_dtn` (
  `Id` int(11) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `Ip` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `testlog2` (
  `no` int(11) NOT NULL AUTO_INCREMENT,
  `Date` datetime DEFAULT NULL,
  `Source` varchar(100) DEFAULT NULL,
  `Destination` varchar(100) DEFAULT NULL,
  `File` varchar(100) DEFAULT NULL,
  `MBperSec` float DEFAULT NULL,
  `MB` float DEFAULT NULL,
  `Time_sec` float DEFAULT NULL,
  PRIMARY KEY (`no`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
```
GridFTP install
(Option) If you have GridFTP, Skip following commands
```
$ sudo curl -LOs https://downloads.globus.org/toolkit/globus-connect-server/globus-connect-server-repo-latest.noarch.rpm
$ sudo yum install globus-connect-server-repo-latest.noarch.rpm
$ sudo curl -LOs https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
$ sudo yum install epel-release-latest-7.noarch.rpm
$ sudo yum install yum-plugin-priorities
$ sudo yum install globus-connect-server
```

GridFTP setting
```
$ sudo vi /etc/gridftp.conf
allow_anonymous 1
anonymous_user root
$ sudo systemctl restart globus-gridftp-server
```

Flask and mysql-connector-python install 
```
$ sudo yum install epel-release
$ sudo yum install python-pip
$ sudo pip install Flask
$ sudo pip install mysql-connector-python
```

## Running
To run Third party transfer server, run following commands

```
$ git clone https://github.com/K-OverCloud/Third-party-transfer-KISTI
$ cd Third-party-transfer-KISTI
$ python gridftp_3rd_party_server.py
```
in gridftp_3rd_party_server.py line 5, 
change mysql login info ( ID & PW ),
```
$ python gridftp_3rd_party_server.py
```

DTN information search, change 127.0.0.1 to your server IP
```
$ curl -H "Content-Type: application/json" -X GET 127.0.0.1:22641/info
```

Transmission log search, change 127.0.0.1 to your server IP
```
$ curl -H "Content-Type: application/json" -X GET 127.0.0.1:22641/info
```

Directory search command, change SourceIP, DestIP, ServerIP to yours
```
$ curl -H "Content-Type: application/json" -X GET -d '{"Source":"SourceIP:2811/export/","Dest":"DestIP:2811/export/"}' ServerIP:22641/transfer
```

Transmission command, change SourceIP, DestIP, ServerIP to yours
```
$ curl -H "Content-Type: application/json" -X POST -d '{"Source":"SourceIP:2811/export/10GB","Dest":"DestIP:2811/export/10GB"}' ServerIP:22641/transfer
```
