# yadc
A DFterm clone

## Build instructions

**Dependencies**

* [goxc](https://github.com/laher/goxc)
* [go-bindata-assetfs](https://github.com/elazarl/go-bindata-assetfs)

**Build**
```sh
$ go-bindata-assetfs web/...   # only necessary on first build or when changing web/*
$ go build 
```
