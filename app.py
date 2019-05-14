from flask import Flask, render_template
import requests
import requests_cache
import json

app = Flask(__name__)


requests_cache.install_cache(cache_name='movies',backend='sqlite',expire_after=240)


class Parser:

	def __init__(self, url):
		self.url = url
		self.films = []

	def get_request(self,url):
		return json.loads(requests.get(url).text)

	def get_films(self):
		for film in self.get_request(self.url):
			self.films.append([
				film['title'],
				self.get_people(film['people'])
			])
		return self.films

	# To Do -- replace if statement and separate every logic into different functions
	# get people for each film
	def get_people(self, people_urls):
		# check if this film have all the people and get their names
		if len(people_urls) < 2:
			people = []
			for person in self.get_request(people_urls[0]):
				people.append(person['name'])
			return people
		else:
			people = []
			for people_url in people_urls:
				people.append(self.get_request(people_url)['name'])
			return people


@app.route('/')
def homepage():

	parser = Parser('https://ghibliapi.herokuapp.com/films/')
	films = parser.get_films()
	return render_template('movies.html', films=films)


if __name__ == '__main__':

	app.run(host='0.0.0.0', debug=True,  port=8080)