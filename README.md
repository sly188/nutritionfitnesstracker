# Fitness and Nutrition Tracker
## Overview
A full-stack fitness tracking application built with Flask and React. 

This project demonstrates core full-stack development skills: modular backend architecture, 

secure authentication, REST API design, and responsive frontend development.

Users can log workouts, track daily nutrition (macros and calories), 

monitor weight progress with visualizations, 

create reusable workout templates, and manage fitness goals. 


## Architecture
Backend: Python Flask with SQLAlchemy ORM and modular blueprint structure  

Frontend: React with Chart.js for data visualization

Database: SQLite & PostgreSQL

Authentication: JWT

## Features
### User Authentication
Registration and login with JWT tokens

Password hashing

Token-based authorization

### Workout Tracking
Log individual workouts with exercise details

Can log sets, reps, and weight

Retrieve workout history

Create and mange workout templates

### Nutrition Tracking
Log macros (protein, carbs, fats, cals.)

Update and delete nutrition entries

Query nutrition data by date range

### Weight Tracking
Log daily weight

Retriev weight history

Chart.js integration for visual progress

### Goal management
Create fitness goals with target values

Track progress towards goals 

Update and mark goals as complete

## Getting Started
### Backend Setup
#### Install Dependencies
cd fitness-tracker

pip install -r requirements.txt

#### Set environment variables:
export DATABASE_URL="sqlite:///fitness.db"

export JWT_SECRET_KEY="secret-key-here"

#### Run server
python app.py

The backend runs on 

http://localhost:5000

### Frontend Setup

#### Install Dependencies
cd fitness-tracker-frontend

#### Start Server
npm start

npm install

The frontend runs on 

http://localhost:3000

## Important Files
app.py/ Main flask app and main backend

auth.py/ Authenticator, enables registration and logging in

goals.py/ Create and manage goals

templates.py/ Create, edit, and delete templates

workouts.py/ Log workouts. 
Workouts can be made into templates that can be reused on the day of so that they can be logged

weight.py/ Log weight into the website, creates graph of weight

models.py/ Database using SQLAlchemy


## Next Steps
Deployment to production environment

Enhance frontend features

Mobile app version
