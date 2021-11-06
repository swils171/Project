"As a user, I want to be able to delete a post I made"

whenever a user is viewing a post they made they should be able to delete it from the company.

Scenario: Delete post I made from a company
Given the user is viewing their post
When the user selects the post options button on their post
And selects delete
Then their post will be deleted from the given companies post database
