# functions that return the parameters for each year and each month respectively 

import pandas as pd
import numpy as np
from weibull import Weibull

def yearly_params(first: int, last: int, dataframe: pd.DataFrame) -> pd.DataFrame:
    '''
    Returns a dataframe that has the parameters (estimated mit the MLE) for all the years in the intervall [start,end], 
    based on the dataframe that contains all our data
    '''

    # initialize a dataframe that has the years as indices
    yearly_df=pd.DataFrame()
    yearly_df['Years']=np.arange(first, last+1)
    yearly_df['param_lambda']=0.0
    yearly_df['param_beta']=0.0
    yearly_df.set_index('Years', inplace=True)

    # compute the parameters for each year
    for y in yearly_df.index:
        mask=dataframe['MESS_DATUM'].dt.year == y
        weibull=Weibull.estimate(dataframe[mask]['FF_10_wind'])
        yearly_df.loc[y, 'param_lambda' ]=weibull.lambd
        yearly_df.loc[y, 'param_beta' ]=weibull.beta

    return yearly_df


def monthly_params(first: int, last: int, dataframe: pd.DataFrame) -> pd.DataFrame:
    '''
    Returns a dataframe that has the parameters (estimated with the MLE) for all the months of the years in the intervall [start,end], 
    based on the dataframe that contains all our data
    '''

    # make a dataframe that has year-month combinations as indices
    months_range = pd.date_range(start=f'{first}-01', end=f'{last+1}-01', freq='M').to_period('M')
    monthly_df = pd.DataFrame(index=months_range, columns=['param_lambda', 'param_beta'])
    monthly_df['param_lambda']=0.0
    monthly_df['param_beta']=0.0
    # compute the parameters for all year-month combinations
    for m in monthly_df.index:
        mask=(dataframe['MESS_DATUM'].dt.month == m.month)& (dataframe['MESS_DATUM'].dt.year == m.year)
        weibull=Weibull.estimate(dataframe[mask]['FF_10_wind'])
        monthly_df.loc[m, 'param_lambda' ]=weibull.lambd
        monthly_df.loc[m, 'param_beta' ]=weibull.beta

    return monthly_df


def bf_classifier(data):
    '''
    classifies the input according to the Beaufort-scale
    '''

    if data >24.5:
        return 10
    elif data >20.8:
        return 9
    elif data >17.2:
        return 8
    elif data >13.9:
        return 7
    elif data >10.8:
        return 6
    elif data >8.0:
        return 5
    elif data >5.5:
        return 4
    elif data >3.4:
        return 3
    elif data >1.6:
        return 2
    elif data >0.3:
        return 1
    else:
        return 0
    

def snh_test( X: np.array) -> list:
   '''
   Computes the test statistic of the standard normal homogeneity test for the given data X
   '''
   Y=np.array(X)
   s=Y.std()
   m=Y.mean()
   T=[]
   for k in range (0, len(Y)):
       z_1= 0 
       for i in range (0, k+1):
           z_1=z_1+(Y[i]- m)/s
       z_1=z_1/(k+1)
       
       z_2= 0 
       for i in range (k+1, len(Y)):
           z_2=z_2+(Y[i]- m)/s
       z_2=z_2/(len(Y) - (k))


       T.append(k*z_1**2 + (len(Y) -k)*z_2**2)
   return T


def pettitt_test( X: np.array) -> list:
   '''
   Computes the test statistic of the pettitt test for the given data X
   '''
   Y=np.array(X)
   R=np.argsort(Y)
   T=[]
   x_k=0
   for k in range(0, len(R)):
      x_k=0
      for i in range(0,k):
         x_k=x_k + 2*(R[i]+1)
      
      x_k=x_k-(k+1)*(len(R)+1)
      T.append(np.abs(x_k))
   return T

arr=np.array([1,1,0.8,1.2,11,10,10,10.2,10.1,10,1,1,0.8,1,1,1,])

from matplotlib import pyplot as plt
plt.plot(pettitt_test(arr))
plt.show()

   


