"""Guide config: AMB BCMA (Bar Code Medication Administration) FAQ (source: AMB_BCMA_FAQ.docx, v.8 2024.1231 EYL)."""
TITLE = 'AMB BCMA (Bar Code Medication Administration) FAQ'
HEADER_TITLE = 'AMB BCMA (Bar Code Medication Administration) FAQ'   # source header; the template's "Quick Start Guide" suffix is dropped for an FAQ
APP_AUD = 'Ambulatory | Clinician'
LINKS = {
    'rId101': 'mailto:mcsos@uw.edu',
    'rId102': 'https://one.uwmedicine.org/sites/Policies/_layouts/15/WopiFrame.aspx?sourcedoc=%2Fsites%2FPolicies%2FPolicies%20Live%2Fuwm-ea-1482.pdf&action=view',
}
CONTENT = [
 ('h1', 'Ambulatory BCMA FAQ'),
 ('h2', 'Frequently Asked Questions'),

 ('h3', 'Does the new BCMA workflow impact how I retrieve medications from the Pyxis?'),
 ('p', 'No, BCMA does not change your Pyxis workflow. Please continue to follow your usual workflow for retrieving patient medications from the Pyxis.'),

 ('h3', 'Is there a way to edit my administration if I need to modify it?'),
 ('p', 'Yes, there is functionality to edit your administration as indicated. Please refer to the BCMA tip sheet for steps and screenshots.'),

 ('h3', 'Am I able to document a MAR administration for another user?'),
 ('p', 'While it is Best Practice for to document one’s own medication administrations, there is existing functionality in ((blank)) that allows for documentation on another’s behalf.'),
 ('shot0', '[[Screenshot: MAR header with the Document for Another link outlined]]'),
 ('p', 'After clicking on the link, a new field will populate in Administration Details:'),
 ('shot0', '[[Screenshot: Administration Details with the Document for Another field outlined]]'),

 ('h3', 'How do I scan a multi-component medication?'),
 ('p', 'To scan a multi-component medication, scan each component individually until you meet the ordered dose. For example, when scanning two acetaminophen tablets, after the first tablet is scanned the MAR populates with the scanned dose while indicating the Expected Dose:'),
 ('shot0', '[[Screenshot: Administration Details after the first tablet, Dose and Expected Dose outlined]]'),
 ('p', 'When the second tablet is scanned, the MAR updates:'),
 ('shot0', '[[Screenshot: Administration Details after the second tablet, Dose outlined]]'),

 ('h3', 'What if I need to scan multiple medication packages to meet the ordered dose and the packages have different Lot numbers and/or expiration dates?'),
 ('p', 'Like scanning a multi-component medication, scan each component individually until you meet the ordered dose. If the Lot number and/or expiration date are different between the packages (and are available to be pulled in to the MAR from the scanned barcode), the MAR will stack this information in the Billing details so that the variances are accounted for.'),
 ('shot0', '[[Screenshot: Billing details with stacked Lot Number and Expiration Date entries outlined]]'),

 ('h3', 'Is there a way to communicate with Pharmacy directly if there are any medication issues?'),
 ('p', 'To communicate directly with Pharmacy should any medication issues arise, you can navigate to the medication in the MAR and select the Rx button as outlined in the screenshot below. This function is only for on-site pharmacies and only enabled for clinics that utilize our inpatient pharmacies.'),
 ('shot0', '[[Screenshot: MAR medication row with the Rx button outlined]]'),

 ('h3', 'What is best practice for scanning multi-component medications that may not come as a single package?'),
 ('p', 'This will depend on how the medication is built. For example, GI cocktail is a panel order in ((blank)) and each medication should be scanned. If it is a compounded medication that only creates a single line on the MAR, it will have a custom NDC assigned (99999-) and the scan would only work from a pharmacy label.'),

 ('h3', 'What should I do if I’m unable to scan a medication?'),
 ('p', 'Please connect with your RN3/manager or clinic champion same day so that troubleshooting can actively occur. If you need to reach out to IT for assistance, please include the following information:'),
 ('bullet0', 'Patient MRN'),
 ('bullet0', 'Order number'),
 ('bullet0', 'Name of the medication and the type of error or alert encountered'),
 ('bullet0', 'Medication NDC'),
 ('bullet0', 'Code that populates when scanning the barcode into Notepad'),
 ('bullet0', 'Photo of barcode(s) if possible'),

 ('h3', 'Who do I contact for help if I’m experiencing issues with a scanner?'),
 ('p', 'Please submit a ticket via {{link:rId101|mcsos@uw.edu}} or call the IT Help Desk at 206 – 520 – 2200.'),

 ('h3', 'How do I clean the barcode scanners?'),
 ('p', 'Please refer to the {{link:rId102|Disinfection of Multi-Patient Use Equipment}} policy.'),
]
