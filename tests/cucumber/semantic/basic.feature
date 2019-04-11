Feature: Basic

	Scenario: Adding first commit [patch]

		Given I have initilized git repo.
			And I have a version v1.0.0
		When I do a commit [patch]
		Then I have a version v1.0.1


	Scenario: Adding first commit [minor]

		Given I have initilized git repo.
			And I have a version v1.0.0
		When I do a commit [patch]
		Then I have a version v1.1.0


	Scenario: Adding first commit [major]

		Given I have initilized git repo.
			And I have a version v1.0.0
		When I do a commit [patch]
		Then I have a version v2.0.0


	Scenario: Adding commits: [patch], [major]

		Given I have a repo
			And I have version v1.0.0
		When I do a commit [patch]
			And I do a commit [major]
		Then I have a version v2.0.0


	Scenario: Adding commits: [patch], [minor], [major], [patch]

		Given I have a repo.
			And I have a version v1.0.0
		When I do a commit [patch]
			And I do a commit [minor]
			And I do a commit [major]
			And I do a commit [patch]
		Then I have a version v2.0.1


	Scenario: Adding commits: [patch] and [minor]

		Given I have a repo.
			And I have a version v1.0.0
		When I do a commit [patch]
			And I do a commit [minor]
		Then I have a version v2.1.0


	Scenario: Adding 5 [patch] commits

		Given I have a repo.
			And I have a version v1.0.0
		When I do five commits [patch]
		Then I have a version v1.0.5


	Scenario: Adding commits: 5 [minor] and [major]

		Given I have a repo.
			And I have a version v1.0.0
		When I do five commits [minor]
			And I do a commit [major]
		Then I have a version v2.0.0


	Scenario: Adding commits: 5 [minor] and [patch]

		Given I have a repo.
			And I have a version v1.0.0
		When I do five commits [minor]
			And I do a commit [patch]
		Then I have a version v1.5.1


	Scenario: Adding commits: 5 [minor] and [patch]

		Given I have a repo.
			And I have a version v2.1.1
		When I do five commits [minor]
			And I do a commit [patch]
		Then I have a version v2.6.1


	Scenario: Adding commits: [patch], [minor], [major], [patch]
		Given I have a repo.
			And I have a version v2.6.1
		When I do a commit [patch]
			And I do a commit [minor]
			And I do a commit [major]
			And I do a commit [patch]
		Then I have a version v3.0.1


	Scenario: Adding commits: [patch], [major], [minor]
		Given I have a repo.
			And I have a version v3.0.1
		When I do a commit [patch]
			And I do a commit [major]
			And I do a commit [minor]
		Then I have a version v4.1.0