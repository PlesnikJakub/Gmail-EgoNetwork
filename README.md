# GmailEgoNetwork


All prerequisities and original manual for API settup is available at https://developers.google.com/gmail/api/quickstart/python

:warning: The setup is complex, so take your time.

## How to run

* Clone or download repository
* Go to Google console and create a project - follow https://developers.google.com/workspace/guides/create-project#create_a_new_google_cloud_platform_gcp_project
* Enable Gmail API for your project - simmilar to https://developers.google.com/workspace/guides/create-project#enable-api
* Setup OAuth consent screen - https://developers.google.com/workspace/guides/create-credentials#configure_the_oauth_consent_screen
* Add your email into Test users list on consent screen page
* Generate OAuth 2.0 Client IDs credentials for desktop application - https://developers.google.com/workspace/guides/create-credentials
* Download credentials and put credentials.json into project root
*  Install dependencies

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
*  Run code
```
python main.py
```
* On first run you will be asked for permissions
* Check out output.csv for result
