# jelver-cli

Introducing the jelver command line that will trigger all the frontend testings.

![jelver-homepage](https://static.wixstatic.com/media/cdef75_3b1b713b184c4607b0acf3032711660c~mv2.png/v1/fill/w_1024,h_780,al_c,q_90,enc_auto/cdef75_3b1b713b184c4607b0acf3032711660c~mv2.png)

### I. Create an account and get your credentials

Click [here](https://app.jelver.com/integration) to start your testing journey.

### II. Integrate with us

Add the client script to the main html page of your website.

```html
<html>
<body>
  ...
  All your html code is here
  ...
  <script src="https://app.jelver.com/testing.js?publicKey=<YOUR_API_KEY>&isProduction=<IS_PRODUCTION>"/> 
</body>
</html>
```


### III. Install jelver-cli 

Install the python packages locally
```sh
pip install jelver-cli
```


### IV. Start testing 

Trigger a full backend testing
```sh
jelver test --api-key=<YOUR_API_KEY>
```

Bear in mind, that it usually takes a bit of time for our backend to analyse all the user flows that will be used to build your test cases.

### V. Done

Your frontend can now be tested at anytime! You can now go back to coding, we have your back!  

### One more thing

You can list all the test cases

```sh
jelver cases ls --api-key=<YOUR_API_KEY>
```

And add or remove some based on your needs.
```sh
jelver cases add <CASE_IDS> --api-key=<YOUR_API_KEY>   # include the CASE_IDS
jelver cases rm <CASE_IDS> --api-key=<YOUR_API_KEY>    # exclude the CASE_IDS

# CASE_IDS are list of case id separated by a comma
# ex: CASE_IDS="1,2,5"
```


