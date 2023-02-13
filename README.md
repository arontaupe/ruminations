# ruminations
 a tool to collectivize online buying behaviour, increasing privacy and autonomy


welcome.
this app is written in python and served with flask.
it is fully dockerized, so that it can be served remotely

to run:
```shell
cd ruminations
```
```shell
docker-compose build
docker-compose up
```
afterwards, there should be the latest image available at
```shell
localhost:5003
```
or whatever port was defined in the environment variables


in order to change any design element, please change the .html code in the template's directory.

for a quick online demo:
use ngrok,
detailed description following.

enjoy privacy. 
embrace insanity.


---

## How to use the Scraper:

```sh
cd ruminations/amazon_scrapy/amazon_scrapy/spiders
scrapy crawl amazon -o test.csv
```
then, in the test.csv there will be the results
