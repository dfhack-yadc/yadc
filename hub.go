package main

type hub struct {
	dfconn *connection
	clients []*connection

	addconn chan *connection
	rmconn chan *connection
}
