"As a user, I want to be able to access all existing questions/post, so I may view them."

The site consist of many post from various "companies", and each of these "companies" can have post of their own. User's should be able to view the post from each "company" when on that "companies" page.

Scenario: View post of a company
Given the user is on the homepage
When the user selects a company
Then the company's post will display

Scenario: View post of a different company
Given the user is viewing one companies page
When the user selects the home icon (the cooler)
And selects a different company
Then a different companies post will display
