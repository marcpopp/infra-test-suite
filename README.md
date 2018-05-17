# infra-test-suite

An Infrastructure Test Suite based on [TestInfra](https://testinfra.readthedocs.io/en/latest/)

TestInfra bietet gegenüber Alternativen wie ServerSpec oder Goss die folgenden Vorteile:
* sehr einfache Test-Syntax
* einfache und schnelle Installation und Konfiguration über pip (Python)
* plattformübergreifende Funktionalität (MacOS + Linux)
* Testinfra kann Ansible Inventories auslesen, die bereits verwendet werden. Hierdurch müssen nicht seperate Hostlisten für die Testausführung gepflegt werden

## Preparation

First all dependencies (e.g. TestInfra) need to be install:
```
$ pip install -r requirements.txt
```

or better: 
```
$ ./init.sh
```

## Usage

For running the actual tests there is another script called `run.sh`

### Execute all Tests

To just run all tests you can run the script like this:

```
$ ./run.sh ../ansible/inventory/
=============================================== test session starts ===============================================
platform darwin -- Python 3.6.2, pytest-3.2.3, py-1.4.34, pluggy-0.4.0 -- /usr/local/opt/python3/bin/python3.6
cachedir: .cache
rootdir: ...., inifile:
plugins: testinfra-1.8.0, xdist-1.20.1, forked-0.2
[gw0] darwin Python 3.6.2 cwd: ...
[...]
[gw5] Python 3.6.2 (default, Jul 24 2017, 18:48:54)  -- [GCC 4.2.1 Compatible Apple LLVM 8.1.0 (clang-802.0.42)]
gw0 [27] / gw1 [27] / gw2 [27] / gw3 [27] / gw4 [27] / gw5 [27]
scheduling tests via LoadScheduling

tests/sample/base.py::test_software[ansible://xxx-rsyslog-None] 
[...]
[gw3] PASSED tests/sample/base.py::test_software[ansible://xxx-rsyslog-None]

--- generated xml file: $pwd/results.xml ----
====================================== 23 passed, 4 xfailed in 19.49 seconds ======================================
```

On the console you get the tests output in human readable form.
The file `results.xml` can be parsed by Jenkins's JUnit Parser Plugin to show the results in the Jenkins WebGUI.
There is also a Plugin for IntelliJ to parse the results.xml: https://plugins.jetbrains.com/plugin/1867-xstructure


### Debug single tests

You can also execute a subset of tests to debug them. They will be run sequentially to allow you to read printed debug output:

```
$ ./run.sh ../ansible/inventory/ tests/sample/base.py
py.test --connection=ansible --ansible-inventory=../ansible/inventories/ --capture=no -v --junitxml results.xml tests/sample/base.py
=============================================== test session starts ===============================================
platform darwin -- Python 2.7.14, pytest-3.2.5, py-1.5.2, pluggy-0.4.0 -- /usr/local/opt/python/bin/python2.7
cachedir: .cache
rootdir: ..., inifile:
plugins: testinfra-1.9.0, xdist-1.20.1, forked-0.2
collected 77 items

tests/sample/base.py::test_software[ansible://xxx-rsyslog-None] PASSED
...
```


## Helper Funktionen

In der Datei `testHelpers.py` sind allgemeine Funktionen definiert, die von spezifischen Tests verwendet werden können. Die Methodennamen der Helperfunktionen dürfen *nicht* mit dem Prefix `test_` beginnen, da sie ansonsten von Testinfra als ausführbare Tests erkannt werden. Es ist darauf zu achten, dass der Quellcode der Helpermethoden dokumentiert ist.

Über den Helper `check_nrpe` können Nagios Checks, die auf den zu testenden Hosts liegen, in der Testsuite wiederverwendet werden.

## Spezifische Tests

Die spezifischen Tests sind im Ordner `tests` nach der jeweiligen Serverrolle strukturiert.

Zu beachten ist, dass Namen von Testmethoden Prefix `test_` beginnen müssen, damit Testinfra sie ausführen kann.


## Umgebungsvariablen

testinfra verwendet Ansible als Backend für das Verbinden mit den Hosts. Hierdurch ist es möglich, das Inventory-File des Openshift Ansible Installers für die Tests wiederzuverwenden. 
Alle Umgebungsvariablen, von Ansible genutzt werden, können auch mit testinfra verwendet werden. So lässt sich bspw. Ansible der Pfad zu der Passwortdatei für das Ansible Vault über die Umgebungsvariable `ANSIBLE_VAULT_PASSWORD_FILE` bekannt machen.
