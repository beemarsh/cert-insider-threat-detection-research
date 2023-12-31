
# Email Cleaning

The email.csv file from[ **Cert Insider Dataset** r6.2](https://kilthub.cmu.edu/articles/dataset/Insider_Threat_Test_Dataset/12841247?file=24844280) is approximately 8 GB.

The dataset has following attributes:
- id
- date
- user
- pc
- to
- cc
- bcc
- from
- activity
- size
- attachments
- content


## Feature Extraction

First we extracted the following features from the dataset. The following features are extracted for a single user for each day. For example **numEmailSentwithAttachDay** means number of emails sent with attachments by a user for that day.
- numEmailSentwithAttachDay
- numEmailSentwithAttachNight
- numEmailRecievedwithAttachDay
- numEmailRecievedwithAttachNight
- numAttachmentDay
- numAttachmentNight
- numdistinctRecipientsDay
- numdistinctRecipientsNight
- numinternalRecipientsDay
- numinternalRecipientsNight
- numSendDay
- numSendNight
- numReceivedDay
- numReceivedNight

> The cleaned dataset is available at [cleaned_email_dataset.csv](./cleaned_email_dataset.csv)

## Data Splitting and Chunking

1.  
- First we loaded our initial dataset and drop the content column which saves a lot a memory during calculating attributes. We will use email content later to develop a different model.
- We also combined columns **'to'**, **'from'**, **'cc'** and **'bcc'** into a single **'recipients'** column.
- We added a **'day'** column which allows us to group the data by day as we are calculating most of the attributes for each single day.
- It also adds **attachment_count** and **is_working_hour** columns.
- For this we used, [reduce_dataset.ipynb](./reduce_dataset.ipynb) script. You can run the [slurm/reduce.slurm](./slurm/reduce.slurm) file in your HPC cluster, which will convert the notebook to a python script and run the script in the node.
- The output of the script is [reduced_email_dataset.csv](./reduced_email_dataset.csv). I have used parallel processing in my script to make it faster. So, it will generate temporary data and combine those data. The temp files are stored in **temp_combined** folder.

2. 
- Since the dataset is huge and would overload the memory, I split the data into different chunks of file. To maintain the integrity of the data, I split the data for each day. The input dataset is obviously [reduced_email_dataset.csv](./reduced_email_dataset.csv).
- The chunk files are available at **temp_chunks** directory. The name of the chunk files are available in [slurm/chunk_files.log](./slurm/chunk_files.log)
- For this we used, [email_chunks_generator.ipynb](./email_chunks_generator.ipynb) script. You can run the [slurm/generate_chunks.slurm](./slurm/generate_chunks.slurm) file in your HPC cluster, which will convert the notebook to a python script and run the script in the node.

###  Attachments Feature Extraction

- The input datasets are the chunks generated by [email_chunks_generator.ipynb](./email_chunks_generator.ipynb).  The output dataset has eight columns, 2 of which are **user** and **day** and 6 are calculated using the [extract_attachment_counts.ipynb](extract_attachment_counts.ipynb) script. The remaining six features are:
  - numAttachmentDay
  - numAttachmentNight
  - numEmailSentwithAttachDay
  - numEmailSentwithAttachNight
  - numEmailRecievedwithAttachDay
  - numEmailRecievedwithAttachNight
- For this we used, [extract_attachment_counts.ipynb](./extract_attachment_counts.ipynb) script. You can run the [extract_attachment_features.slurm](./slurm/extract_attachment_features.slurm) file in your HPC cluster, which will convert the notebook to a python script and run the script in the node.
- The output dataset is [cleaned_datasets/with_attachment_counts.csv](./cleaned_datasets/with_attachment_counts.csv)

###  Emails Send and Received Feature Extraction

- The input datasets are the chunks generated by [email_chunks_generator.ipynb](./email_chunks_generator.ipynb).  The output dataset has six columns, 2 of which are **user** and **day** and 4 are calculated using the [extract_sent_recieved_email_counts.ipynb](./extract_sent_recieved_email_counts.ipynb) script. The remaining four features are:
  - numSendDay
  -  numSendNight
  -  numReceivedDay
  -  numReceivedNight
- For this we used, [extract_sent_recieved_email.ipynb](./extract_sent_recieved_email.ipynb) script. You can run the [extract_sent_received_features.slurm](./slurm/extract_sent_received_features.slurm) file in your HPC cluster, which will convert the notebook to a python script and run the script in the node.
- The output dataset is [cleaned_datasets/with_sent_recieved_counts.csv](./cleaned_datasets/with_sent_recieved_counts.csv)

###  Internal and External Emails Feature Extraction

- The input datasets are the chunks generated by [email_chunks_generator.ipynb](./email_chunks_generator.ipynb).  The output dataset has six columns, 2 of which are **user** and **day** and 4 are calculated using the [extract_distinct_internal_emails.ipynb](./extract_distinct_internal_emails.ipynb) script. The remaining four features are:
  - numdistinctRecipientsDay
  -  numdistinctRecipientsNight
  -  numinternalRecipientsDay
  -  numinternalRecipientsNight
- For this we used, [extract_distinct_internal_emails.ipynb](./extract_distinct_internal_emails.ipynb) script. You can run the [extract_distinct_internal_features.slurm](./slurm/extract_distinct_internal_features.slurm) file in your HPC cluster, which will convert the notebook to a python script and run the script in the node.
- The output dataset is [cleaned_datasets/with_distinct_internal_counts.csv](./cleaned_datasets/with_distinct_internal_counts.csv)

### Combining extracted features
We have extracted different features in three different files. Now, we have to combine them into a single cleaned dataset. The code is available at [combine_cleaned_datasets.ipynb](./combine_cleaned_datasets.ipynb). 
The output dataset is [cleaned_email_dataset.csv](./cleaned_email_dataset.csv)

#### Cleaned Dataset Template:

| user | day       | numEmailSentwithAttachDay | numEmailSentwithAttachNight | numEmailRecievedwithAttachDay | numEmailRecievedwithAttachNight | numAttachmentDay | numAttachmentNight | numdistinctRecipientsDay | numdistinctRecipientsNight | numinternalRecipientsDay | numinternalRecipientsNight | numSendDay | numSendNight | numReceivedDay | numReceivedNight |
|------|-----------|---------------------------|-----------------------------|--------------------------------|----------------------------------|-------------------|---------------------|--------------------------|----------------------------|--------------------------|----------------------------|-------------|---------------|-----------------|-------------------|
| John | 2023-01-01| 5                         | 2                           | 3                              | 1                                | 10                | 4                   | 7                        | 5                          | 2                        | 1                          | 8           | 3             | 6               | 4                 |
| Jane | 2023-01-02| 3                         | 1                           | 4                              | 2                                | 8                 | 2                   | 6                        | 4                          | 1                        | 1                          | 5           | 2             | 5               | 3                 |
| Alex | 2023-01-03| 6                         | 3                           | 2                              | 1                                | 12                | 5                   | 8                        | 6                          | 3                        | 2                          | 10          | 4             | 4               | 2                 |

