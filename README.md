# Code for ONLP website
This is a Django based website for the NLP lab at BIU managed by Prof. Reut Tsarfaty.
The code includes landing page and Demo for YAP.

## Installation instructions

1. clone the repository to your local machine:
```$ git clone https://github.com/OnlpLab/Hebrew-Parsing-Demo.git```

2.Create a virtual environment:
```$ conda create -n onlp-website python=3.7.3```

2. Activate the virtual environment 
```$ source activate onlp-website```

3. Install dependencies with the setup script:
```$ sh setup.sh```

### Use after initial installation
The script creates a virtual environment named `onlp-website`. 
In order to run the website server, activate this environment:

```$ source activate onlp-website```

When activated, cd into the directory, if you are not already in it.
```$ cd Hebrew-Parsing-Demo```

Finally, call the server:
```$ python manage.py runserver```

Once up, you should see a screen as follows:
```
Django version 3.0.2, using settings 'hebrewUD.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
You can now open up `http://127.0.0.1:8000/` in any browser of your choice. 

