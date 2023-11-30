# Team Collab 

Brief project description and purpose for future developers and users

---
## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Testing](#testing)
- [Deployment](#deployment)
- [Technologies Used](#technologies-used)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---
## Introduction

This project aims to build an app that works smoothly with Slack (might be able to support teams later on), promoting teamwork by recognizing achievements (kudos). The target users for this product are workspaces with fewer than 2000 people. 

The product deployed will be a bot that is integrated into Slack, allowing users to interact with the bot to give kudos (acknowledgement messages) to another user, with an attached message and chosen attached "company values", which are defined as values (keywords) that the Slack workspace wants to achieve. 

---
## Features

1. Acknowledge colleagues for their work done with kudos, and align each kudos with one or more corporate values.
2. Customize Corporate Values for a workspace. The project supports permission check, only **workspace admin, workspace owner, and workspace primary owners** of a workspace is permitted to modify corporation values. You can learn more about Slack roles in this page: [Types of roles in Slack](https://slack.com/help/articles/360018112273-Types-of-roles-in-Slack). For our project, we will only be concerned about Workspace Primary Owner, Workspace Owners, Workspace Admins, and Full members.
3. Analyze an employee's statistics, including the number and values for the kudos received within a specified time frame. Only admins are permitted to view others' stats. 

---
## Getting Started [General Usage]

TODO: Fill in general user's steps in getting the bot running in their own workspace. 

---
## Getting Started [Developer]

In this part, we will guide you through the methods to be able to recreate what we have, please make sure you follow this guide as much as possible. 

### Prerequisites

Depending on your preference, you can start the project either locally, or deployed to the cloud. With these choices, we offer two sets of prerequisites. 

#### General requirements

- A valid Slack Development Account, which needs to be configured to run our bot. You should have a Slack Developer account if you have a regular Slack account. If you don't have a valid account, you can register a valid account here: [Slack API](https://api.slack.com/)
- A PostgreSQL Database that you have full control over. The ones used in development by the project is provided Microsoft Azure. You are also welcome to use a local database, as long as you have methods of connecting to it. 

#### Local Development

- Docker installed on your system **OR** Python >= 3.12.0
- If you choose to not use Docker, you also have the options of installing all the required packages from `requirements.txt`, under the `main` directory in our root directory of the project.

#### Online Deployment

- A valid Docker hosting platform, e.g. Heroku, AWS, Microsoft Azure, etc. The development of the project is carried out using Microsoft Azure. 
- A Docker Hub account, registered here: [Docker Hub](https://hub.docker.com/)

### Settings before deployment

#### Slack developer portal

Please follow the following steps precisely to obtain a working copy of our bot. 

First, go to Slack API's webpage: [Slack API](https://api.slack.com/)

![Your apps](images/your_apps.png)

Then, click on the right up corner, that says "Your apps". 

![Create new app](images/create_new_app.png)

Within this page, you want to click on "Create New App". 

You should now be able to select "From an app manifest", which pre-loads all the similar information that our project has setup in the past. 

Then, follow along the guide that is presented. 

1. Select the workspace (ideally your workspace that you have full control over) that you want your bot to be installed in
2. In the "Enter app manifest below" window, delete the original content and paste in the information from the file `manifest.yml` in the same directory as this markdown
3. Then hit "Create"

If everything is right, you should now enter the app's "basic information" page, which allows you to configure certain information about your bot, and also extract some of the **IMPORTANT INFORMATION** to use the bot with. 

Scroll down in this page to the "App Credentials" section, and you should see the following: 

![App credentials](images/app_credentials.png)

Within these fields, take note of the "Signing Secret", as we will use it later in `config.py`. 

Then, scroll down more, and you will find "App-Level Tokens". If there isn't any entries in there, simply click "Generate Token and Scopes", and select the scopes that it needs by referring to the picture below. 

![App level tokens](images/app_level_tokens.png)

After creating, you should be able to click the name of the newly created App Token, and obtain a "Token", as shown below (the one that begins with "xapp-x-xxx...").

![App level token value](images/app_level_token_value.png)

Note down the value of this app token as well. 

Lastly, under the "Install App" sub-menu on the left, as shown in the below figure, you should be able to obtain a "Bot Token". Note it down as well. The bot token should begin with "xoxb-xxxx..."

![Bot token](images/bot_token.png)

With all three of these available, we can now proceed to the configurations of our bot. 

#### config.py

Within `config.py`, there are a few fields to look out for: 

```python
# Connectivity configurations
SLACK_BOT_TOKEN = "xoxb-5933772890579-5945241825189-YUY5SWx1bvaMp3opBV8qeTq0"
SLACK_SIGNING_SECRET = "48928ff7a9457f0f4264af506b5b6bcf"
SLACK_APP_TOKEN = "xapp-1-A05TW1NB0CB-5948193295891-720a67e31f92b0c273bbe5ff3525501b3cdf79421f7aa4143d61ba6cc9d08c53"
```

Within `config.py`, you want to replace the values that we have in there with the new values that you have obtained in the previous step. 

Then, you want to also take a look at the section regarding the database: 

```python
# Database config
DB_HOSTNAME = 'teamspirit.postgres.database.azure.com'
DB_PORT = 5432
DB_DBNAME = 'team_spirit'
DB_USER = 'kudosadmin'
DB_PASSWORD = 'Highsalary001'
```

Replace the database configurations with the connect credentials you actually have as a PostgreSQL database.

After replacing all of the configuration files, we can now proceed to going into the next step. 

### Installation [Local Development]

TODO: Add local running tutorial

### Installation [Online Deployment]

TODO: Add Azure tutorial or docker tutorial

---
## Usage
(After installing the app)

An admin of the workspace can:
1. Customize Corporation Values:
   1. Send `/kudos_customize` in the chat
   2. 
2. View other employees' stats:
   1. Send `/kudos_overview ` in the chat
   2. 

Any user in the workspace can:
1. Send Kudos:
   1. Send `/kudos` in the chat. A window should be popped up
   2. Select recipients (one or multiple)
   3. Select corporation values associated with the kudos
   4. Type messages to the recipients, along with reasons for the kudos
   5. Select if announce this kudos publicly in this channel, and if notify recipients with direct message this kudos. 
<div style="text-align:center">
  <img src="./images/kudos_window.png" alt="Kudos Window" width="70%">
</div>

---
## Project Structure

Outline the structure of the project. Describe the purpose of each major directory and important files. This section provides a roadmap for developers to navigate the codebase.

This project can mainly be divided into 3 parts, in the order of the dataflow: Slack, Backend and database

### Slack

### Backend

### Database
This section introduces the design of our database component. We choose to use Microsoft Azure to host our database and PostgreSQL as our main language. We will introduce below the design of our tables and the functionalities we currently support 
#### Table Design
To support multiple workspaces, we choose to create a new *schema* for each workspace. For each schema, we have the following tables and constraints: 

##### 1. Table: `users`

- **Columns:**
  - `slack_id` (VARCHAR(20), Primary Key): Unique identifier for Slack users.
  - `name` (TEXT): Name of the user.

##### 2. Table: `channels`

- **Columns:**
  - `id` (VARCHAR(20), Primary Key): Unique identifier for channels.
  - `name` (TEXT): Name of the channel.

##### 3. Table: `messages`

- **Columns:**
  - `id` (VARCHAR(50))
  - `time` (TIMESTAMP): Timestamp of the message.
  - `from_slack_id` (VARCHAR(20), Foreign Key): References `users` table for sender.
  - `to_slack_id` (VARCHAR(20), Foreign Key): References `users` table for recipient.
  - `channel_id` (VARCHAR(20), Foreign Key): References `channels` table for the channel.
  - `text` (TEXT)

- **Primary Key:**
  - Composite key on `(id, from_slack_id, to_slack_id)`.

##### 4. Table: `corp_values`

- **Columns:**
  - `id` (SERIAL, Primary Key): Auto-incremented identifier.
  - `corp_value` (TEXT): Corporate values.

##### 5. Table: `kudos`

- **Columns:**
  - `message_id` (VARCHAR(30), Primary Key): Unique identifier for the kudos message.
  - `corp_value_id` (INTEGER, Foreign Key): References `corp_values` table.

**Note:**
- Foreign key constraints are established for referential integrity.
- Appropriate actions on delete (`NO ACTION`, `CASCADE`) are specified based on the relationships.
- Column data types and constraints are provisionally set; consider adjustments based on specific requirements and constraints.
- Every id except the id for `copr_values` is generated by slack and is unlikely to collide. The id for `corp_values` is automatically generated by a sequence. 
- The primary key of `messages` is set to a couple since we want to enable multiple recipients.


#### Code Design
1. To establish a connection with our database, use the `get_DAO()` function available in `__init__.py`. This practice ensures the prevention of creating multiple connections to our database.

2. The `DAObase` is an interface that any Data Access Object must adhere to. For specific behaviors expected from a `DAObase` instance, please refer to the documentations in `main/database/dao_base.py`.

3. The `DAOPostgreSQL` class is an implementation of the `DAObase` interface using PostgreSQL. It is very important to modify the default parameters within the `DAOPostgreSQL.__init__` with your individual account information after setting up your Azure account.

4. If there is necessary modifications to the database design, make the required changes in `init.sql` file and remember to also change relevant sections of `dao_psql.py`. This ensures consistency between the database design and its corresponding implementation.

## Contributing

Explain how others can contribute to the project. Include information about the contribution process, coding standards, and any guidelines for submitting issues or pull requests.

### Database 
1. Multiple injections in the functions of DAOPostgreSQL stem from unforeseen behaviors in the _select_schema helper functions. Invoking this helper function tends to induce instability in the connection to Azure, leading to prolonged query times and potential non-responsiveness. A team member attempted to address this issue by committing the current session after selecting the schema; however, this solution fails to pass the pytest.

2. Add an organization goal component to or project. It should behave like company values, but its cope is only restricted in small teams, and they might be more frequently changed by new goals. Think of them as short term tasks. Admins of a workspace/channel should be able to modify them just like company values. 

3. Enhance the robustness of the code by addressing additional edge cases and unexpected behaviors triggered by unusual inputs or connection instability. This proactive approach will contribute to a more resilient and reliable system, capable of handling diverse scenarios effectively.

## Testing

Presently, our testing framework exclusively comprises unit tests for the database. Each test involves the creation and subsequent teardown of a new schema. It's crucial to note that these tests address only the fundamental aspects of the functionalities; they lack comprehensiveness. Nevertheless, the success of these tests is a prerequisite before implementing any modifications to the database components.

To streamline the testing process, a team member has configured GitHub Actions to automatically run these tests whenever a new push is made to the main branch. This automation ensures continuous validation of the database functionalities, contributing to the overall reliability of our system.

## Deployment

Provide guidance on deploying the project to production. Include any specific configurations or considerations for deployment environments.

## Technologies Used

List the technologies, frameworks, and tools used in the project. This section helps developers understand the tech stack.

## License

Specify the project's license. This informs future developers about the terms under which they can use, modify, and distribute the project.

## Acknowledgments

Express gratitude to individuals or organizations that contributed to the project. This can include mentions of libraries, tools, or resources used.
