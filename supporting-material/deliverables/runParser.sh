python skeleton_parser.py ebay_data/items-*.json

sort -u items.dat -o items_sorted.dat
sort -u bidders.dat -o bidders_sorted.dat
sort -u sellers.dat -o sellers_sorted.dat
sort -u bids.dat -o bids_sorted.dat
sort -u categories.dat -o categories_sorted.dat