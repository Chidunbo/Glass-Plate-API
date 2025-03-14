import time
import requests

# It's good to know how long this takes, becuase you'll want
# to make sure your API queries can complete in a reasonable
# amount of time (days, not months)
startTime = time.time()

# you can get plate numbers (which is a series designation plus a number) here
# https://library.cfa.harvard.edu/plate-series
# So for the a series, you can see that tehre's a list of numbers going
# from 1 to 27504 from this:
# http://dasch.rc.fas.harvard.edu/HistoryOfPlateSeries/History01.jpg
plate_id = 'a00001'

#For a project, I'd have to loop over all the plates or a subset of a plates with this query
address = "https://api.starglass.cfa.harvard.edu/public/plates/p/" + plate_id 
response = requests.get(address)

# The unparsed json response:
print(response.json())
# You can learn what the keywords are from this website:
# https://starglass.cfa.harvard.edu/docs/api/plates.html#plate-response-object

# You would then want to write code that pulls out the elements of interest to you 
# and saves them.

print(f"\nScript took {time.time() - startTime} seconds to run.") 
# make sure your project doesn't take > 10 days of time to run