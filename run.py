from app import create_app
import locale
locale.setlocale(locale.LC_TIME, '')

app = create_app('config')

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
	app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])