import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
df=pd.read_csv(r'C:\Users\DELL\Desktop\NetworkSecurity\network_data\Phishing_Websites_Data.csv')
X=df.drop("Result",axis=1)
y=df["Result"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
test_df=pd.DataFrame(data=X_test)
test_df.to_csv('test.csv')
