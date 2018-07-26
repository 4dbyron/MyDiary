# MyDiary
MyDiary is an online journal where users can pen down their thoughts and feelings.


[![Coverage Status](https://coveralls.io/repos/github/4dbyron/MyDiary/badge.svg?branch=developer)](https://coveralls.io/github/4dbyron/MyDiary?branch=developer)

[![Build Status](https://travis-ci.org/4dbyron/MyDiary.svg?branch=developer)](https://travis-ci.org/4dbyron/MyDiary)

[![Maintainability](https://api.codeclimate.com/v1/badges/7ef8acd847da1bd0fdf4/maintainability)](https://codeclimate.com/github/4dbyron/MyDiary/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/7ef8acd847da1bd0fdf4/test_coverage)](https://codeclimate.com/github/4dbyron/MyDiary/test_coverage)


## Getting Started
Clone 
- https://github.com/4dbyron/MyDiary.git<br/>
or
- git@github.com:4dbyron/MyDiary.git<br/>
or<br/>
[Open live Preview](https://4dbyron.github.io/MyDiary/UI/index.html)


### Prerequisites

To clone, you can click on the `clone or download` button on the left of [this page](https://github.com/4dbyron/MyDiary).
<br/>This option is only preferred when you don't have  `git` installed on your system.

In case you already have git installed e.g through `apt-get install git` on Linux(Debian Derivatives).

Cloning can be done by:

    `git clone https://github.com/4dbyron/MyDiary.git`
or
    `git clone git@github.com:4dbyron/MyDiary.git`
</p>


### Installing
MyDiary has UI and API sections.
Depending on the part you are interested in, you can follow its respective instructions.

#### 1. The User Interface (UI)
- To render the User interface, navigate to MyDiary directory(Appears where we clones our repo)
- while in `MyDiary` you will see the  `UI` directory. navigate to it.
- launch `index.html` with a your favourite browser

e.g <br/>
```cd MyDiary/UI```<br/>
```sensible-browser index.html```

#### 2. The Application Programmable Interface
#####once the repository has been cloned
 - Navigate to the *api* folder/directory 
	with `cd MyDiary/api` command 
	or 
	with your File Explorer.
 - [Install and Setup your virtual environment](https://docs.python-guide.org/dev/virtualenvs/)
 - run 
	`pytest -v`
	or
	`pytest -v test_app.py`
	or
	`python -m pytest test_app.py`

### Testin With Postman
- Start the server with `python app.py`
- launch Postman and enter in the desired endpoint to test.
Example `GET /entries` fetches all entries.
to achieve this with postman, you would to a GET request URL as:
```127.0.0.1:5000/api/v1/entries```



### UI Built With
- HTML
- CSS
- Javascript


## Contributing

Improvements to this application are highly welcomed.
for now, reviewing the pull requests will one way of doing so. 

## Project Management
- Version Control: Git & Github
- [MyDiary PivotalTracker](https://www.pivotaltracker.com/n/projects/2184264)


## Authors

**Byron Taaka**

## Acknowledgments

* [Andela Kenya](andela.com)
* MaryAnne Ng'ang'a
* Eugene Mutai

