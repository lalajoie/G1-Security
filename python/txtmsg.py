from __future__ import print_function # python 2/3 compatibility for example code

import telerivet

API_KEY = '6vi3m_1fY1hW5N5wlJowBiYC3xHd68ex8S6m'  # from https://telerivet.com/api/keys
PROJECT_ID = 'PJac1b0ccab951ab23'

tr = telerivet.API(API_KEY)

project = tr.initProjectById(PROJECT_ID)

# Send a SMS message
project.sendMessage(
    to_number = '+639217301559',
    content = 'Hello world!'
)