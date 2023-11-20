Lab 06
Members: Eric Chen
Github Link: https://github.com/usc-ee250-fall2023/lab-06-rest-lab06_ericsc/

Note: My RPI is running into an issue where I cannot find a di_i2c library because the dexterindustries install doesn't complete.
It gives me a "This CFFI feature requires setuptools on Python >= 3.12. The setuptools module is missing or non-functional." error
and the TAs and CPs couldn't figure out how to fix it.

Question 1:
person is a dictionary whereas person_json is a json formatted string; json.dumps() always returns strings.

Question 2:
If we do sort_keys=True the order of the json keys are sorted alphabetically, and if we don't it maintains its original position.

Question 3:
I used the Spotify API using Client Credentials Flow because the other authentication methods require you to deploy a development
server or a web app. The process was registering as a developer on the Spotify platform, creating an app on their site, and using
the client_id and client_secret to send a post request to the server, which returned an authentication key allowing access to
publicly available information. I took the top global playlist and chose a song and its artists from the json data using a get request.

The format of the message will look like "song: Paint The Town Red, artists: Doja Cat"
If there are multiple artists, it will display multiple artists separated by commas.