import pandas as pd
from daftlistings import Daft, Location, SearchType, PropertyType, SortType, MapVisualization
import re


def get_postcode(listing):
    regex_search = "([Dd]ublin ?[12]?[1-9]|[Cc]o\.? ?[Dd]ublin|[Dd][12]?[1-9])"

    x = re.search(regex_search, listing.title)
    if x is not None:
        return x.group()
    else:
        return "N/A"


def dist_to_city_center(listing):
    dublin_castle_coords = [53.3429, -6.2674]
    return listing.distance_to(dublin_castle_coords)


def floor_area(listing):
    try:
        if listing.as_dict["floorArea"]["unit"] != "METRES_SQUARED":
            return "N/A"
        else:
            return listing.as_dict["floorArea"]["value"]
    except KeyError as e:
        return "N/A"


daft = Daft()
daft.set_location(Location.DUBLIN_CITY)
daft.set_search_type(SearchType.RESIDENTIAL_SALE)
daft.set_sort_type(SortType.PRICE_ASC)
daft.set_max_price(500000)

listings = daft.search()

df = pd.DataFrame()

df['title'] = [d.title for d in listings]
df['longitude'] = [d.longitude for d in listings]
df['latitude'] = [d.latitude for d in listings]
df['price'] = [d.price for d in listings]
df['size'] = [floor_area(d) for d in listings]
df['post_area'] = [get_postcode(d) for d in listings]
df['dist_to_city_center'] = [dist_to_city_center(d) for d in listings]
df['link'] = [d.daft_link for d in listings]

print(df)

# # cache the listings in the local file
# with open("result.txt", "w") as fp:
#     fp.writelines("%s\n" % listing.as_dict_for_mapping() for listing in listings)
#
# # read from the local file
# with open("result.txt") as fp:
#     lines = fp.readlines()
#
# properties = []
# for line in lines:
#     properties.append(eval(line))
#
# df = pd.DataFrame(properties)
# print(df)
#
df.to_csv("output.csv")
