# small_project_dev

# Small project development sandbox

It is a repository containing different projects I have started, which are in early development status. Some of them are one day, some couple day long. Made for educational purpuses.

## List of projects

  - [Weather API](#weather-API)

## Weather API

Program downloads the hourly weather data for the three days before the current one from openweathermap.org using the REST API. It looks for the periods where the temperature was increasing (identified by the start time). Then it saves a list of these periods to a JSON file, for each of them storing the start time, duration in hours, start and end temperatures, and the complete hourly source data for that range.

Then it opens the JSON file created and look for the period of the greatest temperature jump in one hour. Finally it displays information: which period (start - end, dates in ISO 8601 format), what and when the temperature jump occurred (previous temperature and change value in degrees Celsius, date from which the lower value comes from), what was the average humidity and pressure in the whole period.
