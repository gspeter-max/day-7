
'''1661. Average Time of Process per Machine'''
https://leetcode.com/problems/average-time-of-process-per-machine/
import pandas as pd

def get_average_time(activity: pd.DataFrame) -> pd.DataFrame:
    start_df = activity[activity['activity_type'] == 'start']
    end_df = activity[activity['activity_type'] == 'end']

    merge_df = pd.merge(
        start_df , 
        end_df , 
        on = 'machine_id', 
        how = 'inner'
    )
    merge_df['difference'] = (merge_df['timestamp_y'] - merge_df['timestamp_x'])
    merge_df  = merge_df.groupby('machine_id')['difference']. agg('mean').reset_index() 
    merge_df.columns = ['machine_id','processing_time']
    merge_df['processing_time'] = merge_df['processing_time'].round(3)
    return merge_df 

'''1633. Percentage of Users Attended a Contest'''
https://leetcode.com/problems/percentage-of-users-attended-a-contest/

import pandas as pd

def users_percentage(users: pd.DataFrame, register: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    counts = users['user_id'].count()
    df = register.groupby('contest_id')['user_id'].nunique().reset_index() 
    df.columns = ['contest_id','count_users']
    df['percentage'] = ((df['count_users']/counts)*100).round(2)
    df = df.sort_values(
        by = ['percentage','contest_id'], 
        ascending = [False,True]
    )
    return df[['contest_id','percentage']]



'''1587. Bank Account Summary II'''
https://leetcode.com/problems/bank-account-summary-ii/

import pandas as pd

def account_summary(users: pd.DataFrame, transactions: pd.DataFrame) -> pd.DataFrame:
    df = transactions.groupby('account')['amount'].agg('sum').reset_index() 
    df.columns = ['account','balance']
    merge = pd.merge(
        df, 
        users, 
        on = 'account'
    )
    merge = merge[merge['balance'] > 10000]
    return merge[['name','balance']]
