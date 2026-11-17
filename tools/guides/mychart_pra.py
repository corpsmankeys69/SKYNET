"""Guide config: MyChart - Practice (PRA) Environment Tip Sheet (source: AMB MyChart - Practice Environment Tip Sheet.pdf, footer 09/18/22 JMAMB/DAP)."""
TITLE = 'MyChart – Practice (PRA) Environment Tip Sheet'
HEADER_TITLE = 'MyChart – Practice (PRA) Environment Tip Sheet'   # source header; template's "Quick Start Guide" suffix dropped
APP_AUD = 'MyChart | All Roles'
LINKS = {
    'rId101': 'https://trnecare18.epic.medical.washington.edu/pra/',      # live link, host name kept as-is
    'rId102': 'https://one.uwmedicine.org/ehrhub/Pages/Practice_in_Epic.aspx',
}
CONTENT = [
 ('h1', 'MyChart – Practice (PRA) Environment Tip Sheet'),

 ('h2', 'Accessing MyChart in the Practice (PRA) Environment'),
 ('p', 'The MyChart Practice environment is your opportunity to get hands-on practice exploring and testing some of the functionality that our patients see when using MyChart. Follow the instructions below to log into the MyChart PRA Environment as one of the designated MyChart practice patients.'),
 ('step', 'Access the MyChart PRA Environment by clicking on the following link:\n{{link:rId101|https://trnecare18.epic.medical.washington.edu/pra/}}'),
 ('note', 'Must be connected to Pulse Secure VPN or UW Medicine internal network to access MyChart training sites.'),
 ('shot', '[[Screenshot: MyChart sign-in page with the UW Medicine | Fred Hutch Cancer Center logo, and the MyChart Username and Password fields]]'),
 ('step', 'Type a MyChart Username and Password into the appropriate fields of the MyChart PRA Website.'),
 ('step', 'Use one of the following patient logins:'),
 ('table', {'widths': [3078, 3078, 3079], 'title': None,
            'header': ['MyChart Username', 'MyChart Password', 'Patient Name for ((blank)) Practice Playground'],
            'rows': [[u, 'Mychart1', '%s, Nadir' % u] for u in ('MyCat', 'MyCar', 'MyCookie', 'MyCoat', 'MyCow', 'MyCamel', 'MyChair')]}),

 ('h2', 'Accessing ((blank)) in the Practice (PRA) Environment', 'pagebreak'),
 ('p', 'The ((blank)) Practice Playground environment is your opportunity to practice workflows involving MyChart from a clinical perspective, including sending In Basket messages to our designated MyChart practice patients. Follow the instructions from the following link to access Citrix and the ((blank)) – Practice Playground Environment: {{link:rId102|https://one.uwmedicine.org/ehrhub/Pages/Practice_in_Epic.aspx}}'),
 ('step', 'Once you have the ((blank)) – Practice Environment open, log in as one of the following training users:'),
 ('shot', '[[Image: practice playground icon]]'),
 ('table', {'widths': [2300, 2800, 1400, 2735], 'title': 'Login Information for ((blank)) Practice Playground',
            'header': ['Role', 'User ID', 'Password', 'Department'],
            'rows': [['Clinician (RN, MA)', 'Nurse02 to Nurse08', 'train', 'HMC FAM MED CLINIC 20'],
                     ['Practitioner', 'Opintm02 to Opintm08', 'train', 'HMC FAM MED CLINIC 20']]}),
 ('tip', 'Full list of roles for training user logins in ((blank)) PRA Playground included at the link above.'),
]
