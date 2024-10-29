# assignment_three_algorithmic_redistricting

## List of Ohio Counties

https://ohioroster.ohiosos.gov/county_list.aspx

## County Adjacency

https://www2.census.gov/geo/docs/reference/county_adjacency.txt


## Assignment Checklist

✅ Obtain a complete list of counties for the selected state.

✅ Obtain demographic data relating to the total population and the percentage of the population that is white only in each county.  

✅ These data should come from the US Census of Population from 2020 or later. A summary list is provided at https://worldpopulationreview.com/us-countiesLinks to an external site.  

🛠️ If possible, gather data relating to past statewide elections, so you can see proportions of votes for Democratic versus Republican candidates. 

✅ Note counties that are geographically adjacent to one another: https://www2.census.gov/geo/docs/reference/county_adjacency.txtLinks to an external site.

🛠️ Set partitioning. Use integer programming (set partitioning) to obtain an algorithmic/optimal redistricting. Assign every county in your selected state to exactly one congressional district while striving to meet your objective through maximization or minimization.

🛠️ Population balance. Try to satisfy population balance (one-person-one-vote). That is, congressional districts should have approximately the same population. Consider strategies for assigning more than one representative to counties with high-population centers as long as elections are county-wide. Do not divide counties geographically.

🛠️Compact districts. Try to ensure that congressional districts geographically compact (are composed of counties that are adjacent to one another). Describe constraints or objectives employed to accomplish this goal. Note any difficulties encountered in setting up constraints or objectives.

🛠️Solve the integer programming problem using Python PuLP or AMPL.  Note any difficulties encountered, given the size of the integer programming problem.

🛠️Consider secondary goals of redistricting, such as encouraging equal representation across races. For example, you may try to achieve as much racial balance (percentage white alone versus other races) as possible across all congressional districts. Another secondary goal may be to ensure that the proportions of Democratic versus Republican representatives are approximately equal to the proportions of Democratic and Republican voters in recent statewide elections.

🛠️ Prepare a written report of your work. One paper per workgroup. Members of the workgroup will share a common grade on this assignment with the understanding that all workgroup members contribute to the work.