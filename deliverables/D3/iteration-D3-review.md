
# 42 Getting Employed

[//]: # ( > _Note:_ This document is meant to be written during &#40;or shortly after&#41; your review meeting, which should happen fairly close to the due date.      )

[//]: # ( >      )

[//]: # ( > _Suggestion:_ Have your review meeting a day or two before the due date. This way you will have some time to go over &#40;and edit&#41; this document, and all team members should have a chance to make their contribution.)


## Iteration XX - Review & Retrospect

 * When: November 6, 2023
 * Where: Online Zoom Meeting 

 * The recording link is here: 

 * https://utoronto.zoom.us/rec/share/jJo7lJWrfT64yPBoxLF9JdbhaLhejLjHRVNA6Y_6AcHYIqjjdiWOdhwks__RIkvV.RrkGAJLFdz6Uuqya?startTime=1699309966000
 * Password: 0&%7$Si0Ge

## Process - Reflection


#### Q1. What worked well

[//]: # (List **process-related** &#40;i.e. team organization and how you work&#41; decisions and actions that worked well.)

[//]: # ( * 2 - 4 important decisions, processes, actions, or anything else that worked well for you, ordered from most to least important.)

[//]: # ( * Give a supporting argument about what makes you think that way.)

[//]: # ( * Feel free to refer/link to process artifact&#40;s&#41;.)

---
 * The team maintained effective communication channels, allowing members of each component to engage in frequent and transparent exchanges. We had frequent Slack and WeChat group discussions, we also met regularly, at least twice a week in-person to discuss the progress of our project. 
 * The backend development process proceeded seamlessly due to the user-friendly nature of Slack's built-in API, which facilitated efficient integration and communication.
 * The team leader demonstrated exceptional responsiveness and attentiveness, displaying a deep understanding of the project's progress. They effectively established clear expectations, set realistic deadlines, and allocated tasks judiciously. The task assignment page in Notion was updated frequently and set in a straightforward way.

#### Q2. What did not work well

[//]: # (List **process-related** &#40;i.e. team organization and how you work&#41; decisions and actions that did not work well.)

[//]: # ( * 2 - 4 important decisions, processes, actions, or anything else that did not work well for you, ordered from most to least important.)

[//]: # ( * Give a supporting argument about what makes you think that way.)

[//]: # ( * Feel free to refer/link to process artifact&#40;s&#41;.)

---
 * The process of setting up the online database proved to be challenging, particularly with Microsoft Azure, which presented complexities during the setup phase. Additionally, inadequate configuration can lead to significant costs. Moreover, there was no financial support available from our partner or the course staff for students to allocate towards this expense.
 * Locating a suitable Linux container for setting up Docker proved to be a challenging task due to the complexity in identifying an optimal option.
 * Hosting the Linux container on Microsoft Azure also proved to be a challenging task, as the amount of configurations that are needed for the service is tremendous.
 * Our initially proposed method for integrating additional workspaces into our database has encountered an unexpected failure. Consequently, we are implementing a temporary workaround to sustain the program's functionality, concurrently conducting a thorough investigation to identify the root cause of the issue.
 * As development progressed, the process of installing our Slack bot to other workspaces required sophisticated knowledge on hosting a web server with a PHP script, which makes our tech stack even more complex. 

#### Q3(a). Planned changes

[//]: # (List any **process-related** &#40;i.e. team organization and/or how you work&#41; changes you are planning to make &#40;if there are any&#41;)

[//]: # ( * Ordered from most to least important, with supporting argument explaining a change.)

---

 * Fix the bugs and unexpected instabilities of the program due to merging our components together. 
 * The migration of the application from Slack to alternative platforms such as Microsoft Teams and Discord to enhance communication and collaboration capabilities within the team. This is one of the required features that our partner is willing to implement. 
 * We are planning to extend the application's functionality by implementing various features, which may include but are not limited to:

  1. Parsing command-like texts for improved user interaction.
  2. Displaying basic statistics for specific groups of users.
  3. Incorporating a feature for setting and tracking organizational goals.
  4. Enabling the capability to send text feedback via email.

- If time and resources allow, there is consideration for publicly hosting our application.



#### Q3(b). Integration & Next steps

[//]: # (Briefly explain how you integrated the previously developed individuals components as one product &#40;i.e. How did you combine the code from 3 sub-repos previously created&#41; and if/how the assignment was helpful or not helpful.)

[//]: # ( * Keep this very short &#40;1-3 lines&#41;.)

---

- The database team and the backend team added a logger message for each function to record the behavior of the function, in response to merging the logging subteam. 
- We attempted to link the components between the backend team and the database team by starting up the bot using a centralized script. 

## Product - Review

[//]: # (#### Q4. How was your product demo?)

[//]: # ( * How did you prepare your demo?)

[//]: # ( * What did you manage to demo to your partner?)

[//]: # ( * Did your partner accept the features? And were there change requests?)

[//]: # ( * What were your learnings through this process? This can be either from a process and/or product perspective.)

[//]: # ( * *This section will be marked very leniently so keep it brief and just make sure the points are addressed*)

---
* We listed out an outline of things that we want to mention and also thought about what kind of questions that our partner might ask and how we were going to answer them.

* We managed to show almost all the features of our program, except some minor issues.

* Our partner accepted the features, and proposed several features that we could implement in the future, including but not limited to: adding organization goals, parsing commands instead of popping up a window every time a kudos is requested, etc.

* That before presenting, we need to ensure that everything works, and run a quick demo without our partner probably an hour before the demo, so that when demonstrating our program, no surprising issues would arise.

* After the demo, we had a clear understanding on the next steps of our deployed product and how we can improve. With that being said, we are now still working on enhancing our Slack bot by moving towards the requirements stated. 