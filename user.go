package main

var (
    users map[string]*user // session ID -> user
)

type user struct {
    name string
    password string
    logged_in bool
    admin bool
}

func UserLoggedIn(name string) bool {
    for _, u := range users {
        if u.name == name {
            return u.logged_in
        }
    }
    return false
}
