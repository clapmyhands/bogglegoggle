# bogglegoggle

An application to run the game boggle with very barebones functionality. Still very lacking in user experience and might be buggy.

can be tried [here](http://bogglegoggle.sytes.net/boggle/game) -> do read section 2 first for example screenshot

1. [API](#api)
2. [Frontend](#frontend)
3. [Details](#details)

---------------------

## API
### Get random board

* **URL**
  
  *GET* `/api/v1.0/boggle/boards`

* **response**

  ```{ "board_string": <string> }```

* **example**

  ```{ "board_string": "acedlug*e*htgafk" }```

### Find word in board

* **URL**
  
  *GET* `/api/v1.0/boggle/boards/<board_string>/word/<word>`
  

* **URL Example**
  
  *GET* `/api/v1.0/boggle/boards/acedlug*e*htgafk/word/eight`

* **URL Param**

  `board_string`: current board in string format
  
  `word`: word to be searched

* **response**

  ```
  {
    "word": <string>
    "score": <int>
  }
  ```

* **example**

  ```
  {
    "word": "eight"
    "score": 5
  }
  ```

* **Note**

  Only word with length>=3 will be scored. Any word with invalid length/not in dictionary will result with 0 score.
 
### Create a new match

* **URL**
  
  *POST* `/api/v1.0/boggle/matches`

* **response**

  `{ "match_id": <string> }`

* **example**

  ```
  {
    "match_id": "a981218a-183e-4c53-b1b9-1187366d38c3"
  }
  ```

* **Note**

Create a new match entry in the database. This entry records all things related to a match (board, player names, words, and scores).

### Get match status

* **URL**
  
  *GET* `/api/v1.0/boggle/matches/<match_id>`

* **URL Param**

  `match_id`: match identifier
  
* **response**

  if ongoing:
  
  ```
  {
    "match_id": <string>,
    "status": "ongoing"
  }
  ```
  
  if finished:
  
  ```
  {
    "match_id": <string>,
    "board_string": <string>,
    "p1_name": <string>,
    "p1_words": <List[String]>,
    "p1_score": <int>,
    "p2_name": <string>,
    "p2_words": <List[String]>,
    "p2_score": <int>,
    "status": "finished"
  }
  ```
 

* **example**

  ```
  {
    "match_id": "a981218a-183e-4c53-b1b9-1187366d38c3",
    "board_string": "acedlug*e*htgafk",
    "p1_name": "Clasp",
    "p1_words": ["huge", "hug"],
    "p1_score": 7,
    "p2_name": "Stefan",
    "p2_words": ["eight"],
    "p2_score": 5,
    "status": "finished"
  }
  ```
  
* **Note**

  This API will contain different response depending on match status. `"status"` can be used to determine whether additional information is sent.
  
### Join a match

* **URL**
  
  *POST* `/api/v1.0/boggle/matches/<match_id>/session`

* **URL Param**

  `match_id`: match identifier

* **URL Example**
  
  *POST* `/api/v1.0/boggle/matches/a981218a-183e-4c53-b1b9-1187366d38c3/session`


* **response**

  ```
  {
    "match_id": <string>,
    "board_string": <string>
  }
  ```

* **example**

  ```
  {
    "match_id": "a981218a-183e-4c53-b1b9-1187366d38c3",
    "board_string": "acedlug*e*htgafk"
  }
  ```
  
* **Note**

  Retrieve match information needed to start. currently includes `"board_string"`.

### Update match with player move

* **URL**
  
  *Put* `/api/v1.0/boggle/matches/<match_id>`

* **URL Param**

  `match_id`: match identifier

* **URL Example**
  
  *Put* `/api/v1.0/boggle/matches/a981218a-183e-4c53-b1b9-1187366d38c3`
  
* **Data**

  Data are send as JSON string. Use `Content-type="application/json"` and `Json.stringify()`
  
  ```
  {
    "name": <string>,
    "words" <List[string]>
  }
  ```

* **response**

  ```
  {
    "match_id": <string>,
    "status": "finished"/"ongoing"
  }
  ```

* **example**

  ```
  {
    "match_id": "a981218a-183e-4c53-b1b9-1187366d38c3",
    "board_string": "finished"
  }
  ```
 
* **Note**

  Match is ongoing until both player finish their game. Calling this API with a finished `match_id` will result in abort from server (400).
  
  Score is not sent together. Score will be recalculated in the server.


## Frontend

## Design Details

* **Get random board**

  Initially I wanted a `Get board` API which can return newly generated board and previously generated board. Eventually split and currently only `Get random board` is implemented. Random board can be picked from board list kept in redit set.

* **Getting Specific board**

  currently not done as `board_string` is the board itself. Previous idea was using md5 to obscure board but it requires 32 char while board is currently only 16 char.
  
* **Generating board**
  
  Currently not implemented but based on searching around, there are ways to generate board.
  
  1. random shake from Hasbro official boggle dice.
  2. Use english letter distribution
  3. do Reverse Boggle (generate boggle board from possible word list) [SO discussion](https://stackoverflow.com/questions/21593925/how-to-create-a-boggle-board-from-a-list-of-words-reverse-boggle-solver?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa)
  
  Option 1 would only work for 4x4 and up to 6x6 official boggle board while option 2 and 3 could theoretically be used to generate any MxN board.
  
  These aren't really related to any of the design decision made however, the eventual goal would be to generate a random board for every boggle game - only keeping board if its in a match.
  
* **Match player**

  Currently only using name input however it should be easy to extend to user ID. Linking match to User ID would also allow for match history and interaction between user e.g follow/friend, challenge, etc.

* **Redis Usage**

  Redis used to store word list per board. At first `Find Word` call for every board, all possible word on the board are searched using DFS and Dictionary Trie. Solution word list is then stored for subsequent `Find Word` call.
  
  Currently redis is used more like a cache.

* **Database Usage
  
  Only Match information is stored in database. We can also store score information(currently only based on word length). We can also store Dictionary and even have multiple language dictionary.
  
* **Stateless application server**

  The application server is almost stateless as it does not keep any information on memory.
  
  1. `get random board` retrieves random board from redis
  2. `Find word` solve the board and store it in redis. Every subsequent call would retrieve from redis if found.
  3. `Create match` creates a new entry in the database directly.
  4. `Join match` takes the related `board_string` from redis using the passed `match_id`
  5. `Get match status` retrieve information and only filter based on match status before replying back to client
  6. `Update match` process the passed parameter (name, words) and update the relevant database entry
  
  Dictionary is currently still loaded from file and kept in memory but dictionary can be moved to database too.
  If our application server is stateless, we can scale up by adding more server to handle requests.
  Since all related information to match are currently in one table, we can scale up by adding more write slave as long as the same match is routed to the same database.
  
* **Boggle Time Constraint**
  
  Officially Boggle is supposed to have a 3-minute time constraint for each game/match. Currently this is not implemented as I can't currently think of a way to enfore a 3-minute constraint without possible risk. Some method which have been considered:
  
  1. Time constraint based on request and response send and receive time --- Client can still cheat around this by changing the time they send the request.
  2. Enforcing the time client-side --- timer can obviously be stopped on javascript.
  3. Simulate the game on both side --- I want the prototype to be as stateless as possible and simulating the game would require to keep track of each ongoing match/game.
  4. Using token with validation on server-side --- still require to keep token time validity. Probably can be saved in redis. Need to research more on this method.
  
  In the end, I decided to leave time constraint alone and let client-side code decide when to send update.
  
## Application Detail

- Deployed on Amazon AWS EC2 Asia(Singapore)
- Deployed with Apache 2 - Mod_wsgi(python wsgi apache mod)
- Developed with Flask - Python 3.6
- SQLite database
  
