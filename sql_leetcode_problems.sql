

'''1587. Bank Account Summary II'''
https://leetcode.com/problems/bank-account-summary-ii/
# Write your MySQL query statement below


select u.name, 	
    sum(t.amount ) as balance
from users u 
left join transactions t on u.account = t.account 
group by u.name 
having sum(t.amount) > 10000; 


'''1633. Percentage of Users Attended a Contest'''
https://leetcode.com/problems/percentage-of-users-attended-a-contest/

with temp_temp as (
	select contest_id , 
		count(distinct user_id) as upper_things , 
		(select count(*) from users ) as lower_things
	from register
	group by contest_id 
) 
select contest_id , 
	round((upper_things / lower_things)*100), 2) as percentage
from temp_temp 
order by percentage desc , 
	contest_id ; 



https://leetcode.com/problems/average-time-of-process-per-machine/
'''1661. Average Time of Process per Machine'''

with start_table as (
	select machine_id, 
	activity_type , 
	timestamp 
	from activity
	where activity_type = 'start'
	), 
end_table as (
	select machine_id, 
	activity_type , 
	timestamp 
	from activity
	where activity_type = 'end'
	)  

select s.machine_id , 
	round(avg((s.timestamp - e.timestamp)),3) as processing_time 
from start_table s
inner join end_table e on s.machine_id = e.machine_id  
group by s.machine_id ; 
