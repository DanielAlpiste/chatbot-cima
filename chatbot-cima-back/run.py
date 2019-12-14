from app import create_app
import locale
locale.setlocale(locale.LC_TIME, '')

app = create_app('config')

if __name__ == '__main__':
	app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
