package main

import (
	"flag"
	"fmt"
)

var addr = flag.String("addr", ":8000", "http service address")

func main() {
	flag.Parse()
	fmt.Printf("Serving HTTP on %s\n", *addr)
	startServer(addr)
}
