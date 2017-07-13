import re
import json
from difflib import SequenceMatcher





# remove some specific chars from a text
def preprocess(text):
    return re.sub('[-_,;\'"]', ' ', text)






# try to find if txt2 contains exact words of txt1 (order of the words is not considered)
def text_match(txt1, txt2):
    # preprocess texts
    txt1 = preprocess(txt1)
    txt2 = preprocess(txt2)
    # remove spaces and set texts to lower case
    txt1 = txt1.strip().lower()
    txt2 = txt2.strip().lower()
    # add spaces to textes in the begin/end (" "+text+" "),
    # This will make sure to find the exact match (e.g. 'W560FB'.count('W560') = 1 this is wrong  but '_W560FB_'.count('_W560_') = 0: that's correct)
    txt2 = " "+txt2+" "
    # convert text1 to list of words
    txt1_list = txt1.split(" ")
    # check if all words of text1 exists into text2, if so return 1 or 0
    for word in txt1_list:
        # if there is only one word doesn't exists return 0
        if(txt2.count(" "+word+" ")==0):
            return 0
    # return 1 if all words from product exists into listing record
    return 1






# this function takes products and listings files and generate the output JSON file
def generate_matches(products_file, listings_file, result_file="result.json"):
    
    # get data from the files as Python lists
    try:
        products_lines = [line.rstrip('\n') for line in open(products_file, encoding="utf8")]
        prices_lines = [line.rstrip('\n') for line in open(listings_file, encoding="utf8")]
    except FileNotFoundError:
        print("Error: File not found, please make sure to choose correct filname")
        return
    
    # init counters
    index_product = 0 # products lines count
    nbr_matches = 0 # number of matches count
    
    # create result JSON file
    file = open(result_file, "w", encoding="utf8")
    
    # loop on each product and check if there is a match to that product in the listings lines
    for product in products_lines:
        match_exists = False # flag used to show matching results in console
        # conver string to dictionary
        product_json = json.loads(product)
        
        # remove special chars
        product_name = product_json.get('product_name')
        product_name = preprocess(product_name)

        # print trace
        print(str(index_product)+" : ==> Processing: "+product_name)
        index_listing = 0 # listing index

        # loop on each listing line and try to find a match to the product for the above loop elements
        for price in prices_lines:
            # convert string to dictionary
            price_json = json.loads(price)
            # remove special chars
            product_title = price_json.get('title')
            # add manufacturer name to the string (give more chance to find a match)
            product_title += " "+price_json.get('manufacturer')
            # preprocess title
            product_title = preprocess( product_title)
            
            # if there is a match, merge dicts and put them into JSON as a line
            if(text_match(product_name,  product_title)>0):
                # increase nbr of matches
                nbr_matches+=1
                # print trace
                print("+++ Match found: "+product_title)
                # merge price and product dictionary to form a json object
                product_price = {**product_json, **price_json}
                # put merged dicts in a JSON file line
                json.dump(product_price, file,  ensure_ascii=False)
                file.write('\n')
                match_exists = True
                # break when you find a match
                break;
            
            # increase listings index 
            index_listing+=1
        # increment products index
        index_product+=1
        # print trace if there is no match
        if(not(match_exists)):
            print("--- No match found")
        print("\n____________________________________________________\n")

    # close JSON file
    file.close()
    # print total matches found
    print("Total matches: "+str(nbr_matches))





# main function
def main():
    # call generate matches function to generate output file
    generate_matches('products.txt', 'listings.txt')



# call main function
main()
