package main

type sem struct {
    count int
    ch chan bool
}

func NewSem() (s *sem) {
    s = new(sem)
    s.count = 0
    s.ch = make(chan bool)
    return
}

func (s *sem) Inc() {
    s.count += 1
}

func (s *sem) Dec() {
    s.ch <- true
}

func (s *sem) Wait() {
    for {
        <- s.ch
        if s.count <= 0 {
            return
        }
    }
}
