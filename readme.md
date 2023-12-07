# Slack App / Getting Employed

## D5 Handoff Video & Quick introduction

We have filmed a simple video that walks through our product briefly and the features it currently supports, please take a look before reading through the guides below. 

https://youtu.be/6g5cdE2szyk

## [Main Guide](developer-guide/main-guide.md)

A full and complete guide to setup and use the project as a regular user and a developer is available by the hyperlink above. 

Please read through this guide, it should be able to clear out a lot of your confusions.

## Partner Intro

[//]: # (* Include the names, emails, titles, primary or secondary point of contact at the partner organization)
[//]: # (* Provide a short description about the partner organization. &#40;2-4 lines&#41;)

- Partner Information: Team Collab
- Primary Contact: David Jorjani (d.jorjani@gmail.com)

David is our primary contact, and he has an idea of starting up a Slack Application that will help in the management of teams if they are using Slack. 

He also has the idea of also deploying a similar bot to Microsoft Teams in the future. 

## Description about the project

[//]: # (* Provide a high-level description of your application and it's value from an end-user's perspective)
[//]: # (* What is the problem you're trying to solve? Is there any context required to understand **why** the application solves this problem?)

Our application is a Slack Bot that will help in management of teams in multiple ways. The bot will have multiple features that will help in the management of teams (which can be extended easily). 

The problem we are trying to solve is to create a "helper" that can help manage the teams in Slack better. 

For example, one feature that we are intending to complete is the feature to send a "kudos" to another user, which is like a "thank you" message. 

This command can be used by Managers of a certain work space to ensure that an employee does receive acknowledgements when they do something beyond expectations.

## Features

### Admin Commands
- **Customize Corporation Values**:
  - Use `/kudos_customize` to add new corporate values.
  - Supports prefilling typed values for quick adding.
  - After adding, receive confirmation from the Slack Bot.

- **Remove Customized Corp Values**:
  - Use `/kudos_corp_value_remove` to delete existing values.
  - Supports multi-selection for bulk removal.
  - Supports prefilling typed values for quick removal.
  - Includes safeguards to ensure kudos integrity with value updates.

- **View Employee Stats**:
  - Use `/kudos_overview` to see kudos statistics for employees.
  - Select users and time frames for detailed insights.

### General Commands
- **Send Kudos (GUI)**:
  - Initiate with `/kudos`.
  - Choose recipients, values, and compose messages.
  - Options for public announcement and direct messaging.

- **Send Kudos (Command Parsing)**:
  - Use command syntax for quick sending.
  - Pre-fill recipients, values, and messages in the pop-up window.

### Managing Members
- Workspace owners can manage member access to admin functions.
- Interface for changing account types of workspace members.

## User Interface
- The app provides intuitive GUIs for all functionalities.
- Screenshots in the app guide shows the following, referenced [Main Guide#usage](developer-guide/main-guide.md#usage):
  - Customization window for adding/removing corporate values.
  - Overview window for viewing employee kudos.
  - Kudos sending window and member management interface.
  - Corporate value removal window with multi-selection.

## Instructions

[//]: # (* Clear instructions for how to use the application from the end-user's perspective)
[//]: # (* How do you access it? For example: Are accounts pre-created or does a user register? Where do you start? etc. )
[//]: # (* Provide clear steps for using each feature described in the previous section.)
[//]: # (* This section is critical to testing your application and must be done carefully and thoughtfully.)

- The Slack App will be added to the workspace by the workspace admin, we will provide a link to add the app to their workspace. 
- After the Slack App is added to the workspace, any user can just invoke the `/kudos` command in any message box available. 
- The user will also be able to customize more company values, by typing `/kudos_customize`, or remove existing customized corporate values, by typing `/kudos_corp_value_remove`, that they want to use for their workspace in the pop-up window.
- The user will also be able to view the kudos statistics for employees by typing `/kudos_overview` in the pop-up window.
 
## Development requirements

[//]: # (* What are the technical requirements for a developer to set up on their machine or server &#40;e.g. OS, libraries, etc.&#41;?)
[//]: # (* Briefly describe instructions for setting up and running the application. You should address this part like how one would expect a README doc of real-world deployed application would be.)
[//]: # (* You can see this [example]&#40;https://github.com/alichtman/shallow-backup#readme&#41; to get started.)

Reference to the [Main Guide#getting-started-developer](developer-guide/main-guide.md#getting-started-developer) for the full guide on how to setup and run the application.

## Deployment and Github Workflow

[//]: # (Describe your Git/GitHub workflow. Essentially, we want to understand how your team members share codebase, avoid conflicts and deploys the application.)

[//]: # (* Be concise, yet precise. For example, "we use pull-requests" is not a precise statement since it leaves too many open questions - Pull-requests from where to where? Who reviews the pull-requests? Who is responsible for merging them? etc.)
[//]: # (* If applicable, specify any naming conventions or standards you decide to adopt.)
[//]: # (* Describe your overall deployment process from writing code to viewing a live application)
[//]: # (* What deployment tool&#40;s&#41; are you using? And how?)
[//]: # (* Don't forget to **briefly justify why** you chose this workflow or particular aspects of it!)

We will be using the following workflow for submitting amendments to our codebase:
- When we are working on a feature, we will create a new branch for that feature.
- We will then work on that feature on that branch, and then create a pull request to merge that branch into the `main` branch.
- For every pull request to be merged, we will require at least 2 reviews from any team member. After each review, the reviewer will comment on the pull request. 
- After confirming that 2 reviews have been done, any member will be able to confirm the merge and ask on Slack for a confirmation from the team.
- When everyone believes that the pull request can be merged, anyone can merge the pull request into the `main` branch.
- This will ensure that our code base will only be updated when everyone is aware of the changes that are being made.

Regarding naming conventions, we have adapted a naming convention that will be described in details in the next section. 

We will be using Docker to deploy our application:
- When testing and developing, we will run docker locally and test the application on Slack. When we call a script that deploys the docker locally, it will also allow the application to be used on Slack.
- When we are ready to deploy, we will deploy the application on a web service available online so that our bot will be online all the time.
- By using Docker, we can ensure that the application will be deployed in the same environment as the one that we are developing on, which will reduce the chances of bugs appearing when we deploy the application.


## Coding Standards and Guidelines

[//]: # (Keep this section brief, a maximum of 2-3 lines. You would want to read through this [article]&#40;https://www.geeksforgeeks.org/coding-standards-and-guidelines/&#41; to get more context about what this section is for before attempting to answer.)
[//]: # (* These are 2 optional resources that you might want to go through: [article with High level explanation]&#40;https://blog.codacy.com/coding-standards-what-are-they-and-why-do-you-need-them/&#41; and [this article with Detailed Explanation]&#40;https://google.github.io/styleguide/&#41;)

- For every commit message, we will try to follow the format of `<type>: <description>` 
- With this, we can ensure that we can easily identify the commit that introduced a certain feature. 

## Licenses 

[//]: # (Keep this section as brief as possible. You may read this [Github article]&#40;https://help.github.com/en/github/creating-cloning-and-archiving-repositories/licensing-a-repository&#41; for a start.)
[//]: # ( * What type of license will you apply to your codebase? And why?)
[//]: # ( * What affect does it have on the development and use of your codebase?)

- We will not be applying any license to our codebase, as we do not intend to make our codebase open source.
- It will not affect our codebase at all, as we will be providing our code directly to our partner.
