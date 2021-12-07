# Welcome to SwapStop
 
SwapStop is a web application for students to facilitate trades with one another — no money involved. This is our documentation for SwapStop.
 
# Getting Started
 
Check if you have pip by heading to your terminal and running <br/>
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
`flask run`
 
Finally, check which port is output by running flask (likely something along the lines of http://127.0.0.1:5000), copy this address, and open it in your browser of choice. You should be able to see and interact with our application now!
 

Once you have SwapStop successfully running in your computer's browser, please make an account. This can be done by navigating to the top right hand corner of the screen. There, to the left of “Login” you should be able to find “Register”. After this you should be presented with a Registration form. Each field is clearly labeled-- so, to properly register simply input what each field requests. Once properly registered, you will then be redirected to the login page. Login with the account you just made and you’ll have entered SwapStop!
 
Once logged in, you will be brought to the Marketplace —— SwapStop Grand Central Station, if you will. It is here where you can view all the items that other users of SwapShop currently have on sale. Here in the Marketplace, you are able to quickly skim through all of the items on sale. When you find an item that you’re interested in acquiring, click the view item button in the bottom left hand corner of that item’s card. This will take you to a more detailed depiction of the item, including the description, when the item was posted, and if the item is still available. From this screen, you are given the option to contact the owner of the selected item or return back to the marketplace. These options, “Back to Marketplace” and “Contact”, are distinctly labeled for an intuitive user experience. The “Contact” form only requires one input (a message), but your contact information will also be sent to the owner along with the message.
 
In order to post an item of your own, navigate to and click on the List Item page in the navbar. You will then be taken to the List Item page, where you will be required to enter the listing’s name, a description of the listing, and an img file that takes jpeg, png, gif, or jpg formats. The image file upload will indicate to you that an acceptable photo has, in fact, been provided. Once you provide valid inputs and click “Post Listing,” your item will be listed to the marketplace. If you would like to view your newly-created listing, you can go to the My Items page using the navbar. From here, you are able to see all of their listings, past and present. If you would like to view one of your items specifically, click the “view” found in the bottom left hand corner of the item’s card. This will take you to a page that displays not only an option to edit or delete the listing, but also displays any messages that have been sent with regard to the item that is being viewed.
 
If you would like to remove or edit a listing that you have previously posted, navigate to that item using My Items, click “view,” and then click “edit.” This will take you to a page that displays the current item information, as well as an “update” and “delete” button. To edit, simply type into the text boxes or click an entry from the dropdown, and then click the “update” button. To delete, click “delete” and you’ll receive a confirmation that your item was deleted. 
 
Finally, to log out, click “Log Out” in the top right corner, and to access the Marketplace, click either the SwapStop logo or “Marketplace” in the navbar.