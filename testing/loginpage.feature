"As a user, I want to be able to create an account, so I may access the site"

The website will use user accounts to track their permissions, post, and make user interaction easier.

Scenario: User wants to make account
Given the user is on the splash page
When they input their details
And click create account
Then if they enter valid credentials an account created message will appear

"As a user, I want to be able to log into my account, so I may access the site"

The website will use user accounts to track their permissions, post, and make user interation easier.

Scenario: User wants to login
Given the user is on the spalsh page
When they input their credentials
And click login
Then if they enter valid credentials they will be taken to their homepage
