"As a user, I want to be able to report post, so I may moderate inappropriate content"

When a user is viewing a post they will be able to fill out a forum to report a post

Scenario: User wants to report a post
Given a user is viewing a post
When the user selects the report button
And fills out the report forum
Then a report will get filed in the report database