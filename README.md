# yadc
A DFterm clone

## Build instructions

**Dependencies**

* [go-bindata-assetfs](https://github.com/elazarl/go-bindata-assetfs)
* [goxc](https://github.com/laher/goxc) (optional; for cross-compiling more
  easily)

**Build**

The `build.sh` script is recommended. You can pass `-r` or `--run` to run
`yadc` automatically after building. Any additional arguments (e.g. `--help`)
will be passed to `yadc` (this requires `-r`/`--run`).

```sh
$ go-bindata-assetfs web/...   # only necessary on first build or when changing web/*
$ go build
```

Note: If you prefer to serve files from the web/ directory (for example, to
avoid rebuilding for development purposes), you can pass `-servefs` to `yadc`.
Building without go-bindata-assetfs entirely is currently not supported,
however.
