# pylagolog

## install

```
sudo apt install python3-antlr3
git clone https://github.com/hibitomo/pylagolog
cd pylagolog
sudo ./setup.py install
```

## How to use

```
pylagolog -r rule.datalog -q query.datalog
```

### gRPC server

```
lagolog-server
```

### gRPC client

```
$ lagolog-client -a 'p(x) :- q(x)'  # Add rule
$ lagolog-client -a 'q("test")'
$ lagolog-client -q 'p(x)'          # Query
p("test")
$ lagolog-client -d 'q("test")'     # Delete rule
$ lagolog-client -q 'p(x)'
```
