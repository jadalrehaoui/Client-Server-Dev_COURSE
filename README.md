# Client Server Development
#### Jad Alrehaoui - SNHU
##### Writing maintable, readable and adaptable programs
Let's start by **readable**, writing a readable program consists of having a mindset that someone else will use the code and try to modify, update or change it completely. It is part of being on a team. So commenting the code and using a naming convention agreed on by the team is key. I tried my best to keep my code clean and readable by stating what is the functionality of each block, and how it doing what is required. 
**Maintainable** code has also something to do with having the mindset of keeping it clear for the reader. I managed to keep the code maintainble by not repeating myself, and by optimising the code for the reader. At the end of the day, the computer will follow the instructions as they are written, but for someone else to know what the code is about it needs to be maintainable. 
**Adaptability** is having a code that needs little change to work with different arguments. In my code I have an example of adaptability which is having the username and password saved in separate variables so that the connection string still work the same with a different user.

##### Approaching a problem as a computer scientist
Approaching a problem as a computer scientist is fun, because we always deal with problems and how efficient can we be solving them. At first I try to digest the problem and how complicated it is and how is it affecting the whole. Then I brainstorm ideas, these ideas can vary from the most silly solutions to the most complex ones. Then I filter the feasable solution keeping in mind that the simpler the better even with complicated things. When a solution is present there's always room to optimize and make it more efficient if it was accepted.

##### What do computer scientists do and why does it matter ?
A computer scientist is a jack of all traits in my perspective, they need to be smart, efficient and fast even if they look like they are sitting on a screen all day which I like. We design, create and build systems to make life easier, faster and more efficient. 

# Repo talk and explain
This project requires a mongo database and python to be installed. The mongo database holds records about animals. I was to create a dashboard showcasing the database and its documents. 

First I used the **mongoimport** command to import documents from a csv file to the local database
```
mongoimport --port 27017 --db AAC --type csv --headerline --collection animals --file ./datasets/aac_animals.csv
```
- 27017 is the port my mongodb instance is running on
- AAC is the database I want to create
- animals is the collection I want to add to the AAC database
- ./datasets/aac_animals.csv is the file to import data from

Then I tested it with some queries to check if the data is there
``` 
> mongosh # to access mongodb shell in the terminal
> show dbs # show all the databases available
> use AAC # enter AAC db
> db.animals.find({}) # find all records
```
Once I confirmed that database is set I set a user called **aacuser** with access only to the AAC database relying on the least privilege needed.
```
# in mongo shell
> db.createUser({"user": "aacuser", "pwd": passwordPrompt(), "roles": [{"role": "readWrite", "db": "AAC"}]})
```
Now that I have a user and password I can go ahead and start connecting python with the mongo db

To do that I defined a class called **AnimalShelter** that will act as a model in my MVC program and I used **pymongo** to connect to mongodb

**pymongo installation**

``` 
# in the terminal
> pip3 install pymongo
# or 
> pip install pymongo
```
Then in AnimalShelter __init__ I connected python to mongodb as such
```
class AnimalShelter(object):
    def __init__(self, username, password):
        self.client = MongoClient('mongodb://%s:%s@localhost:47040/AAC' % (username, password))
        self.database = self.client['AAC']
        try:
            x = dumps(self.database.animals.find_one())
        except:
            print("Failure")
```
the try except block is to ensure that the connection was successful

Then I implemented the CRUD function with the help of [pymongo documentation](https://pymongo.readthedocs.io/en/stable/index.html)

[Then using dash framework I coded the dashboard](https://dash.plotly.com/)

Thanks for reading !
Cheers !
