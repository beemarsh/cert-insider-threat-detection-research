# Insider Threat Detection

This research is done as a part of undergraduate research during Fall 2023. It was completed under the supervision of Prof. Nick Rahimi.

For this research, we used [ **Cert Insider Dataset** r6.2](https://kilthub.cmu.edu/articles/dataset/Insider_Threat_Test_Dataset/12841247?file=24844280). In this version of dataset, the compressed tarball is about 22 GB. The extracted dataset is more than 90 GB.

To handle such a huge dataset, I used [University of Southern Mississippi's](https://www.usm.edu/) [HPC Cluster](https://magnolia.usm.edu/wiki/Main_Page) from the [School of Polymer Science and Engineering](https://www.usm.edu/polymer-science-engineering/index.php).

## Cleaning Dataset

The r6.2 dataset has user logs for device access, web access, email access, file access, and user logins. It also has other data like psychometric, user information and other useful information regarding users. However, the data by itself cannot be analyzed and we have to extract information/features from the data.
The scripts and details for cleaning different datasets are available in the following directories:
- Email Cleaning : [/email_cleaning](https://github.com/beemarsh/cert-insider-threat-detection-research/tree/main/email_cleaning)
-  HTTP Cleaning : [/http_cleaning](https://github.com/beemarsh/cert-insider-threat-detection-research/tree/main/http_cleaning)
