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


def book_friday(auth, date):
    url = "https://multiresa.net/sports/app/req/requestResa.php?action=sendresa&idcompte=reebok&activite=58&refCRENO=64029591&numCRENO=1&lejour={}&lecreno=0800&leidU=0&resadirect=0&lenomU= &leprenomU= &letelU= &lemailU= &lemultiU=1&effectif=9&lepartenaireU=0&callback=jQuery11110057299936134415086_1589642160431".format(
        date)
    return get_with_auth(url, auth)


def book_wednesday(auth, date):
    url = "https://multiresa.net/sports/app/req/requestResa.php?action=sendresa&idcompte=reebok&activite=58&refCRENO=64288541&numCRENO=1&lejour={}&lecreno=0800&leidU=0&resadirect=0&lenomU= &leprenomU= &letelU= &lemailU= &lemultiU=1&effectif=9&lepartenaireU=0&callback=jQuery11110733734535711519_1589646622704&_=1589646622712".format(
        date)
    return get_with_auth(url, auth)


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


def main(email, password):

    d = datetime.date.today()
    next_wed, next_fri = next_weekday(d, 2), next_weekday(d, 4)

    print("> Running at {}".format(datetime.datetime.now()))

    # # Login
    res_login = login(email, password)
    auth = res_login.headers['Set-Cookie'].split(';')[0]
    print("> Successfully logged with token {}".format(auth))

    # # Book wednesday
    print("> Booking for wednesday {}".format(next_wed))
    res_wednesday = book_wednesday(auth, next_wed)
    print("> Booking for wednesday {}".format(res_wednesday.text))

    # # Book friday
    print("> Booking for friday {}".format(next_fri))
    res_friday = book_friday(auth, next_fri)
    print("> Booking for friday {}".format(res_friday.text))

    # # Logout
    logout()



if __name__ == "__main__":
    parser = optparse.OptionParser()

    parser.add_option('-e', '--email', action="store", dest="email")
    parser.add_option('-p', '--password', action="store", dest="password")

    options, args = parser.parse_args()

    main(options.email, options.password)
