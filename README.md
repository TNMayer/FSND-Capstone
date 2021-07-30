# Udacity Full Stack Capstone Project

This is the Readme file and also the documentation for my capstone project for Udacity´s Full Stack Developer Nanodegree. To dive right into the app you can use the following endpoint links.

Local API Endoint Link: http://127.0.0.1:8080<br>
Heroku API Endpoint Link: https://tnmayer-fsnd-capstone.herokuapp.com

## Setup local POSTGRES Database

In order to be able to use the endpoints you need a local Postgres endpoint with the same configuration that is used in the application. This can be done via the subsequent psql commands.

First you have to login into your psql command line (e.g. psql -U postgres)

```
create database fsnd_capstone;
create user fsnd with encrypted password 'fsnd';
grant all privileges on database fsnd_capstone to fsnd;
```