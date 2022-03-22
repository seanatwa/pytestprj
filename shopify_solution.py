"""
Our company hosts search bars on a number of websites.
One of our important datasets is searches,
which has columns: search_id | site_id
The search_id is unique.
In the example below, two searches were made on the same site.
"""

searches = [
    {"search_id": 0, "site_id": 0},
    {"search_id": 1, "site_id": 0},
    {"search_id": 2, "site_id": 1},
    {"search_id": 3, "site_id": 2},
]

"""
The other important dataset is clicks,
which has columns search_id | position
In the example below:
- In query 0, only the top result was clicked
- In query 1, results in position 4 and 5 were clicked
"""

clicks = [
    {"search_id": 0, "position": 0},
    {"search_id": 1, "position": 4},
    {"search_id": 1, "position": 5},
    {"search_id": 2, "position": 3},
    {"search_id": 3, "position": 0},    
]


"""
We want to start measuring the following metric:
For each site, in what percent of queries:
- The top result was clicked (position 0) AND
- Nothing else was clicked
In our examples above, we have one site with two queries.
The first query only got a click on position 0, so it
contributes to this metric. The second query got clicks on
position 4 and 5, so it does not. The output would be:
"""

top_result_ctr = [
    {"site_id": 0, "pct": 0.5},
    {"site_id": 1, "pct": 0},
    {"site_id": 2, "pct": 1},   
]


''' 
###################################
Native solution 1
assumptions:
  - lists are not too big
  - No two 0 hit in the click data
################################### 
'''
def calculate_crt_single_site(aClicks):
  search_hit = 0
  for c in aClicks:
    search_hit += 1 if c["position"] == 0 else 0 
  
  search_count = len(set([c["search_id"] for c in aClicks]))
  
  return search_hit/search_count
  

test_input = [
    {"search_id": 0, "position": 0},
    {"search_id": 1, "position": 4},
    {"search_id": 1, "position": 5},
]
test_expected = 0.5
assert test_expected == calculate_crt_single_site(test_input)


def compute_ctr_1(aSearches, aClicks):  # assume O(m), O(n), result 0(m*(n+m)) = O(m^2)
  ret = list()
  
  sites = set([s["site_id"] for s in aSearches])  #O(m)
  for curr_site in sites: #O(m)
    curr_site_searches = [s["search_id"] for s in aSearches 
                          if s["site_id"] == curr_site] #O(m)
    curr_site_clicks = [c for c in aClicks 
                        if c["search_id"] in curr_site_searches] #O(n)
    curr_site_ctr = calculate_crt_single_site(curr_site_clicks)  #O(n)
    ret.append({"site_id": curr_site, 
                "pct": curr_site_ctr})
                
  return ret


assert top_result_ctr == compute_ctr_1(searches, clicks)


'''
###################################
Native solution 2
same as solution 1, but more compact with list comprehanstion
################################### 
'''
def calculate_crt_by_searchid(aClicks, aSearchIDs):
  search_hit = 0
  for c in aClicks:
    search_hit += 1 if c["search_id"] in aSearchIDs and c["position"] == 0 else 0 
  
  search_count = len(set([c["search_id"] 
                          for c in aClicks 
                          if c["search_id"] in aSearchIDs]))
  
  return search_hit/search_count
  
test_input_click = [
    {"search_id": 0, "position": 0},
    {"search_id": 1, "position": 4},
    {"search_id": 1, "position": 5},
]
test_input_searchid = [0, 1]
test_expected = 0.5
assert test_expected == calculate_crt_by_searchid(test_input, test_input_searchid)


def compute_ctr_2(aSearches, aClicks): 
  sites = set([s["site_id"] for s in searches])  #O(m)
  site_searches = [{'site_id': curr_site, 
                    'searches': [s["search_id"] 
                                 for s in searches 
                                 if s['site_id'] == curr_site]} 
                   for curr_site in sites]
  return [{'site_id': s['site_id'], 
          'pct': calculate_crt_by_searchid(clicks, s['searches']) } 
          for s in site_searches]

assert top_result_ctr == compute_ctr_2(searches, clicks)


'''
###################################
Pandas solution 1
###################################
'''
# solution of SQL
# solution of ph.merge


# Clicked position 0 and only position 0
searches = [{"search_id": 0, "site_id": 0}]
clicks = [{"search_id": 0, "position": 0}]
top_result_ctr = [{"site_id": 0, "pct": 1.0}]
#assert compute_ctr(searches, clicks) == top_result_ctr


# Test case 0_0
expected_top_result_ctr = []
assert expected_top_result_ctr == 
            compute_ctr([], 
                        []) 


# Test case 0_1
expected_top_result_ctr = []
assert expected_top_result_ctr == 
            compute_ctr([{"search_id": 0, "site_id": 0}], 
                        []) 


# Test case 0_2
expected_top_result_ctr = []
assert expected_top_result_ctr == 
            compute_ctr([], 
                        [{"search_id": 0, "position": 0}]) 
    

# Test case 1_1
expected_top_result_ctr = [{"site_id": 0, "pct": 1.0}]
#assert expected_top_result_ctr == 
            compute_ctr([{"search_id": 0, "site_id": 0}], 
                        [{"search_id": 0, "position": 0}]) 


# Test case 1_2
input_search = [{"search_id": 0, "site_id": 0},
               ]
input_click = [{"search_id": 0, "position": 0},
               {"search_id": 0, "position": 4},
               {"search_id": 0, "position": 5},
expected_top_result_ctr = [{"site_id": 0, "pct": 0.0}]
              ] 
assert expected_top_result_ctr == compute_ctr(input_search, input_click)) 


# Test case 1_3
# Same site, multiple searchies, both top
expected_top_result_ctr = [{"site_id": 0, "pct": 1.0}]
input_search = [{"search_id": 0, "site_id": 0},
                {"search_id": 1, "site_id": 0},
               ]
input_click = [{"search_id": 0, "position": 0},
               {"search_id": 1, "position": 0},
              ] 
assert expected_top_result_ctr == compute_ctr(input_search, input_click)) 


# Test case 1_4
# Same site, multiple searchies, 1 out 2 hit top
expected_top_result_ctr = [{"site_id": 0, "pct": 0.5}]
input_search = [{"search_id": 0, "site_id": 0},
                {"search_id": 1, "site_id": 0},
               ]
input_click = [{"search_id": 0, "position": 0},
               {"search_id": 1, "position": 4},
              ] 
assert expected_top_result_ctr == compute_ctr(input_search, input_click)) 
