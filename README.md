# Welcome to SwapStop

SwapStop is a web application for students to facilitate trades with one another — no money involved. This is our documentation for SwapStop.

# Getting Started

Check if you have pip by running <br/>
`pip --version` <br/>
If pip is not installed, you will get an error that looks like "pip not found". Install pip using [Online Guide](https://www.geeksforgeeks.org/download-and-install-pip-latest-version/) <br/>

### Make sure you are in the swapproj folder

Execute: <br/>
`pip install -r requirements.txt`

# Running Flask

### Make sure you are in the SwapStop folder

To run our application in Flask, execute these three lines: <br/>

`export FLASK_APP=swapproj` <br/>
`export FLASK_ENV=development` <br/>
`flask run` <br/>

Finally, check which port is output by running flask (likely something along the lines of 127.0.0.1:5000), copy this address, and open it in your browser of choice. You should be able to see and interact with our application now!