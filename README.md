![Apprise Logo](https://raw.githubusercontent.com/caronc/apprise/master/apprise/assets/themes/default/apprise-logo.png)

<hr/>

**ap·prise** / *verb*<br/>
To inform or tell (someone). To make one aware of something.
<hr/>

**Apprise Transactions** *aims* to enable push Notifications for *just about* every payment platform with *just about* every notification service

*notification* services available to us today such as: Telegram, Discord, Slack, Amazon SNS, Gotify, etc.

* One notification library to rule them all.
* A common and intuitive notification syntax.
* Supports the handling of images and attachments (to the notification services that will accept them).

Business owners who wish to receive notifications for payments no longer need to develop a custom notification system for each and every new payment platform or notification service as they appear. They can use this one script to standardize how transactions are received across payment platforms.

Developers who wish to build applications that accept payments can more easily integrate a range of payment platforms. JSON formatted requests can be sent to notification services, such as Amazon SNS or a custom endpoint, for further processing. Everything is already wrapped and supported within the *apprise transaction notify* script that ships with this product.


![apprise-transactions unit tests](https://github.com/apprises/apprise-transactions/workflows/apprise-transactions%20unit%20tests/badge.svg)
![Upload Python Package](https://github.com/apprises/apprise-transactions/workflows/Upload%20Python%20Package/badge.svg)
[![codecov](https://codecov.io/gh/apprises/apprise-transactions/branch/master/graph/badge.svg)](https://codecov.io/gh/apprises/apprise-transactions)

## Supported Notifications
This project is dependent on [Apprise](https://github.com/caronc/apprise) for notifications.

[Please see the official Apprise wiki for a full list of services that are supported.](https://github.com/caronc/apprise/wiki)

### Supported Payment Platforms
The table below identifies the platforms this tool supports and some example service urls you need to use in order to take advantage of it. Click on any of the services listed below to get more details on how you can configure Apprise to access them.

Payment Platform  | Status | Dependent Services | Default Port
------------- | ------------- | ------------- | ------------- 
[Monero](https://getmonero.org)  | Implemented (Stable) | monerod / monero-wallet-rpc | (TCP) 18081 / (TCP) 18082 
[Square](https://developer.squareup.com/us/en)  | Planned | [Square, Inc.](https://squareup.com/us/en/about) | (TCP) 443


## Installation
The easiest way is to install this package is from pypi:
```bash
pip install apprise-transactions
```
## Command Line
A small command line tool is also provided with this package called apprise-transactions. If you know the server url's you wish to notify, you can simply provide them all on the command line and send your notifications that way:

Note: The command line tool is intended to be executed once per transaction.
```bash
# Here is a full example, but we will go over the parts of the command below

monero-wallet-rpc --wallet-file ~/mywallet --disable-rpc-login --rpc-bind-port 18088 --prompt-for-password \
--tx-notify "/usr/bin/apprisetransactions --payment_provider Monero --tx_id %s \
--urls tgram://1034520651:CCCFjiawu448agga4TI_Bu3oolct1Qrxasdjf --debug --get_tx_details \
-s 0 -b You%20have%20received%20%7Bamount%7D%20%7Bcurrency%7D%2C%20which%20is%20currently%20worth%20%24%7Bamount_in_usd%7D \
-t Congrats%20incoming%20payment%20from%20%7Bpayment_provider%7D"

# First you should test that notifications are working with your preferred notification service(s) with the basic command line parameters, then add additional parameters
apprisetransactions --payment_provider Monero --tx_id testsdiajetestasjdftestasdjf --urls tgram://1043520651:CCCFjiawu448agga4TI_Bu3oolct1Qrxasdjf

# To have automated notifications when receiving a new transaction you need to run a command that kicks off this tool while passing the tx_id
# --detach should be added if this process should run in the background
monero-wallet-rpc --tx-notify ""

# The full path of apprisetransacttions needs to be specified within the tx-notify parameter for it to be executed
# find and note the static path
# linux
which apprisetransactions
# example output: /usr/bin/apprisetransactions
# we now add this to our previous command, with %s being passed to the tx_parameter

monero-wallet-rpc --tx-notify "/usr/bin/apprisetransactions  --payment_provider Monero \
--tx_id %s --urls tgram://1043520651:CCCFjiawu448agga4TI_Bu3oolct1Qrxasdjf"

# Now let's look at examples of all the parameters one can use with apprisetransactions

# Send a notification to as many servers as you want
# as you can easily chain one after another:
monero-wallet-rpc --tx-notify "/usr/bin/apprisetransactions \
--payment_provider Monero --tx_id %s \
--urls mailto://userid:password@example.com?smtp=mail.example.com&from=noreply@example.com&name=no%20reply,pbul://o.gn5kj6nfhv736I7jC3cj3QLRiyhgl98b"


# If you don't specify a --body (-b) or --title (-t) then the default is taken
# --title Received%20transaction%20from%20%7Bpayment_provider%7D
# resolves to "Received transaction from Monero"
# --body Check%20your%20wallet%20for%20more%20details
# resolves to "Check your wallet for more details"
# Go to https://www.urlencoder.org/ for easy url encoding
# Another example below: You have received {amount} {currency}, which is currently worth ${amount_in_usd}
monero-wallet-rpc --tx-notify "/usr/bin/apprisetransactions \
--payment_provider Monero --tx_id %s \
--urls mailto://userid:password@example.com?smtp=mail.example.com&from=noreply@example.com&name=no%20reply \
--get_tx_details \
--body You%20have%20received%20%7Bamount%7D%20%7Bcurrency%7D%2C%20which%20is%20currently%20worth%20%24%7Bamount_in_usd%7D"

# By default only the fact that you received a transaction is conveyed
# --get_tx_details needs to be specified if you want to utilize the following placeholders:
# {amount} {fee} {note} {recipient} {timestamp} {confirmations}
monero-wallet-rpc --tx-notify "/usr/bin/apprisetransactions \
--payment_provider Monero --tx_id %s \
--urls mailto://userid:password@example.com?smtp=mail.example.com&from=noreply@example.com&name=no%20reply \
--get_tx_details \
--body {recipient}"

#  For developers who want to forward the raw data to another server can do so
# Just specify --get_tx_details and --get_raw_data
# XML / JSON directly to a port or via Amazon SNS is supported
# body / title parameters will be ignored
monero-wallet-rpc --tx-notify "/usr/bin/apprisetransactions \
--payment_provider Monero --tx_id %s \
--urls json://user:password@hostname:port \
--get_tx_details \
--get_raw_data"

# By default transactions are notified by the configured server immediately
# For higher security specify the number of confirmations as a parameter
# -1 will notify both, when the transaction is found in the mem pool and when the transaction is added to a block
# 0 is the default
# 1 means that the transaction has been added to one block on the network
# The example below is 10, meaning 10 nodes in the network must have accepted your tx in their next block
monero-wallet-rpc --tx-notify "/usr/bin/apprisetransactions  --payment_provider Monero \
--tx_id %s --urls tgram://1043520651:CCCFjiawu448agga4TI_Bu3oolct1Qrxasdjf \
--security_level 10"

```

### Configuration Files
To request further transaction details requests are made to a server. By default localhost will be used.
Optionally server configuration can be stored in a file.
```bash
# Configuration files can be stored anywhere and passed in via --server_config (-c)
monero-wallet-cli --tx-notify "/usr/bin/apprisetransactions \
--payment_provider Monero --tx_id %s \
--urls pbul://o.gn5kj6nfhv736I7jC3cj3QLRiyhgl98b \
--server_config /etc/apprise/server.cfg"
```

### Attaching Files
Apprise also supports file attachments too! Specify as many attachments to a notification as you want.
```bash
# Include a custom image in the notification:
monero-wallet-rpc --tx-notify "/usr/bin/apprisetransactions \
--payment_provider Monero --tx_id %s \
--urls discord:///4174216298/JHMHI8qBe7bk2ZwO5U711o3dV_js \
-attach https://siasky.net/fAOAieEJvZ0FegbcZMPWAtbKKscdUKXCimkjtv6uHKW9-A"
```

## Developers
To send a notification from within your python application, just do the following:
```python
# import one or more of the transaction factories
from apprisetransactions.factories import MoneroFactory
# import one or more transaction types
from apprisetransactions.transactions import MoneroTransaction
# import server config that's needed to get the details of a transaction
from apprisetransactions.configuration import ServerConfig
# import security settings
from apprisetransactions import settings
from apprisetransactions.settings import BlockchainSecurity
# initialize singletons
settings.init()
# set your security level
settings.security_level = BlockchainSecurity.IN_A_BLOCK
# Create a transaction factory
transaction_factory = MoneroFactory(server_config_file='server.cfg')
# Get a transaction from the transaction factory
transaction: MoneroTransaction = transaction_factory.get_transaction(
            tx_id='asdf',
            get_tx_data=True,
            get_raw_data=True,
        )
# specify the notification services that you want to use in a list
urls = ['pbul://o.gn5kj6nfhv736I7jC3cj3QLRiyhgl98b']
body = 'Transaction received: {tx_id}'
title = 'Transaction incoming from {payment_provider}'
attach = 'https://siasky.net/fAOAieEJvZ0FegbcZMPWAtbKKscdUKXCimkjtv6uHKW9-A'
# Have the notification services propagate the transaction notification
# A sample pushbullet notification:
apprise_result = transaction.notify(
    urls=urls, body=body, title=title, attach=attach
)
if apprise_result is False:
    logging.error('Apprise failed to complete notification')
```

### Attaching Files
Attachments are very easy to send using the API:
```python
apprise_result = transaction.notify(
    urls=urls, body=body, title=title, attach='/local/path/to/my/DSC_003.jpg'
)
```

To send more than one attachment, you just need the **AppriseAttachment** object:
```python
from apprise import AppriseAttachment

# Initialize our attachment object
attachments = AppriseAttachment()

# Now add all of the entries we're intrested in:
# ?name= allows us to rename the actual jpeg as found on the site
# to be another name when sent to our receipient(s)
attachments.add('https://i.redd.it/my2t4d2fx0u31.jpg?name=FlyingToMars.jpg')

# Now add another:
attachments.add('/path/to/funny/joke.gif')

# Send your multiple attachments with a single notify call:
apprise_result = transaction.notify(
    urls=urls, body=body, title=title, attach=attachments
)
```

## Want To Learn More?

Want to add a payment provider?
* 💡 [Contribute to the Apprise Transactions Code Base](https://github.com/apprises/apprise-transactions/wiki/Development_Contribution)
Want to add a notification service?
* 💡 [Contribute to the Apprise Code Base](https://github.com/caronc/apprise/wiki/Development_Contribution)

If you're interested in reading more about this and other methods on how to customize your own notifications, please check out the following links:
* 📣 [Using the CLI](https://github.com/apprises/apprise-transactions/wiki/CLI_Usage)
* 🛠️ [Development API](https://github.com/apprises/apprise-transactions/wiki/Development_API)
* 🔧 [Troubleshooting](https://github.com/apprises/apprise-transactions/wiki/Troubleshooting)
* ⚙️ [Configuration File Help](https://github.com/apprises/apprise-transactions/wiki/config)
* 🌎 [Apprise API/Web Interface](https://github.com/apprises/apprise-transactions/apprise-api)
* 🎉 [Showcase](https://github.com/apprises/apprise-transactions/wiki/showcase)


