# -*- coding: utf-8 -*-


github_get_user_resp = '''{"display_name": "smallfz", "github_user": {"login": "smallfz", "id": 8371274, "avatar_url": "https://avatars3.githubusercontent.com/u/8371274?v=4", "gravatar_id": "", "url": "https://api.github.com/users/smallfz", "html_url": "https://github.com/smallfz", "followers_url": "https://api.github.com/users/smallfz/followers", "following_url": "https://api.github.com/users/smallfz/following{/other_user}", "gists_url": "https://api.github.com/users/smallfz/gists{/gist_id}", "starred_url": "https://api.github.com/users/smallfz/starred{/owner}{/repo}", "subscriptions_url": "https://api.github.com/users/smallfz/subscriptions", "organizations_url": "https://api.github.com/users/smallfz/orgs", "repos_url": "https://api.github.com/users/smallfz/repos", "events_url": "https://api.github.com/users/smallfz/events{/privacy}", "received_events_url": "https://api.github.com/users/smallfz/received_events", "type": "User", "site_admin": false, "name": null, "company": null, "blog": "", "location": null, "email": null, "hireable": null, "bio": null, "public_repos": 25, "public_gists": 0, "followers": 4, "following": 3, "created_at": "2014-08-06T06:33:27Z", "updated_at": "2017-12-10T11:11:42Z", "private_gists": 0, "total_private_repos": 0, "owned_private_repos": 0, "disk_usage": 1188, "collaborators": 0, "two_factor_authentication": false, "plan": {"name": "free", "space": 976562499, "collaborators": 0, "private_repos": 0}}}'''

github_token = {"access_token": "6f05099102192fbcc40d5592d4e23bb944f5f8b9", "token_type": "bearer", "scope": "repo,user"}

github_get_repos_resp = '''[{"id": 111982938, "name": "handy-docker-images", "full_name": "smallfz/handy-docker-images", "owner": {"login": "smallfz", "id": 8371274, "avatar_url": "https://avatars3.githubusercontent.com/u/8371274?v=4", "gravatar_id": "", "url": "https://api.github.com/users/smallfz", "html_url": "https://github.com/smallfz", "followers_url": "https://api.github.com/users/smallfz/followers", "following_url": "https://api.github.com/users/smallfz/following{/other_user}", "gists_url": "https://api.github.com/users/smallfz/gists{/gist_id}", "starred_url": "https://api.github.com/users/smallfz/starred{/owner}{/repo}", "subscriptions_url": "https://api.github.com/users/smallfz/subscriptions", "organizations_url": "https://api.github.com/users/smallfz/orgs", "repos_url": "https://api.github.com/users/smallfz/repos", "events_url": "https://api.github.com/users/smallfz/events{/privacy}", "received_events_url": "https://api.github.com/users/smallfz/received_events", "type": "User", "site_admin": false}, "private": false, "html_url": "https://github.com/smallfz/handy-docker-images", "description": null, "fork": false, "url": "https://api.github.com/repos/smallfz/handy-docker-images", "forks_url": "https://api.github.com/repos/smallfz/handy-docker-images/forks", "keys_url": "https://api.github.com/repos/smallfz/handy-docker-images/keys{/key_id}", "collaborators_url": "https://api.github.com/repos/smallfz/handy-docker-images/collaborators{/collaborator}", "teams_url": "https://api.github.com/repos/smallfz/handy-docker-images/teams", "hooks_url": "https://api.github.com/repos/smallfz/handy-docker-images/hooks", "issue_events_url": "https://api.github.com/repos/smallfz/handy-docker-images/issues/events{/number}", "events_url": "https://api.github.com/repos/smallfz/handy-docker-images/events", "assignees_url": "https://api.github.com/repos/smallfz/handy-docker-images/assignees{/user}", "branches_url": "https://api.github.com/repos/smallfz/handy-docker-images/branches{/branch}", "tags_url": "https://api.github.com/repos/smallfz/handy-docker-images/tags", "blobs_url": "https://api.github.com/repos/smallfz/handy-docker-images/git/blobs{/sha}", "git_tags_url": "https://api.github.com/repos/smallfz/handy-docker-images/git/tags{/sha}", "git_refs_url": "https://api.github.com/repos/smallfz/handy-docker-images/git/refs{/sha}", "trees_url": "https://api.github.com/repos/smallfz/handy-docker-images/git/trees{/sha}", "statuses_url": "https://api.github.com/repos/smallfz/handy-docker-images/statuses/{sha}", "languages_url": "https://api.github.com/repos/smallfz/handy-docker-images/languages", "stargazers_url": "https://api.github.com/repos/smallfz/handy-docker-images/stargazers", "contributors_url": "https://api.github.com/repos/smallfz/handy-docker-images/contributors", "subscribers_url": "https://api.github.com/repos/smallfz/handy-docker-images/subscribers", "subscription_url": "https://api.github.com/repos/smallfz/handy-docker-images/subscription", "commits_url": "https://api.github.com/repos/smallfz/handy-docker-images/commits{/sha}", "git_commits_url": "https://api.github.com/repos/smallfz/handy-docker-images/git/commits{/sha}", "comments_url": "https://api.github.com/repos/smallfz/handy-docker-images/comments{/number}", "issue_comment_url": "https://api.github.com/repos/smallfz/handy-docker-images/issues/comments{/number}", "contents_url": "https://api.github.com/repos/smallfz/handy-docker-images/contents/{+path}", "compare_url": "https://api.github.com/repos/smallfz/handy-docker-images/compare/{base}...{head}", "merges_url": "https://api.github.com/repos/smallfz/handy-docker-images/merges", "archive_url": "https://api.github.com/repos/smallfz/handy-docker-images/{archive_format}{/ref}", "downloads_url": "https://api.github.com/repos/smallfz/handy-docker-images/downloads", "issues_url": "https://api.github.com/repos/smallfz/handy-docker-images/issues{/number}", "pulls_url": "https://api.github.com/repos/smallfz/handy-docker-images/pulls{/number}", "milestones_url": "https://api.github.com/repos/smallfz/handy-docker-images/milestones{/number}", "notifications_url": "https://api.github.com/repos/smallfz/handy-docker-images/notifications{?since,all,participating}", "labels_url": "https://api.github.com/repos/smallfz/handy-docker-images/labels{/name}", "releases_url": "https://api.github.com/repos/smallfz/handy-docker-images/releases{/id}", "deployments_url": "https://api.github.com/repos/smallfz/handy-docker-images/deployments", "created_at": "2017-11-25T06:44:15Z", "updated_at": "2017-11-25T06:47:46Z", "pushed_at": "2017-11-25T17:08:14Z", "git_url": "git://github.com/smallfz/handy-docker-images.git", "ssh_url": "git@github.com:smallfz/handy-docker-images.git", "clone_url": "https://github.com/smallfz/handy-docker-images.git", "svn_url": "https://github.com/smallfz/handy-docker-images", "homepage": null, "size": 3, "stargazers_count": 0, "watchers_count": 0, "language": "Shell", "has_issues": true, "has_projects": true, "has_downloads": true, "has_wiki": true, "has_pages": false, "forks_count": 0, "mirror_url": null, "archived": false, "open_issues_count": 0, "license": null, "forks": 0, "open_issues": 0, "watchers": 0, "default_branch": "master", "permissions": {"admin": true, "push": true, "pull": true}}, {"id": 110776887, "name": "cx_oracle_on_ctypes", "full_name": "smallfz/cx_oracle_on_ctypes", "owner": {"login": "smallfz", "id": 8371274, "avatar_url": "https://avatars3.githubusercontent.com/u/8371274?v=4", "gravatar_id": "", "url": "https://api.github.com/users/smallfz", "html_url": "https://github.com/smallfz", "followers_url": "https://api.github.com/users/smallfz/followers", "following_url": "https://api.github.com/users/smallfz/following{/other_user}", "gists_url": "https://api.github.com/users/smallfz/gists{/gist_id}", "starred_url": "https://api.github.com/users/smallfz/starred{/owner}{/repo}", "subscriptions_url": "https://api.github.com/users/smallfz/subscriptions", "organizations_url": "https://api.github.com/users/smallfz/orgs", "repos_url": "https://api.github.com/users/smallfz/repos", "events_url": "https://api.github.com/users/smallfz/events{/privacy}", "received_events_url": "https://api.github.com/users/smallfz/received_events", "type": "User", "site_admin": false}, "private": false, "html_url": "https://github.com/smallfz/cx_oracle_on_ctypes", "description": "cx_Oracle on ctypes", "fork": true, "url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes", "forks_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/forks", "keys_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/keys{/key_id}", "collaborators_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/collaborators{/collaborator}", "teams_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/teams", "hooks_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/hooks", "issue_events_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/issues/events{/number}", "events_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/events", "assignees_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/assignees{/user}", "branches_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/branches{/branch}", "tags_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/tags", "blobs_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/git/blobs{/sha}", "git_tags_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/git/tags{/sha}", "git_refs_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/git/refs{/sha}", "trees_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/git/trees{/sha}", "statuses_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/statuses/{sha}", "languages_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/languages", "stargazers_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/stargazers", "contributors_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/contributors", "subscribers_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/subscribers", "subscription_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/subscription", "commits_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/commits{/sha}", "git_commits_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/git/commits{/sha}", "comments_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/comments{/number}", "issue_comment_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/issues/comments{/number}", "contents_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/contents/{+path}", "compare_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/compare/{base}...{head}", "merges_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/merges", "archive_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/{archive_format}{/ref}", "downloads_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/downloads", "issues_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/issues{/number}", "pulls_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/pulls{/number}", "milestones_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/milestones{/number}", "notifications_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/notifications{?since,all,participating}", "labels_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/labels{/name}", "releases_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/releases{/id}", "deployments_url": "https://api.github.com/repos/smallfz/cx_oracle_on_ctypes/deployments", "created_at": "2017-11-15T03:09:11Z", "updated_at": "2017-11-15T03:09:13Z", "pushed_at": "2016-12-28T20:21:09Z", "git_url": "git://github.com/smallfz/cx_oracle_on_ctypes.git", "ssh_url": "git@github.com:smallfz/cx_oracle_on_ctypes.git", "clone_url": "https://github.com/smallfz/cx_oracle_on_ctypes.git", "svn_url": "https://github.com/smallfz/cx_oracle_on_ctypes", "homepage": "", "size": 6066, "stargazers_count": 0, "watchers_count": 0, "language": "Python", "has_issues": false, "has_projects": true, "has_downloads": true, "has_wiki": true, "has_pages": false, "forks_count": 0, "mirror_url": null, "archived": false, "open_issues_count": 0, "license": null, "forks": 0, "open_issues": 0, "watchers": 0, "default_branch": "master", "permissions": {"admin": true, "push": true, "pull": true}}]'''
