
def get_page(url):
    try:
        import urllib3
        http = urllib3.PoolManager()
        r = http.request('GET', url) 
        return r.data
    except:
        return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote +1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

#links = get_all_links(get_page("http://www.udacity.com/cs101x/index.html"))

def union(a,b):
    for bb in b:
        if bb not in a:
            a.append(bb)
    #return a

def crawl_web(seed,max_depth):
    tocrawl = [seed]
    crawled = []
    next_depth =[]
    depth = 0
    index = []
    while tocrawl and depth <= max_depth:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index,page,content)
            union(next_depth, get_all_links(content))
            crawled.append(page)
        if not tocrawl:
            tocrawl, next_depth = next_depth, []
            depth = depth + 1
    return index

#print crawl_web('http://www.udacity.com/cs101x/index.html',100)
#print crawl_web('http://news.yahoo.com/',4)

# index will be a structure like
#           [ [<keyword>, [<url>,count][<url>,count][...]], ...] 
def add_to_index(index,keyword,url):
    for entry in index:
        if entry[0] == keyword:
            for element in entry[1]:
                if element == url:
                    return
            entry[1].append([url,0])
            return
    index.append([keyword,[url,0]])

def lookup(index,keyword):
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
    return []


def add_page_to_index(index,url,content):
    words = content.split()
    for word in words:
        add_to_index(index,word,url) 

def split_string(source,splitlist):
    output = []
    atsplit = True
    for char in source:
        if char in splitlist:
            atsplit = True
        else:
            if atsplit:
                output.append(char)
                atsplit = False
            else:
                output[-1] = output[-1] + char
    return output

def record_user_click(index, keyword, url):
    urls = lookup(index, keyword)
    if urls:
        for entry in urls:
            if entry[0] == url:
                entry[1] = entry[1]+1

def hash_string(keyword, buckets):
    h = 0
    for c in keyword:
        h = (h + ord(c)) % buckets
    return h

#print hash_string("ua",12)
#print hash_string("udacity",12)

def make_hashtable(nbuckets):
    table = []
    for unused in range(0,nbuckets):
        table.append([])
    return table

def hashtable_get_bucket(htable,key):
    return htable[hash_string(key, len(htable))]

def hashtable_add(htable, key, value):
    hashtable_get_bucket(htable, key).append([key,value])

def hashtable_lookup(htable,key):
    bucket = hashtable_get_bucket(htable, key)
    for entry in bucket:
        if entry[0] == key:
            return entry[1]
    return None

def hashtable_update(htable,key, value):
    bucket = hashtable_get_bucket(htable, key)
    for entry in bucket:
        if entry[0] == key:
            entry[1] = value
            return
    bucket.append([key,value])



#print make_hashtable(3)

index=[]
add_page_to_index(index,'fake.test',"This is a test")
#print index

add_page_to_index(index,'not.test',"This is not a test")
#print index










