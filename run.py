import requests
import time
import optparse
import datetime


def login(email, password):
    url = "https://multiresa.net/sports/club/reebok/membre-connexion.html"

    payload = {
        'login': email,
        'password': password,
        'uniqid': 'formulaire_connexion',
        'submit': 'Connexion'
    }

    return requests.request('POST', url, data=payload)


def logout():
    url = "https://multiresa.net/sports/club/reebok/membre-deconnexion.html"

    return requests.request('GET', url)


def get_with_auth(url, auth):
    headers = {'Cookie': auth}
    return requests.request("GET", url, headers=headers)


def book_monday(auth, date):
    url = "https://multiresa.net/sports/app/req/requestResa.php?action=sendresa&idcompte=reebok&activite=58&refCRENO=64289098&numCRENO=1&lejour={}&lecreno=1215&leidU=0&resadirect=0&lenomU= &leprenomU= &letelU= &lemailU= &lemultiU=1&effectif=9&lepartenaireU=0&callback=jQuery111107388843733109449_1591020662852&_=1591020662853".format(
        date)
    return get_with_auth(url, auth)


def book_tuesday(auth, date):
    url = "https://multiresa.net/sports/app/req/requestResa.php?action=sendresa&idcompte=reebok&activite=58&refCRENO=64288860&numCRENO=1&lejour={}&lecreno=1215&leidU=0&resadirect=0&lenomU= &leprenomU= &letelU= &lemailU= &lemultiU=1&effectif=9&lepartenaireU=0&callback=jQuery1111006633657723714825_1591020966450&_=1591020966451".format(
        date)
    return get_with_auth(url, auth)


def book_wednesday(auth, date):
    url = "https://multiresa.net/sports/app/req/requestResa.php?action=sendresa&idcompte=reebok&activite=58&refCRENO=64288541&numCRENO=1&lejour={}&lecreno=0800&leidU=0&resadirect=0&lenomU= &leprenomU= &letelU= &lemailU= &lemultiU=1&effectif=9&lepartenaireU=0&callback=jQuery11110733734535711519_1589646622704&_=1589646622712".format(
        date)
    return get_with_auth(url, auth)


def book_friday(auth, date):
    url = "https://multiresa.net/sports/app/req/requestResa.php?action=sendresa&idcompte=reebok&activite=58&refCRENO=64029729&numCRENO=1&lejour={}&lecreno=1145&leidU=0&resadirect=0&lenomU= &leprenomU= &letelU= &lemailU= &lemultiU=1&effectif=9&lepartenaireU=0&callback=jQuery111106262353388596023_1589753468290&_=1589753468292".format(
        date)

    return get_with_auth(url, auth)


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def main(email, password):

    d = datetime.date.today()
    next_mon, next_tue = next_weekday(d, 0), next_weekday(d, 1)

    print("> Running at {}".format(datetime.datetime.now()))

    # # Login
    res_login = login(email, password)
    auth = res_login.headers['Set-Cookie'].split(';')[0]
    print("> Successfully logged with token {}".format(auth))

    # # Book wednesday
    print("> Booking for monday {}".format(next_mon))
    res_monday = book_monday(auth, next_mon)
    print("> Booking for monday {}".format(res_monday.text))

    # # Book friday
    print("> Booking for tuesday {}".format(next_tue))
    res_tuesday = book_tuesday(auth, next_tue)
    print("> Booking for tuesday {}".format(res_tuesday.text))

    # # Logout
    logout()


if __name__ == "__main__":
    parser = optparse.OptionParser()

    parser.add_option('-e', '--email', action="store", dest="email")
    parser.add_option('-p', '--password', action="store", dest="password")

    options, args = parser.parse_args()

    main(options.email, options.password)
