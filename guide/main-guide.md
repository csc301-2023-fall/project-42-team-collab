# Team Collab / Team Spirit

This guide serves as a comprehensive guide for future developers and users

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started \[General Usage\]](#getting-started-general-usage)
- [Getting Started \[Developer\]](#getting-started-developer)
  - [Prerequisites](#prerequisites)
    - [General requirements](#general-requirements)
    - [Local Development](#local-development)
    - [Online Deployment](#online-deployment)
  - [Settings before deployment](#settings-before-deployment)
    - [Slack developer portal](#slack-developer-portal)
    - [config.py](#configpy)
    - [install.php](#installphp)
  - [Installation \[Local Development\]](#installation-local-development)
    - [Installation using Docker](#installation-using-docker)
    - [Installation without using Docker](#installation-without-using-docker)
  - [Installation \[Online Deployment\]](#installation-online-deployment)
    - [Docker Hub](#docker-hub)
    - [Microsoft Azure](#microsoft-azure)
    - [\[Optional\] Setting up release of the project to be installed in other workspaces](#optional-setting-up-release-of-the-project-to-be-installed-in-other-workspaces)
  - [Adding new commands to the bot](#adding-new-commands-to-the-bot)
- [Usage](#usage)
  - [Admin Commands](#admin-commands)
    - [Customize Corporation Values](#customize-corporation-values)
    - [Customize Corporation Values](#customize-corporation-values-1)
    - [Remove Customized Corp Values](#remove-customized-corp-values)
    - [View other employees' stats](#view-other-employees-stats)
  - [General Commands](#general-commands)
    - [Send Kudos (Using the GUI)](#send-kudos-using-the-gui)
    - [Send Kudos (Using command parsing)](#send-kudos-using-command-parsing)
- [Managing Members](#managing-members)
- [Project Structure](#project-structure)
  - [Backend](#backend)
    - [main.py](#mainpy)
    - [team\_spirit.py](#team_spiritpy)
    - [design.py](#designpy)
  - [Database](#database)
    - [Table Design](#table-design)
      - [1. Table: `users`](#1-table-users)
      - [2. Table: `channels`](#2-table-channels)
      - [3. Table: `messages`](#3-table-messages)
      - [4. Table: `corp_values`](#4-table-corp_values)
      - [5. Table: `kudos`](#5-table-kudos)
    - [DAO Design](#dao-design)
- [Contributing](#contributing)
  - [Slack Back End](#slack-back-end)
  - [Documentation](#documentation)
  - [Database](#database-1)
  - [Deployment](#deployment)
- [Testing](#testing)
- [Acknowledgments](#acknowledgments)
  
---
## Introduction

This project aims to build an app that works smoothly with Slack (might be able to support Microsoft Teams later on), promoting teamwork by recognizing achievements (kudos). The target users for this product are workspaces with fewer than 2000 people. 

The product deployed will be a bot that is integrated into Slack, allowing users to interact with the bot to give kudos (acknowledgement messages) to another user, with an attached message and chosen attached "company values", which are defined as values (keywords) that the Slack workspace wants to achieve. 

Here's a quick introduction video that one of our group members has filmed. It should give you a pretty basic overview of what our bot is able to do in a general perspective, without getting into too much complicated details.  

https://youtu.be/6g5cdE2szyk

---
## Features

1. Acknowledge colleagues for their work done with kudos, and align each kudos with one or more corporate values.
2. Customize (add / remove) Corporate Values for a workspace. The project supports permission check, only **workspace admin, workspace owner, and workspace primary owners** of a workspace is permitted to modify corporation values. You can learn more about Slack roles in this page: [Types of roles in Slack](https://slack.com/help/articles/360018112273-Types-of-roles-in-Slack). For our project, we will only be concerned about Workspace Primary Owner, Workspace Owners, Workspace Admins, and Full members.
3. Analyze an employee's statistics, including the number and values for the kudos received within a specified time frame. Only admins are permitted to view others' stats. 

---
## Getting Started [General Usage]

Before any user can start to use the project product, we need to ensure that the section [Getting Started [Developer]](#getting-started-developer) is being read by someone, and has an active server started and running. This is crucial for the bot work. 

Then, with that being done, under the [Installation [Online Development]](#installation-online-deployment) section, you should be able to obtain an "Installation link" to your workspace. Simply click on that link and select the workspace you want it to be installed in, and in a while, the bot should be installed to your workspace. 

With the bot installed in your workspace, you can now proceed to the [Usage](#usage) section, which documents some of the simple things you can do with our bot. 

---
## Getting Started [Developer]

In this part, we will guide you through the methods to be able to recreate what we have, please make sure you follow this guide as much as possible. 

### Prerequisites

Depending on your preference, you can start the project either locally, or deployed to the cloud. With these choices, we offer two sets of prerequisites. 

#### General requirements

- A valid Slack Development Account, which needs to be configured to run our bot. You should have a Slack Developer account if you have a regular Slack account. If you don't have a valid account, you can register a valid account here: [Slack API](https://api.slack.com/)
- A PostgreSQL Database that you have full control over. The ones used in development by the project is provided Microsoft Azure. You are also welcome to use a local database, as long as you have methods of connecting to it. 
- Clone this repository to any of your local development environments. 

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

If everything is right, you should now enter the app's "basic information" page, which allows you to configure certain information about your bot, and also extract some of the **IMPORTANT INFORMATION** to use the bot with. Due to time constraints, some of the information in our `manifest.yml` might not be fully polished, so you might have to perform some updates in the information section of the bot.  

Scroll down in this page to the "App Credentials" section, and you should see the following: 

![App credentials](images/app_credentials.png)

Within these fields, take note of the "**Signing Secret**", as we will use it later in `config.py`. 

Also, you want to take note of "**Client ID**" and "**Client Secret**", as we will use it later in `install.php`.

Then, scroll down more, and you will find "App-Level Tokens". If there isn't any entries in there, simply click "Generate Token and Scopes", and select the scopes that it needs by referring to the picture below. The tokens that you need are: "connections:write, authorizations:read, app_configurations:write". 

Note: This set of token permissions isn't tested thoroughly, and might contain extra permissions needed for the bot to work. 

![App level tokens](images/app_level_tokens.png)

After creating, you should be able to click the name of the newly created App Token, and obtain a "**Token**", as shown below (the one that begins with "xapp-x-xxx...").

![App level token value](images/app_level_token_value.png)

Note down the value of this app token as well. 

Under the "Install App" sub-menu on the left, as shown in the below figure, you should be able to obtain a "**Bot Token**". Note it down as well. The bot token should begin with "xoxb-xxxx..."

![Bot token](images/bot_token.png)

With all of these information available, we can now proceed to the configurations of our bot.

#### config.py

Within `main/config.py`, there are a few fields to look out for: 

```python
# Connectivity configurations
SLACK_BOT_TOKEN = "xoxb-5933772890579-5945241825189-YUY5SWx1bvaMp3opBV8qeTq0"
SLACK_SIGNING_SECRET = "48928ff7a9457f0f4264af506b5b6bcf"
SLACK_APP_TOKEN = "xapp-1-A05TW1NB0CB-5948193295891-720a67e31f92b0c273bbe5ff3525501b3cdf79421f7aa4143d61ba6cc9d08c53"
```

Within `config.py`, you want to replace the values that we have in there with the new values that you have obtained in the previous step. The values shown above are the current values that we are using for our bot. 

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

Note: The database credentials we have shown above will be unavailable after **January 1st, 2024**. 

After replacing the details of the configuration files, we can now proceed to going into the next step.

#### install.php

Under `main/setup_script/install.php`, there are a few fields to be updated as well.

```php
$client_id = "5933772890579.5948056374419";
$client_secret = "8d1d5b9e81638194f42e8eba4daec9c4";
```

You want to update these two lines with the information that you have found in the previous step ([Slack Developer Portal](#slack-developer-portal)) as well.

Then, simply save the file and continue on.

### Installation [Local Development]

#### Installation using Docker

After setting up all the required configurations above, you should be able to look into `main/docker/docker_readme.md`, and execute `build_docker_and_run.sh` or `build_docker_and_run.bat` to start up the bot. 

A successful start up of the bot should look something like this: 

![local startup](images/local_startup.png)

The indication that the bot is up and running is the line: 

`⚡ Bolt app is running!`. 

#### Installation without using Docker

If you do not want to use Docker, as instructed above, you also have the choice of running it on Python directly. 

To do this, you want to change your working directory to the `main` folder. Then, you want to execute `pip install -r requirements.txt`. 

Then, you can execute `python ./main.py` within the same directory, and you should able to see similar results as the Docker local deployment, as shown in the pictures below: 

![pip install](images/pip_install.png)

![local python startup](images/local_python_startup.png)

### Installation [Online Deployment]

Note: The following part contains a lot of setup on Microsoft Azure and Docker Hub, as that is the Docker container hosting service that we have chosen for our project. 

**Here is a guide that I have recorded, which provides all of the details you need to know to setup online deployment:** 

https://youtu.be/tXMTvcuYfSA

Please check the video description for the timestamps for the setup of each different component. 

#### Docker Hub

As mentioned by the prerequisites, you should have a valid Docker Hub account [https://hub.docker.com/](here). 

Now, with your Docker Hub account, you want to create a repository that is **exactly** named `team_spirit`, as shown in the figure below. (You may also choose to create repository names that are different, but that requires updating a lot of the scripts we have written)

![docker hub](images/docker_hub.png)

For our project, we have decided to use a **private** repository, so we recommend you to do the same. 

After creating the repository, you should see the following page by navigating into your repository. 

![docker repository](images/docker_repo.png)

On the upper right corner, you will be notified on how to push your current working image to Docker Hub. 

More specific guide on how to push to your Docker Hub is written in `docker_readme.md`. A hyperlink is here: [How to push a local Docker image to Docker Hub?](../main/docker_readme.md#how-to-push-a-local-docker-image-to-docker-hub)

After everything is setup, you should be able to push your local image to your Docker Hub, which completes this step. 

You should be able to verify this by clicking into the repository and seeing that under "Tags", there is a "latest" Tag which is pushed very recently. 

#### Microsoft Azure

With all the Docker setup done, you can now create a new "Docker Container App" on Microsoft Azure. The setup for this part varies a lot, and is very hard to be covered in this guide, so I recommend you to look up a tutorial on YouTube or Google to create a new Docker Container App.

Please refer to the guide linked in [Installation [Online Deployment]](#installation-online-deployment) if you can't find a tutorial that works. The timestamp for this part is at 06:07, 22:22, and 27:05. 

With a Docker Container App created, one of the main settings that you want to ensure is: 

![azure docker settings](images/azure_docker_settings.png)

With all these being done, you can simply start up the Docker Container and the bot should be running. 

#### [Optional] Setting up release of the project to be installed in other workspaces

This part is optional, but it is necessary if you plan to distribute your Slack bot to multiple workspaces. 

Please refer to the guide linked in [Installation [Online Deployment]](#installation-online-deployment) if you think setting this part up is difficult. This part is at timestamps 11:54 and 15:21. 

The main goal of this part is to setup a PHP Web Server that runs an automated installation script, which triggers [Slack's OAuth Request](https://api.slack.com/authentication/oauth-v2) and installs the bot to the corresponding workspace. 

The main goal here is to create a web server that can deal with HTTP GET and POST requests, and deal with them using an installation script. To complete this goal, I have utilized Microsoft Azure's web server, with a simple installation script provided in `main/setup_script/install.php`. 

Please refer to the guide linked in [Installation [Online Deployment]](#installation-online-deployment). The timestamp for this part is at 11:54 and 15:21.

You want to ensure that the script is available on the Web Server (HTTPS needed), and can be accessed publicly. 

With all that being done, the following is a figure of how it is laid out in our current web server. 

![web server](images/web_server.png)

The home page of our web server is `wwwroot`, and I have created a directory called `install` and placed the file `install.php` in there.

With these being done, you should now have access to your script through a link, something like: `https://team-spirit.azurewebsites.net/install/install.php`. 

Then, you want to head back once more to Slack Developer Portal, and under "OAuth & Permissions", add the redirect URL as the link to your installation script, as shown below. 

![redirect_url](images/redirect_url.png)

With these setup, you should now be able to use the link provided by "Manage Distribution" under the Slack Developer Portal to install your bot to other workspaces as well. 

![manage distribution](images/manage_distribution.png)


### Adding new commands to the bot
First head to [Slack Developer Portal](https://api.slack.com/apps) page, and click on the bot that you just added. 

![Click the bot](images/click_your_app.png)

Then click "Slash Commands" on your left under "Features"
![CLick Slash Commands](images/add_command_window.png)

Click "Create New Command" button
![Click New Command](images/create_new_command.png)

1. Enter the name of your new command (take note of this name)
2. Add description about this new command
3. (Optional) Add hint about any parameter about this command
4. (Optional) If your Slash command needs to deal with parsing the input that has mentions about users or channels, tick the "Escape channels, users, and links" option, as that allows the input received to escape specific information for you to use. 
5. Click "Save"

![Guide add new command](images/guid_create_command.png)

After adding a command here, be sure to refer to [team_spirit.py](#teamspiritpy) to understand how to add a "command listener" so that your command actually works!

A "command listener" is of the following format: 

```python
@app.command("/kudos")
def open_modal(ack, command, client, payload) -> None:
```

Where you can replace the `command_name` in `@app.command("/<command_name>")` to define the function that will handle this Slash command request when invoked by a user. 

---
## Usage
This section will focus on the general usage by a regular (non-developer) user, after the app is installed in your workspace.

### Admin Commands
#### Customize Corporation Values:
   1. Send `/kudos_customize` in any chat box, then a window like the following picture shows will pop-up. Note that this command also supports prefilling the value(s) you typed in the command, e.g. `/kudos_customize GoodTeamwork Innovation`.
   ![kudos customize window](images/kudos_customize.png)
   2. Then, you can type in the company value that you want to add to the workspace. 
   3. If this succeeds, you should receive a private message from our Slack Bot saying that the value was added (for confirmation).
#### Remove Customized Corp Values:
   1. Send `/kudos_corp_value_remove` in any chat box, then a window like the following picture shows will pop-up. Note that this command also supports prefilling the value(s) that you have added to the workspace, e.g. `/kudos_corp_value_remove GoodTeamwork Innovation`.
    ![kudos corp value remove window](images/corp_value_remove_window.png)
   2. Select the value that you want to remove, and click "Remove". Note you can choose multiple values to remove at once.
   3. If this succeeds, you should receive a private message from our Slack Bot saying that the chosen values were removed (for confirmation).
   4. Be aware that if you send kudos to someone and include a corporate value that has been deleted, that particular value will be removed from the kudos. Furthermore, if all the corporate values in your kudos have been removed, then the entire kudos will also be deleted. 
#### View other employees' stats:
   1. Send `/kudos_overview` in the chat, and the following window will pop-up.  
   ![kudos overview window](images/kudos_overview.png)
   2. Select the user and the time frame that you want to view kudos for, and click "View". The results should replace this window and display kudos information about that user within the specified time frame. 

### General Commands
#### Send Kudos (Using the GUI):
   1. Send `/kudos` in the chat.
   2. Select recipients (one or multiple)
   3. Select corporation values associated with the kudos
   4. Type messages to the recipients, along with reasons for the kudos
   5. Select if announce this kudos publicly in this channel, and if notify recipients with direct message this kudos. 

![kudos window image](images/kudos_window.png)

#### Send Kudos (Using command parsing):
   1. Send `/kudos message [@person1] [@person2] [@...] [$value1$] [$value2$] [$value...$] message`
   2. In the pop-up window, you should see that the recipients are pre-filled with the `@mentions` of users that you have typed in the command. 
   3. You should also see that the values that you have assigned using this command with `$value$` are automatically filled. 
   4. You should also see that any content that is in the command that is not a `@mention` nor a `$value$` becomes a part of the actual message. 

   For example, I can execute `/kudos Hi this is Ray, saying thanks to @Will Will $Good Teamwork$. Very cool`. Then, these information will be automatically filled, and the message pre-filled will become: "Hi this is Ray, saying thanks to Will. Very cool"

## Managing Members

If you are a workspace primary owner, you can enter the "Manage Members" page to customize who should have access to the admin functions. 

![member management](images/member_management.png)

Then, it should bring you to a page that allows you to set the account types of each member in your workspace: 

![change member type](images/change_member_type.png)

---
## Project Structure

Outline the structure of the project. Describe the purpose of each major directory and important files. This section provides a roadmap for developers to navigate the codebase.

This project can mainly be divided into 3 parts, in the order of the dataflow: Slack, Backend and database


### Backend
This section introduces the basic outline and structure of our Bot. 

#### main.py

The main entry point to all of our code is `main.py`, which imports all the relevant modules and starts up our bot. It doesn't provide much functionality, but it involves setting up the logger so that we have logs to review when something goes wrong.  

The logging configurations can be found in `main/logging.conf`. Which allows you to change the logging level. By default, it is at INFO, which prints out most information when functions are invoked.  

#### team_spirit.py

`team_spirit.py` is our bot's main code, which involves calling all the relevant function in our database and creating listeners for events that are passed by Slack's API. 

Since we have too many functions in `team_spirit.py`, I will just bring a quick overview on how we laid out the file. 

Within the file, you should be able to see numerous dividers like: 

```python
# #############################################################################
# COMMAND HANDLER: /kudos
# #############################################################################
```

These dividers split our bot into multiple sections, each section deals with one specific command that is invoked by Slack's API. For example, the first function under the `/kudos` handler section is labelled: 

```python
@app.command("/kudos")
def open_modal(ack, command, client, payload) -> None:
```

This is the main function that will be invoked when a user types in `/kudos` in their chat box. This is also known as a "command listener" function, which will be invoked when an event is being heard. 

This function then calls functions that interact with the database and functions that interact with `design.py`, which will be described later. 

The second function under the `/kudos` handler section is: 

```python
@app.view("kudos_modal")
def handle_submission(ack, body, view, client, payload) -> None:
```

This is a "view listener" function, as it is called when the "view" with the "callback_id" of "kudos_modal" is being submitted. 

The command `/kudos` opens up a "view" (a pop-up window), with specified attributes like "callback_id", which is used to interact with our "view listener" function. 

All of the views that we have used in this project are JSON-like Python dictionaries, as you can see in `design.py`. 

The rest of the functions in `team_spirit.py` follows a similar logic, where each of them has a "view listener" and a "command listener", sometimes with specific event listeners as requested by Slack.

#### design.py

This file stores all of the "view" components (JSON dictionaries) that we will use to generate the pop-up windows that will appear when we invoke a specific command.

There are numerous fields that can be filled within these modules, but it is extremely hard to cover all of them. 

You can learn more about how we setup the Modal views using [Slack's Block Kit](https://api.slack.com/tutorials/intro-to-modals-block-kit) and [Slack's Blocks](https://api.slack.com/reference/block-kit/blocks) in their respective hyperlinks.

### Database
This section introduces the design of our database component. We choose to use Microsoft Azure to host our database and PostgreSQL as our main language. We will introduce below the design of our tables and the functionalities we currently support:

#### Table Design
To support multiple workspaces, we choose to create a new *schema* for each workspace. For each schema, we have the following tables and constraints: 

You can view a sample of this schema by checking into `main/database/init.sql`. This is the script that we use to initialize a new workspace's database relations. 

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
  - `message_id` (VARCHAR(30)): Unique identifier for the kudos message.
  - `corp_value_id` (INTEGER, Foreign Key): References `corp_values` table.
- **Primary Key:**
  - Composite key on `(message_id, corp_value_id)`.

**Note:**
- Foreign key constraints are established for referential integrity.
- Appropriate actions on delete (`NO ACTION`, `CASCADE`) are specified based on the relationships.
- Column data types and constraints are provisionally set; consider adjustments based on specific requirements and constraints.
- Every id except the id for `corp_values` is generated by slack and is unlikely to collide. The id for `corp_values` is automatically generated by a sequence. 
- The primary key of `messages` is set to a couple since we want to enable multiple recipients.


#### DAO Design
1. To establish a connection with our database, use the `get_DAO()` function available in `__init__.py`. This practice ensures the prevention of creating multiple connections to our database.

2. The `DAObase` is an interface that any Data Access Object must adhere to. For specific behaviors expected from a `DAObase` instance, please refer to the documentations in `main/database/dao_base.py`.

3. The `DAOPostgreSQL` class is an implementation of the `DAObase` interface using PostgreSQL. It is very important to modify the default parameters within the `DAOPostgreSQL.__init__` with your individual account information after setting up your Azure account.

4. If there is necessary modifications to the database design, make the required changes in `init.sql` file and remember to also change relevant sections of `dao_psql.py`. This ensures consistency between the database design and its corresponding implementation.

## Contributing

The following section is some TODOs that we have yet to complete as a part of our project, but we will provide general guidelines and description to these issues. 

### Slack Back End
1. Our current Bot's home page is completely blank, but it can be setup by using Slack's block kit relatively easily. Completing the Bot's home page allows for a new user to quickly grasp the usage of our bot, hence making it more accessible by users. 

### Documentation
1. Our current GitHub page doesn't have a wiki page that documents everything in an organized manner. Mostly, we rely on comments that is written directly on the code file, not providing an actual documentation for them, which may cause some issues in terms of communicating.

### Database 
1. Multiple injections in the functions of DAOPostgreSQL stem from unforeseen behaviors in the `_select_schema` helper functions. Invoking this helper function tends to induce instability in the connection to Azure, leading to prolonged query times and potential non-responsiveness. A team member attempted to address this issue by committing the current session after selecting the schema; however, this solution fails to pass the pytest.

2. Add an organization goal component to or project. It should behave like company values, but its cope is only restricted in small teams, and they might be more frequently changed by new goals. Think of them as short term tasks. Admins of a workspace/channel should be able to modify them just like company values. 

3. Enhance the robustness of the code by addressing additional edge cases and unexpected behaviors triggered by unusual inputs or connection instability. This proactive approach will contribute to a more resilient and reliable system, capable of handling diverse scenarios effectively.

### Deployment
1. Notice that currently, our Slack bot is deployed using "Socket mode", which is only recommended as a way of deploying the bot if only used for development purposes. If possible, you can setup your own HTTP server hosting at a domain, which allows you to redirect all sources of HTTP Requests to our bot using Slack's BOLT API. If you plan to distribute the bot into public, this is a necessary step, as socket direct connections are often insecure. 

2. The project was originally planned to be also used by Microsoft Teams. However, as the API given by Slack is very limited to only working with Slack, we have limited our project's capabilities to only work with Slack. Furthermore, the APIs that we can use to communicate with Teams is extremely different with what we have currently. If we want to support Teams in the future, the best we can do is probably to reuse the same structure of our Slack bot and create a new project on it. 

## Testing

Presently, our testing framework exclusively comprises unit tests for the database. Each test involves the creation and subsequent teardown of a new schema. It's crucial to note that these tests address only the fundamental aspects of the functionalities; they lack comprehensiveness. Nevertheless, the success of these tests is a prerequisite before implementing any modifications to the database components.

To streamline the testing process, a team member has configured GitHub Actions to automatically run these tests whenever a new push is made to the main branch. This automation ensures continuous validation of the database functionalities, contributing to the overall reliability of our system.

You may modify the GitHub actions files stored under `.github/workflows`. 

The file named `build_and_test.yml` configures Pytest and runs them on a Linux machine.

The file named `docker-image.yml` uses Docker to build an image and push to our Docker Hub repository as stated in [Docker Hub](#docker-hub). Notice that I have used a lot of replacement fields like `${{ secrets.DOCKERHUB_USERNAME }}`. These are known as GitHub repository secrets, and you can learn more about them here: [Using secrets in GitHub actions](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)

## Acknowledgments

Special thanks to the University of Toronto's CSC301 Teaching Team, which gave us the idea of this project! 

Also, thanks a lot for you to be reading until now! 
