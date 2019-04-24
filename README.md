Oracle Database role
====================
[![License](https://img.shields.io/badge/license-Apache-green.svg?style=flat)](https://raw.githubusercontent.com/lean-delivery/ansible-role-oracle-db/master/LICENSE)
[![Build Status](https://travis-ci.org/lean-delivery/ansible-role-oracle-db.svg?branch=master)](https://travis-ci.org/lean-delivery/ansible-role-oracle-db)
[![Build Status](https://gitlab.com/lean-delivery/ansible-role-oracle-db/badges/master/build.svg)](https://gitlab.com/lean-delivery/ansible-role-oracle-db/pipelines)
[![Galaxy](https://img.shields.io/badge/galaxy-lean__delivery.oracle__db-blue.svg)](https://galaxy.ansible.com/lean_delivery/oracle_db)
![Ansible](https://img.shields.io/ansible/role/d/35592.svg)
![Ansible](https://img.shields.io/badge/dynamic/json.svg?label=min_ansible_version&url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv1%2Froles%2F35592%2F&query=$.min_ansible_version)

Summary
-------

This role installs and configures oracle database (Oracle RDBMS 11g2 & Oracle RDBMS 12c & Oracle 11g2 XE) and all associated software/configurations for this (packages, limits, swap size and etc).

Requirements
------------

  - Minimal Version of the ansible for installation: 2.5.
  - Prepared ansible inventory file with listed VMs with python. These machines should be accessible via SSH.
  - Supported Centos 7.* Oracle 12c
  - Supported Centos 6.* Oracle 11g
  - [Official Oracle 12 database support distribution](https://docs.oracle.com/database/121/LADBI/pre_install.htm#LADBI7532)
  - **SELinux**

    No problems in role with active SELinux were encountered. In a case of any issues you should [disable SELinux Temporarily or Permanently](https://www.tecmint.com/disable-selinux-temporarily-permanently-in-centos-rhel-fedora/).

About Oracle Database Express Edition (XE)
------------------------------------------

It is a free-to-use entry-level version of Oracle Database available for a number of platforms. It provides a subset of EE functionality (not including features such as managed backup and recovery, high availability and replication), is community-supported and comes with its own license terms. XE imposes the following restrictions : maximum of 1 CPU, 1 GB of RAM and 11 GB of user data for 11g.

About Enterprise Manager Express
--------------------------------

According to Oracle, Enterprise Manager Database Control is no longer available in Oracle Database 12c. You can use Enterprise Manager Cloud Control 12c or the EM Express 12c to manage Oracle Database 12c databases.

EM Express is an built-in component and requires no seperate installation or license.
Think of it as a light-weight or limited version of Enterprise Manager Cloud Control.
It can be accessed via url:

  `https://hostname:portnumber/em/`

Where hostname is the name or IP of the Oracle database server, portnumber is the port
EM Express is running on. To get portnumber, run below query:

  SQL> SELECT DBMS_XDB_CONFIG.GETHTTPSPORT() FROM DUAL;

Usually, portnumber is 5500.

See more about EM Express in below links:

[Getting Started with Oracle Enterprise Manager Express](http://www.oracle.com/webfolder/technetwork/tutorials/obe/db/12c/r1/2day_dba/12cr1db_ch3emexp/12cr1db_ch3emexp.html)

[Introduction to Oracle Enterprise Manager Database Express](https://docs.oracle.com/database/121/ADMQS/GUID-BA75AD46-D22E-4914-A31E-C395CD6A2BBA.htm#ADMQS031)

Important note!
--------------

Role use next mechanism for identify a swap file size:

- If RAM on your server > 10 GB swap file will be = 16 GB.
- If RAM < 10 GB but  > 2 GB, so swap file will be = RAM x 1.5 GB.
- When RAM < 2GB your swap file will be 8 GB.

Default place for swap file is root directory / .

If you want change size you swap file, please use variable `oracle_db_swap_count` in your playbook.


Role Variables
--------------

  - `oracle_version` - major number of Oracle Database version   
     *default*: `12`
  - `patch_version` - number of Oracle Database version with patch   
     *default*: `12.1.0.2`
  - `transport` - artifact source transport. Use  **web**, **local** for more predictable result   
    *default*: `web`
  Available:
    - `web` Fetching artifact from custom web uri
    - `local` Local artifact
  - `transport_web` - URI for http/https artifact e.g   
    *default*: `http://my-storage.example.com`
  - `transport_local` - path for local artifact   
    *default*: `/tmp`
  - `oracle_images` - list of Oracle Database files   
    default*:
      - ` - linuxamd64_12102_database_1of2.zip`
      - ` - linuxamd64_12102_database_2of2.zip`
  - `oracle_base` - oracle base installation directory   
    *default*: `/opt/oracledb`
  - `unqname` - database unique name   
    *default*: `orcl`
  - `sid` - instance unique identifier   
    *default*: `orcl`
  - `db_user` - database user   
    *default*: `oracle`
  - `db_tablespace` - mandatory tablespace of the data dictionary   
    *default*: `oracle`
  - `db_port` - database port   
    *default*: `1521`
  - `oracle_db_swap_count` - swap file size   
    *default*: role identify a swap file size
  - `oracle_db_swapfile` - path to swap file   
    *default* `/oracle-swapfile`
  - `db_startup_timeout` - startup timeout for systemd service   
    *default* `300`

  - **For Oracle Universal Installer**
    - `inventory_directory` *default* `/opt/oraInventory`
    - `ora_inst` *default*`/etc/oraInst.loc`

  - **Password for administrative accounts**

    All databases include the SYS, SYSTEM, SYSMAN and DBSNMP administrative
    accounts. To protect these accounts from unauthorized access, their
    passwords must be changed according Oracle password policy.

    - `syspass` - password for all database users
    - `syspassword` - SYS password
    - `systempassword` - SYSTEM password
    - `sysmanpassword` - SYSMAN password
    - `dbsnmppassword` - DBSNMP password
    - `db_user_password` - initial user password
    - `pdbadminpassword` - if a multitenant DB with one or more pluggable DBs is created

  - **Default password for administrative accounts Oracle 11, XE versions**
    ```yaml
    syspass: SysPassOracle2017SecretToken
    syspassword: SysPassword2017SecretToken
    systempassword: SystemPassword2017SecretToken
    sysmanpassword: SysmanPassword2017SecretToken
    dbsnmppassword: DbSnmpPassword2017SecretToken
    db_user_password: DbPassword2017SecretToken (for created DB schema)
    ```

  - **Default password for administrative accounts Oracle 12 version**
    ```yaml
    syspass: SysPassOracle2017SecretToken
    syspassword: SysPassword2017SecretToken
    systempassword: SystemPassword2017SecretToken
    dbsnmppassword: DbSnmpPassword2017SecretToken
    pdbadminpassword: PdbAdminPassword2017SecretToken
    db_user_password: DbPassword2017SecretToken (for created DB schema)
    ```

Example Playbook
----------------

- Installing Oracle 11.2.0.1
  ```yaml
  - name: Install oracle db
    hosts: all

    roles:
      - role: lean_delivery.oracle_db
        oracle_version: 11
        patch_version: 11.2.0.1
        transport_web: http://my-storage.example.com
        oracle_images:
          - linux.x64_11gR2_database_1of2.zip
          - linux.x64_11gR2_database_2of2.zip
  ```

- Installing Oracle 11.2.0.3 from local files
  ```yaml
  - name: Install oracle db
    hosts: all

    roles:
      - role: lean_delivery.oracle_db
        oracle_version: 11
        patch_version: 11.2.0.3
        transport: local
        transport_local: /tmp
        oracle_images:
          - p10404530_112030_Linux-x86-64_1of7.zip
          - p10404530_112030_Linux-x86-64_2of7.zip
          - p10404530_112030_Linux-x86-64_3of7.zip
          - p10404530_112030_Linux-x86-64_4of7.zip
          - p10404530_112030_Linux-x86-64_5of7.zip
          - p10404530_112030_Linux-x86-64_6of7.zip
          - p10404530_112030_Linux-x86-64_7of7.zip
  ```

- Installing Oracle 11.2.0.4 with custom swap file size
  ```yaml
  - name: Install oracle db
    hosts: all

    roles:
      - role: lean_delivery.oracle_db
        oracle_version: 11
        patch_version: 11.2.0.4
        transport_web: http://my-storage.example.com
        oracle_images:
          - p10404530_112040_Linux-x86-64_1of7.zip
          - p10404530_112040_Linux-x86-64_2of7.zip
          - p10404530_112040_Linux-x86-64_3of7.zip
          - p10404530_112040_Linux-x86-64_4of7.zip
          - p10404530_112040_Linux-x86-64_5of7.zip
          - p10404530_112040_Linux-x86-64_6of7.zip
          - p10404530_112040_Linux-x86-64_7of7.zip
        oracle_db_swapfile: /oracle-swapfile-11
        oracle_db_swap_count: 2048
  ```

- Installing Oracle 12.1.0.2
  ```yaml
  - name: Install oracle db
    hosts: all

    roles:
      - role: lean_delivery.oracle_db
        oracle_version: 12
        patch_version: 12.1.0.2
        transport_web: http://my-storage.example.com
        oracle_images:
          - linuxamd64_12102_database_1of2.zip
          - linuxamd64_12102_database_2of2.zip
  ```

- Installing Oracle XE
  ```yaml
  - name: Install oracle db
    hosts: all

    roles:
      - role: lean_delivery.oracle_db
        oracle_version: xe
        transport_web: http://my-storage.example.com
        oracle_images:
          - linux.x64_11gR2_xe.zip
  ```

License
-------
Apache

Author Information
------------------

authors:
  - Lean Delivery Team <team@lean-delivery.com>
