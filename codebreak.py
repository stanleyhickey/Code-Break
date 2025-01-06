#!/usr/bin/env python
# coding: utf-8

# In[8]:


from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np


def dftable(url: str) -> None:
    
        
    response = requests.get(url)
    response.raise_for_status()
    content = response.text
   
    
    soup = BeautifulSoup(content, "html.parser")
    headers = {"x-coordinate", "Character", "y-coordinate"}

    
    for table in soup.find_all("table"):
        match = [cell.get_text().strip() for cell in table.find("tr").find_all("td")]
        if set(match) == headers:
            data = [
                [cell.get_text().strip() for cell in row.find_all("td")]
                for row in table.find_all("tr")[1:]  # Skip header row
                if len(row.find_all("td")) == 3  # Filter incomplete rows
            ]
    df = pd.DataFrame(data, columns=match)
    

    df["x-coordinate"] = df["x-coordinate"].astype(int)
    df["y-coordinate"] = df["y-coordinate"].astype(int)
    x_dim = (df['x-coordinate'].max())
    y_dim = (df['y-coordinate'].max())
    grid = np.full((y_dim + 1, x_dim + 1), " ", dtype=str)
    
    # Place characters
    for _, row in df.iterrows():
        grid[y_dim - row["y-coordinate"], row["x-coordinate"]] = row["Character"]
        
    

    
    for row in grid:
        print("".join(row))

    
url = "https://docs.google.com/document/d/e/2PACX-1vShuWova56o7XS1S3LwEIzkYJA8pBQENja01DNnVDorDVXbWakDT4NioAScvP1OCX6eeKSqRyzUW_qJ/pub"
dftable(url)


# In[ ]:




