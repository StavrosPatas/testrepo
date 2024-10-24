#!/usr/bin/env python
# coding: utf-8

# In[2]:


import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta
import os


# In[3]:


# Function to parse the XML file and extract data
def xml_to_csv(xml_file_path, output_csv_path):
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Extract the required values
    bid_time_interval = root.find('BidTimeInterval').attrib['v']  # Constant value in every row
    document_id = root.find('DocumentIdentification').attrib['v']
    sender_id = root.find('SenderIdentification').attrib['v']
    receiver_id = root.find('ReceiverIdentification').attrib['v']
    bid_id = root.find('AllocationTimeSeries/BidIdentification').attrib['v']
    auction_id = root.find('AllocationTimeSeries/AuctionIdentification').attrib['v']
    contract_id = root.find('AllocationTimeSeries/ContractIdentification').attrib['v']
    in_area = root.find('AllocationTimeSeries/InArea').attrib['v']
    out_area = root.find('AllocationTimeSeries/OutArea').attrib['v']

    # Get the start and end times for the BidTimeInterval (used in the original method)
    start_time_str, end_time_str = bid_time_interval.split('/')
    start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%MZ")
    end_time = datetime.strptime(end_time_str, "%Y-%m-%dT%H:%MZ")

    # Calculate hourly intervals between start and end times
    interval_duration = timedelta(hours=1)

    # Extract all intervals
    intervals = root.findall('AllocationTimeSeries/Period/Interval')

    # Prepare the data for the CSV
    data = []
    current_time = start_time

    for interval in intervals:
        # Extract the 'v' attribute values from the XML
        pos = interval.find('Pos').attrib['v'] if interval.find('Pos') is not None else ""
        qty = interval.find('Qty').attrib['v'] if interval.find('Qty') is not None else ""
        price_amount = interval.find('PriceAmount').attrib['v'] if interval.find('PriceAmount') is not None else ""
        bid_qty = interval.find('BidQty').attrib['v'] if interval.find('BidQty') is not None else ""
        bid_price_amount = interval.find('BidPriceAmount').attrib['v'] if interval.find('BidPriceAmount') is not None else ""
        
        # Create a row with extracted values
        row = {
            'Bid Time Interval': bid_time_interval,  
            'Document ID': document_id,
            'Auction ID': auction_id,  
            'Contract ID': contract_id,  
            'Sender ID': sender_id,
            'Receiver ID': receiver_id,
            'Bid ID': bid_id,
            'In Area': in_area,
            'Out Area': out_area,
            'Position': pos,  
            'Quantity': qty,
            'Price Amount': price_amount,
            'Bid Quantity': bid_qty,
            'Bid Price Amount': bid_price_amount
        }
        
        # Append row to the data list
        data.append(row)

    # Create a DataFrame from the data
    df = pd.DataFrame(data)

    # Save the DataFrame to CSV
    df.to_csv(output_csv_path, index=False)


# In[4]:


# Function to process all XML files in the current folder
def process_all_xml_in_folder():
    # Get the folder where the executable/script is located
    folder_path = os.getcwd()  # Get current working directory
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xml'):
            xml_file_path = os.path.join(folder_path, file_name)
            # Use the same name as the XML file but with a .csv extension
            output_csv_path = os.path.join(folder_path, file_name.replace('.xml', '.csv'))
            xml_to_csv(xml_file_path, output_csv_path)
            print(f"Processed: {file_name} -> {output_csv_path}")


# In[5]:


# Run the function to process all XML files
process_all_xml_in_folder()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




