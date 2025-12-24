# POKÉTRACKER
### Video Demo:  <https://youtu.be/bYlmAYWZBOY>
### Description:
The Pokétracker application is a gamified personal financial planner as my final project for CS50P's final project.
A trainer's (user's) progress in their financial journey is represented through their partner pokémon and will grow and evolve as they reach their financial goals.
The application is built on the simple 50/30/20 rule where 50% of one's income goes towards "needs", 30% goes towards "wants", and 20% goes towards "savings."
The ultimate goal is to bring a simple, less intimidating approach to finances in a simple gamified approach that we recognize from our childhood.

#### Features:
1. **Log Expenses:**
    - Allows user to log expenses by categorizing them into needs and wants. "needs" and "wants" are case sensitive and blank space sensitive. Input is stored in dictionary state["expenses"] to be used later to calculate deltas from targets in choice 3.
2. **Log Savings:**
    - Allows user to log savings and stores savings into state["total_saved"] to be used later to calculate deltas from targets in choice 3. If pokemon evolves, prints a message informing user. Accomplishes this by comparing the stage before the savings with the stage after updating progress.
3. **View 50/30/20 Targets Summary**
    - Outputs target metrics for the year and associated deltas to achieve the target metrics. Also displays how much gyms have been defeated by how much savings acquired.
4. **View Pokemon Progress**
    - Showcases Pokemon, their current level representing how many milestones accomplished, their xp towards the next level representing in percentage how close they are to the next milestone, and their streak of using the application.
5. **Change Income**
    - As people's income might change throughout the year, the Poketracker application allows you to change your income to recalculate new targets.
6. **Quit**
    - Allows user to save their data into a json file and quit out of the program.

#### Functions:
- Pokemon class consists of STARTERS dictionary and a starter_selection class method. I chose to make this a class to bundle up the dictionary and function to help keep my code organized and allow me to easily add more functionality to the class if I wish to build upon this version.
    - **Starters:** Dictionary consisting of keys and lists. Each list contains the evolutionary line of a different pokemon.
    - **starter_selection:** Randomly selects a starter, prints a message, and returns whichever selected starter to the object. This allows the game to save a pokemon to the load_state.
- The program additionally has a total of 5 functions. Two of these 5 functions are used towards saving and loading game play; while the remaining three specifically relate to functionality in the application.
    - **save_state:** Writes over json file, named "save.json" with user data, defined as variable "state."
    - **load_state:** If save.json exists, function returns the a usable python data structure by using json.load(). Contraily, if the file does not exist, the function returns none. If function returns none, player is new and the main function begins to assign values to "state" variable.
    - **compute_target:** Inputs expenses and yearly_income and outputs targets and deltas for choice 3. Firstly, the function assigns the 50/30/20 rule to targets object. targets is a dict object consisting of needs, wants, and savings keys and values created by multiplying the yearly_income with 0.5, 0.3, and 0.2 respectively. deltas object is also a dictionary consisting of a loop to find progress on each of the targets. Positive numbers showcase progress left and negative numbers showcase additional saving/spending The function returns a dict object consisting of targets dictionary with the key "targets" and deltas dictionary with the key "deltas" to an object that can be called on in choice 3.
    - **gyms_milestones:** The function inputs total_saved and milestones to output the number of savings milestones the user has reached as an int value. Used in option 3 to update gym progress and in function "update_progress." Milestones are defined by total savings as students earn many additional sources of income like scholarships and odd jobs. Setting milestones allow students to set goals of how much total income they aspire to earn for the year.
    - **update_progress:** Takes total_saved and milestones and returns a user's current progress toward their financial milestones represented as "XP" (float) and determines the "level"(int) which represents the numbers of milestones accomplished and "stage"(int) of their Pokemon. User's pokemon starts at stage 1. Upon completing over half of the milestones, user's pokemon reaches stage 2. After completing all milestones, user's pokemon will reach stage 3.

#### How It Works:
If user is a new player, user will be asked for their name, yearly income, and their major financial milestones(can be unordered).
    - Example:
        What is your name trainor: Varsan
        Enter your yearly income: 300
        Enter 3 or more of your major financial milestones(seperated by ,): 400,150,200
I leveraged regex to ensure inputs follow the correct format to not to break the rest of the code.
Following inputs, the user will be given a Pokemon chosen at random. You can then input numbers to activate the different features in the app.

#### Files:
1. project.py: Contains main function used for the project. Additionally contains classes and other custom functions.
2. README.md: Features a detailed description on the project and all its features. At the top of the file, there is a youtube video URL also explaining how the project works.
3. requirements.txt: Lists all libaries used in the project.py file.
4. save.json: Includes save data for the game
5. test_project.py: Tests 3 of the core custom functions (compute_target, gyms_milestones, and update_progress) used in project.py
