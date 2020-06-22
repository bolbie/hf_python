from flask import Flask, render_template, request, escape, session, copy_current_request_context
from vsearch import search_for_letters
from threading import Thread
from time import sleep

from DBcm import UseDataBase, ConnectionError, CredentialsError, SQLError
from checker import check_logged_in

app = Flask(__name__)

app.config['dbconfig'] = { 'host':'127.0.0.1',
                           'user':'vsearch',
                           'password':'vsearchpasswd',
                           'database':'vsearchlogDB' }


@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are now logged in'


@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out'


@app.route('/search_for', methods=['POST'])
def do_search() -> 'html':
    """Extract the posted data; perform the search; return results."""

    @copy_current_request_context
    def log_request(req: 'flask_request', res: str) -> None:
        """Log details of the web request and the results in MySQL database."""
        sleep(10)
        with UseDataBase(app.config['dbconfig']) as cursor:
            _SQL = """insert into log
                  (phrase, letters, ip, browser_string, results)
                  values
                  (%s, %s, %s, %s, %s)"""
            cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res ))

    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search_for_letters(phrase, letters))
    try:
        log_req=Thread(target=log_request, args=(request, results))
        log_req.start()
    except Exception as err:
        print('***** Logging failed with this error:', str(err))
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    """Display this webapp's HTML form."""
    return render_template('entry.html',
                           the_title='Welcome to Search For Letters on the web!')


@app.route('/viewlog')
@check_logged_in
def view_the_log() -> 'html':
    """Display the contents of the vsearchlogDB as a HTML table."""
    try:
        with UseDataBase(app.config['dbconfig']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results from log"""
            cursor.execute(_SQL)
            contents = cursor.fetchall()
        titles = ('Phrase', 'Letters', 'Remote Addr', 'User Agent', 'Results')
        return render_template ('viewlog.html',
                                the_title='View Log',
                                the_row_titles=titles,
                                the_data=contents)
    except ConnectionError as err:
        print('Is your database switched on? Error:', str(err))
    except CredentialsError as err:
        print('Used-id/Password issues. Error:', str(err))
    except SQLError as err:
        print('Is your query correct? Error:', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))
    return 'Error'


app.secret_key = 'BolbieHFSecretKey'


if __name__ == '__main__':
    app.run(debug=True)
