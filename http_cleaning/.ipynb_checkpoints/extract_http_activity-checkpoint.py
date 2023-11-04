#!/usr/bin/env python
# coding: utf-8

# In[1]:


# The input dataset should already have a 'day' and 'is_working_hour column' defined which we already did.
# We are also using the chunks that we generated using the email_chunk_generator file

# The output dataset has six columns, 2 of which are user and day.
# This script calculate four attributes from the email cert dataset. It generates the following attribute for each user for every single day
# numSendDay
# numSendNight
# numReceivedDay
# numReceivedNight# The input dataset should already have a 'day' and 'is_working_hour column' defined which we already did.
# We are also using the chunks that we generated using the http_chunk_generator file

# The output dataset has eight columns, 2 of which are user and day.
# This script calculate four attributes from the email cert dataset. It generates the following attribute for each user for every single day
# numWebAccDay
# numWebAccNight
# numUploadDay
# numUploadNight
# numDownloadDay
# numDownloadNight

# For this dataset calculation, I used HPC Cluster (Magnolia) from University of Southern Mississippi
# In HPC clusters, I used Slrum Workload Manager, the script for which is also discussed somewhere in the repo

import pandas as pd
from multiprocessing import Pool
import os


# In[2]:


temp_folder_results = 'temp_results'  # Temporary folder to store intermediate result files
temp_folder_chunks= 'temp_chunks'  # Folder that stores intermediate chunked files
output_file = 'with_activity_counts.csv'


# In[3]:


# To make sure that the folder exists
os.makedirs(temp_folder_results, exist_ok=True)


# In[39]:


# Function to calculate the number of emails sent and received during day and night for each user in a day
def calculate_activity_counts(chunk_filename):
    df = pd.read_csv(f'{temp_folder_chunks}/{chunk_filename}')

    df['is_working_hour'] = df['is_working_hour'].astype(bool)

    # Filter data for Sent activities
    access_data = df[df['activity'] == 'WWW Visit']
    download_data = df[df['activity'] == 'WWW Download']
    upload_data = df[df['activity'] == 'WWW Upload']

    # Group data by user, date, and working hour, then count the downloads during day and night for each user
    day_access = access_data[access_data['is_working_hour']][['user', 'day']].groupby(['user', 'day']).size().reset_index(name='numWebAccDay')
    night_access = access_data[~access_data['is_working_hour']][['user', 'day']].groupby(['user', 'day']).size().reset_index(name='numWebAccNight')
    
    # Group data by user, date, and working hour, then count the downloads during day and night for each user
    day_downloads = download_data[download_data['is_working_hour']][['user', 'day']].groupby(['user', 'day']).size().reset_index(name='numDownloadsDay')
    night_downloads = download_data[~download_data['is_working_hour']][['user', 'day']].groupby(['user', 'day']).size().reset_index(name='numDownloadsNight')

    day_uploads = upload_data[upload_data['is_working_hour']][['user', 'day']].groupby(['user', 'day']).size().reset_index(name='numUploadDay')
    night_uploads = upload_data[~upload_data['is_working_hour']][['user', 'day']].groupby(['user', 'day']).size().reset_index(name='numUploadNight')

    combined_access = day_access.merge(night_access, on=['user', 'day'], how='outer')
    combined_downloads = day_downloads.merge(night_downloads, on=['user', 'day'], how='outer')
    combined_uploads = day_uploads.merge(night_uploads, on=['user', 'day'], how='outer')

    merged_data = combined_access.merge(combined_downloads, on=['user', 'day'], how='outer')
    merged_data = merged_data.merge(combined_uploads, on=['user', 'day'], how='outer')

    merged_data.fillna(0, inplace=True)  # Replace NaN with 0
    merged_data[['numWebAccDay','numWebAccNight','numDownloadsDay','numDownloadsNight','numUploadDay','numUploadNight']] = merged_data[['numWebAccDay','numWebAccNight','numDownloadsDay','numDownloadsNight','numUploadDay','numUploadNight']].astype(int)
    
    temp_filename = f'{temp_folder_results}/temp_result_{chunk_filename}'
    
    # # Because we are processing different chunks, a separate result file is generated for each chunk in temp_folder_chunks folder
    merged_data.to_csv(temp_filename, index=False)
    
    return temp_filename  # Return the filename of the saved result
    
    # return temp_filename  # Return the filename of the saved result


# In[40]:


# First we have to get the list of chunks that we have in the chunks folder
file_names = os.listdir(temp_folder_chunks)
# Filter only files (not directories)
chunk_filenames = [file for file in file_names if os.path.isfile(os.path.join(temp_folder_chunks, file))]

# chunk_filenames = ['temp_chunk_2010-01-09.csv','temp_chunk_2010-01-12.csv']

# Calculate the number of emails sent and received during day and night for each chunk
with Pool() as pool:
    result_filenames = pool.map(calculate_activity_counts, chunk_filenames)

# Since our results are divided into different files for each day, we have to combine them
combined_result = pd.concat([pd.read_csv(filename) for filename in result_filenames])

# Save the final result to a CSV file
combined_result.to_csv(output_file, index=False)


# In[41]:


# To remove the generated temp files
for filename in result_filenames:
    if os.path.exists(filename):  # Check if the file exists before removing
        os.remove(filename)
    else:
        print(f"File {filename} not found.")

