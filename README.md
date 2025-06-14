
# Practical Challenge – Weather Forecast API (IPMA)

Simple REST API that collects weather forecast data from the official IPMA website (https://www.ipma.pt/pt/otempo/prev.localidade.hora/) and return what was received.


## API Reference

```http
  GET /get_weather_info/{day}&{district}&{local}
```

| Parameter | Type     | Description                                       |
| :-------- | :------- | :--------------------------------                 |
| `day`     | `int`    | **Required**. Specific day to fetch the data      |
| `district`      | `string` | **Required**. Specific district to fetch the data |
| `local`      | `string` | **Required**. Specific local to fetch the data    |

#### get_weather_info(day, district, local)

Takes the weather information for the parameters combination.


## Installation

Install and setup Docker following the steps for your OS. Download and setup found here: https://docs.docker.com/desktop/

Clone the git project found here: URL.

```bash
  git clone <repository-url>
```

## How to run the application

Go to the diretory that you've cloned the project.

```bash
  cd my-project
```
At terminal create a virtual environment and activate it.

```bash
  python3 venv .venv
  source .venv/bin/activate
```

Execute the following command to build and run the application on Docker.

```bash
  docker compose up --build
```

## How to use the API

After built, enter on any browser and make a request for the API, as follows:

```bash
  http://localhost:8000/get_weather_info/{day}&{district}&{local}
```

Change `day`, `district` and `local`.

#### Example:

```bash
  http://localhost:8000/get_weather_info/15&Porto&Porto
```

#### Restrictions:

The default IPMA application shows the weather forecast for 10 days counting from the current date to 9 days ahead. So `actual_day + 9 >= day >= current_day`.

If an invalid combination of `distric` and `local` is put at the `url`, the default behaviour of the IPMA application is to show the information for Lisbon.

#### Problem found:

For an unknown reason, probably timout, the execution of the application could work or not work for the same request. When it happens, you should restart the application and try again.

At the Docker container terminal, press `Ctrl + C` to stop the application, and execute these shell commands at the local terminal to restart the container and the application:

```bash
  docker stop $(docker ps -aq) && docker rm $(docker ps -aq)
  docker compose up --build
```