# MPR-sharepoint-utils

Tools for interfacing between python code and SharePoint storage.

- built directly off graphql api
- currently requires pandas (eventually could have a base SharepointUtils class that only returns file streams, does not do `pd.read_csv` or `pd.read_excel`)

## Installing the package

```bash
pipenv install mpr-sharepoint-utils
```

Once the package is installed, you can use it like this:

```python
from sharepoint_utils.lib import SharePointUtils
```

## Using the package:

- Useful methods are in the SharePointUtils class, which requires these arguments to connect to your SharePoint instance:
  - client_id, the ID portion of your user (or service) account credentials
  - client_secret, the secret string of your user (or service) credentials
  - site_id, the ID of the SharePoint site you wish to access
  - tenant, the name of your organization (you can find this in a SharePoint URL, like "tenant.sharepoint.com")

## FAQs

Q: How do
I know what my
site ID is?
A: First, get your access token with the first command below; then, plug that into the second command below to get your site ID.

Get access token (can use to get site id given hostname and path (site/subsite)):

```
curl --location --request POST 'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'client_id=INSERT_CLIENT_ID' \
--data-urlencode 'scope=https://graph.microsoft.com/.default' \
--data-urlencode 'client_secret=INSERT_CLIENT_SECRET' \
--data-urlencode 'grant_type=INSERT_CLIENT_CREDENTIALS'
```

Get site ID

```
curl --location --request GET 'https://graph.microsoft.com/v1.0/sites/{hostname}:/sites/{path}?$select=id' \
--header 'Authorization: Bearer access_token' \
--data
```
