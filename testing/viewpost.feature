"As a user, I want to be able to access all existing questions/post, so I may view them."

The site consist of many post from various forums, and each of these forums can have post of their own. User's should be able to view the post from each forum when on that forum's page.

Scenario: View post of a forum
Given the user is on the homepage
When the user selects a forum
Then the forum's post will display

Scenario: View post of a different forum
Given the user is viewing one forums page
When the user selects the home icon (the cooler)
And selects a different forum
Then a different forums post will display

Scenario: View post replies
Given the user is viewing post from a forum
When the user selects a given post
Then it will open a new page with the post enlarged and has the replies below the post
