# Slack App / Getting Employed
> _Note:_ This document will evolve throughout your project. You commit regularly to this file while working on the project (especially edits/additions/deletions to the _Highlights_ section). 
 > **This document will serve as a master plan between your team, your partner and your TA.**

## Product Details

#### Q1: What is the product?

 > Short (1 - 2 min' read)
 * Start with a single sentence, high-level description of the product.
 * Be clear - Describe the problem you are solving in simple terms.
 * Specify if you have a partner and who they are.
 * Be concrete. For example:
    * What are you planning to build? Is it a website, mobile app, browser extension, command-line app, etc.?      
    * When describing the problem/need, give concrete examples of common use cases.
    * Assume your the reader knows nothing about the partner or the problem domain and provide the necessary context. 
 * Focus on *what* your product does, and avoid discussing *how* you're going to implement it.      
   For example: This is not the time or the place to talk about which programming language and/or framework you are planning to use.
 * **Feel free (and very much encouraged) to include useful diagrams, mock-ups and/or links**.

A Slack App that helps users to do various things, these include but not limited to:
- Send kudos using a form to a certain user
- Option to add user's alignment of company values in the kudos that are sent
- Ability to retrieve information of how much kudos are sent to a certain user and their statistics
- TODO


#### Q2: Who are your target users?

Teams working in small organizations (less than 2000 people).

#### Q3: Why would your users choose your product? What are they using today to solve their problem/need?

> Short (1 - 2 min' read max)
 * We want you to "connect the dots" for us - Why does your product (as described in your answer to Q1) fits the needs of your users (as described in your answer to Q2)?
 * Explain the benefits of your product explicitly & clearly. For example:
    * Save users time (how and how much?)
    * Allow users to discover new information (which information? And, why couldn't they discover it before?)
    * Provide users with more accurate and/or informative data (what kind of data? Why is it useful to them?)
    * Does this application exist in another form? If so, how does your differ and provide value to the users?
    * How does this align with your partner's organization's values/mission/mandate?

TODO

#### Q4: What are the user stories that make up the Minumum Viable Product (MVP)?

 * At least 5 user stories concerning the main features of the application - note that this can broken down further
 * You must follow proper user story format (as taught in lecture) ```As a <user of the app>, I want to <do something in the app> in order to <accomplish some goal>```
 * User stories must contain acceptance criteria. Examples of user stories with different formats can be found here: https://www.justinmind.com/blog/user-story-examples/. **It is important that you provide a link to an artifact containing your user stories**.
 * If you have a partner, these must be reviewed and accepted by them. You need to include the evidence of partner approval (e.g., screenshot from email) or at least communication to the partner (e.g., email you sent)

TODO

#### Q5: Have you decided on how you will build it? Share what you know now or tell us the options you are considering.

> Short (1-2 min' read max)
 * What is the technology stack? Specify languages, frameworks, libraries, PaaS products or tools to be used or being considered. 
 * How will you deploy the application?
 * Describe the architecture - what are the high level components or patterns you will use? Diagrams are useful here. 
 * Will you be using third party applications or APIs? If so, what are they?

Technology Stack

- Python as the Backend
- Slack Bolt SDK for Python as the entry point to Slack's API
- TODO as the Database entry

TODO

----
## Intellectual Property Confidentiality Agreement 
> Note this section is **not marked** but must be completed briefly if you have a partner. If you have any questions, please ask on Piazza.
>  
**By default, you own any work that you do as part of your coursework.** However, some partners may want you to keep the project confidential after the course is complete. As part of your first deliverable, you should discuss and agree upon an option with your partner. Examples include:
1. You can share the software and the code freely with anyone with or without a license, regardless of domain, for any use.
2. You can upload the code to GitHub or other similar publicly available domains.
3. You will only share the code under an open-source license with the partner but agree to not distribute it in any way to any other entity or individual. 
4. You will share the code under an open-source license and distribute it as you wish but only the partner can access the system deployed during the course.
5. You will only reference the work you did in your resume, interviews, etc. You agree to not share the code or software in any capacity with anyone unless your partner has agreed to it.

**Your partner cannot ask you to sign any legal agreements or documents pertaining to non-disclosure, confidentiality, IP ownership, etc.**

Briefly describe which option you have agreed to.

Option 5. 

TODO

----

## Teamwork Details

#### Q6: Have you met with your team?

Do a team-building activity in-person or online. This can be playing an online game, meeting for bubble tea, lunch, or any other activity you all enjoy.
* Get to know each other on a more personal level.
* Provide a few sentences on what you did and share a picture or other evidence of your team building activity.
* Share at least three fun facts from members of you team (total not 3 for each member).

Since we all know each other very well, we hang out frequently together.

Fun Facts:

1. Ray Hung can easily get a 90+ exam grade with a 1-hour review. 
2. We have at least 3 students that knows how to solve a Rubik's cube. Including one speed-cuber that can solve it in under 20 seconds consistently!
3. We have 3 students that can play the piano.


#### Q7: What are the roles & responsibilities on the team?

Describe the different roles on the team and the responsibilities associated with each role. 
 * Roles should reflect the structure of your team and be appropriate for your project. One person may have multiple roles.  
 * Add role(s) to your Team-[Team_Number]-[Team_Name].csv file on the main folder.
 * At least one person must be identified as the dedicated partner liaison. They need to have great organization and communication skills.
 * Everyone must contribute to code. Students who don't contribute to code enough will receive a lower mark at the end of the term.

List each team member and:
 * A description of their role(s) and responsibilities including the components they'll work on and non-software related work
 * Why did you choose them to take that role? Specify if they are interested in learning that part, experienced in it, or any other reasons. Do no make things up. This part is not graded but may be reviewed later.

1. Ray Hung - Leader, Backend Developer, Scrum Manager, Partner Liaison
    - He is the leader of the team (Has experience in leading teams)
    - He will be responsible for the overall progress of the project, and ensuring that it meets requirements
    - He will also be responsible for the backend development of the project that is related to Slack's API (Has experience writing a Discord bot)
    - He will also be the partner liaison (As the leader)

2. Scott Cui - Co-Leader, Partner Liaison

3. Will Zhao - Backend Developer, Quality Assurance Tester
   - He will serve as a backend developer and will primarily be responsible for refining and organizing the code and streamlining the workflow for the entire project. (He likes to organize stuff)
   - He will ensure that the implemented feature works as intended and meets the specified requirments. 

4. Arthur Li

5. Jiawei Yu
    - He will be responsible for some parts of the backend development of the project, especially the ones with the database (Has experience in database management)
    - He chooses to take this role as he likes managing databases and understanding the back scene of a project seems really enjoyable to him

#### Q8: How will you work as a team?

Describe meetings (and other events) you are planning to have. 
 * When and where? Recurring or ad hoc? In-person or online?
 * What's the purpose of each meeting?
 * Other events could be coding sessions, code reviews, quick weekly sync meeting online, etc.
 * You should have 2 meetings with your project partner (if you have one) before D1 is due. Describe them here:
   * You must keep track of meeting minutes and add them to your repo under "documents/minutes" folder
   * You must have a regular meeting schedule established for the rest of the term.  

Any meetings required will be held either in person or Zoom. 

However, meetings are not necessary, as we will communicate through Slack and Notion on a frequent basis.

Meetings with project partner will be conducted through Slack as well, as the project partner prefers communication on Slack. 

#### Q9: How will you organize your team?

We used Notion to manage tasks, schedule meetings, post announcements, and document information. 

- We prioritize our tasks with the help of the Notion task board. It's flexible and we can easily assign tasks to specific people.
- Different types of work have different criteria for determining the status. 
    - Programming works are completed once the pull requests are merged.
    - Meetings are completed once we reach our goal for that meeting.
    - Assignments/Deliverables are completed once we submit it.
    - Other tasks can be generalized in similar ways.

We will also utilize Slack to test out our bot and to communicate with our partner.

We will also use the GitHub Project to better manage programming works.

#### Q10: What are the rules regarding how your team works?

**Communications:**

 * We expect that we will meet weekly. 
    * For daily communications, we will use Slack.
    * For weekly meetings, we will host them on Zoom.

 * We will try our best to meet with our partner once a week. 
    * We will first email our partner about our expected meeting schedule, and we will modify it as needed.
    * Then, we will host a meeting with our partner on a proper platform (Zoom).
    * If situation allowed, we will record the meetings and archive them.
    * If in doubt about the client's needs, we will ask on Slack directly.


**Collaboration: (Share your responses to Q8 & Q9 from A1)**

 * How are people held accountable for attending meetings, completing action items? Is there a moderator or process?
 * How will you address the issue if one person doesn't contribute or is not responsive? 
 * TODO


 - As we are close friends in our lives, we will hold each other accountable for attending meetings and completing assigned tasks 
 - If some member of our team does not contribute or is not responsive, we will first try to communicate with them and understand the reason behind it, and try our best to help him overcome it. If the problem persists, we will contact the TA for help.
