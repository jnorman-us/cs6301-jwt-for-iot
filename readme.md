
# CS 6301.003 - Final Project
The final project for CS 6301.003. My project is a demonstration of the security in a smart home system written in Python.

## Inspiration
What inspired me to make this project was the paper:
> A Study on a JWT-Based User Authentication and API Assessment Scheme Using IMEI in a Smart Home Environment

It describes an IoT home security system that defends against 3 major attack vectors using JWT:

 1. Logging in a user (Protocol #1)
 2. Registering a new device into the network (Protocol #2)
 3. Calling device APIs (Protocol #3)

## Objectives
My objective is to implement the calculations described in the paper to secure these 3 important attack vectors. I will create a simple demonstration showing these handshakes in action while printing the calculated values to follow along with.

## System Design
A python program using a JWT library. Just a single program with objects for the client and server. Instead of using the actual network, just mock the communications between the server/client objects.

## Installation
You must be using Python 3 to run this project. To install the Python Virtual Environment, type:

	python3 -m venv venv/
	source venv/bin/activate
	pip3 install -r requirements.txt

We just installed the dependencies for this project. You can read the requirements.txt to review the libraries I used.

## Implementation
To run the program, run the command
	
	python3 main.py

### Login Interface (Protocol #1)
The first UI is the login UI. The credentials for logging in are:

 - **Username**: `asd`
 - **Password**: `asd`

After submitting, you will see the console output the calculations being run on both the client and the server. The produced hex values are the outputs of the handshake that takes place to establish the session and generate the JWT.

![](https://github.com/jnorman-us/cs6301-jwt-for-iot/blob/main/Protocol%20%231.png?raw=true)

### Device Management Interface (Protocol #3)
After logging in, you should be able to see the Device Management interface. Here, you can see the stored JWT token and Random Number. You can also see a list of existing devices and press the buttons to toggle the lightbulbs. This triggers a call to the server, which will authorize the transactions; the calculations that take place will be printed in console according to the protocol here:

![](https://raw.githubusercontent.com/jnorman-us/cs6301-jwt-for-iot/main/Protocol%20%233.png)

### Adding a new Light Bulb (Protocol #2)
There is also a button to add a new light bulb to the smart home. Pressing it will trigger calls to the server and will require calculations to be run to ensure the user is allowing the addition of the new device (outputted in console). Here is the protocol:

![](https://raw.githubusercontent.com/jnorman-us/cs6301-jwt-for-iot/main/Protocol%20%232.png)

### Exiting
To exit the Python Virtual Environment, type into console:

	deactivate

## Struggles
Initially, my project was supposed to be a React.JS page illustrating the execution of these 3 protocols. However, Javascript, especially on the browser side, has very minimal support for cryptography functions. Reasons for this include:

 - Javascript is too slow to run expensive computations for cryptography
 - No use case for the frontend to run cryptography with most applications being centralized
 - No native data-structure for the storage of byte arrays

Since I had been using Python for my CS 6348 (Data and Application Security) class, I chose to switch to Python. The UI isn't as responsive as a React.JS app, but it is able to run the calculations for all 3 protocols.

Also, I wanted to implement the timestamping feature that would have alleviated the vulnerability to replay attacks, but I was not sure about the calculations presented. A timestamp is typically 4 bytes, whereas the outputs of the hash function and the random number generator are 32 bytes. Concatenating 4+32 bytes produces 36 bytes, but I'm not sure how to XOR 36 bytes and 32 bytes.

## Screenshots

### The handshakes run for logging in, turning off a lightbulb, and adding a new bulb
![](https://raw.githubusercontent.com/jnorman-us/cs6301-jwt-for-iot/main/image.png)

### The UI for logging in
![enter image description here](https://raw.githubusercontent.com/jnorman-us/cs6301-jwt-for-iot/main/LoginForm.png)

### The UI for Managing Devices
![enter image description here](https://raw.githubusercontent.com/jnorman-us/cs6301-jwt-for-iot/main/DeviceManager.png)

## Directions
In order for this implementation to be useful, I would like to

 - Add these handshakes to a real IoT setting
 - Conduct communications over the network, instead of through a mockup
 - Implement the timestamping feature to prevent replay attacks
