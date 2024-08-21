# UMD Professor Ranker
Discord bot that ranks UMD professors/courses based on their ratings or average GPA

![Screenshot 2024-08-21 161753](https://github.com/user-attachments/assets/c1efa623-6522-43d9-b2ac-a285624041a0)

## Installation

### Prerequisites
- [Python]
- [Pip]

Download the script to computer
```shell
git clone https://github.com/justinn123/UMD-Prof-Ranker.git
cd UMD-Prof-Ranker
```

Then download required packages for the script
```shell
pip install -r requirements.txt
```

## How It's Made: 

**Tech Used**: Python, Python Discord Library, Planet Terp API

The bot uses Planet Terp API to get data about courses and professors. The information includes professor ratings, course evaluations, and average GPA statistics. By analyzing this data, the bot can rank based on either ratings or GPA. There is also a feature where it ranks courses in a specific department such as Computer Science by GPA,
so users know what classes are more difficult. Users can also look up a specific professor to get their average rating and GPA. Users can get even more specific information by providing a course the professor has taught to get data for that specific course.

## Current Issues:

1. If the ranking list is too long, the bot will not be able to send the data to Discord due to the 2000-character limit.
2. The discord commands are also very long making it tedious to type and get data, I am currently working on creating aliases for commands and shortening them to improve user experience.
3. The bot is still in the early stages of development, so there is not much functionality outside of ranking courses and professors.

## Lessons Learned: 

Working on this project provided valuable experience in parsing JSON files and sorting data efficiently. By interacting with the API and handling the returned data, I developed a deeper understanding of structuring and managing JSON data. Additionally, sorting this data based on various criteria enhanced my skills in data organization and manipulation. 


