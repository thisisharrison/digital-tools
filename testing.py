

def testing(url, staging):

    staging = staging
    date_s = '202012311234'

    if ('?' not in url) and ('&' not in url):
        if staging == False:
            parsedUrl = url + '?sz=9999'
        else:
            parsedUrl = url + '?__siteDate=' + date_s + '&sz=9999'
    
        return parsedUrl
    
    if ('?sz' in url) and ('&' not in url):
        if staging == False:
            parsedUrl = url.replace('?sz=', '?sz=9999')
        else:
            split = url.split('?sz')
            parsedUrl = split[0] + '?__siteDate=' + date_s 
            extra_params = ('&sz' + ''.join(split[1:])).replace('&sz=', '&sz=9999')
            parsedUrl += extra_params
        
        return parsedUrl

    if ('?q=' in url) and ('&sz' not in url):
        if staging == False:
            parsedUrl = url + '&sz=9999'
        else:
            parsedUrl = url + '&__siteDate=' + date_s + '&sz=9999'
        return parsedUrl
    
    if ('?q=' in url) and ('&sz' in url):
        url = url.replace('&sz=', '&sz=9999')
        if staging == False:
            parsedUrl = url
        else:
            # Check
            parsedUrl = url + '&__siteDate=' + date_s
        return parsedUrl


    if ('?q=' in url) and ('&' in url):
        split = url.split('?')
        extra_params = '&'.join(split[1:])
        if staging == False:
            parsedUrl = url + extra_params + '&sz=9999'
        else:
            # Check
            parsedUrl = url + extra_params + '&__siteDate=' + date_s + '&sz=9999'
        return parsedUrl


    if ('?' in url) and ('&sz' not in url):
        if staging == False:
            parsedUrl = url + '&sz=9999'
        else:
            # split by '?'
            split = url.split('?')
            extra_params = '&'.join(split[1:])
            parsedUrl = split[0] + '?__siteDate=' + date_s + '&' + extra_params + '&sz=9999'
        
        return parsedUrl

    if ('?' in url) and ('&sz' in url): 
        url = url.replace('&sz=', '&sz=9999')
        if staging == False:
            parsedUrl = url
        else:
            split = url.split('?')
            extra_params = '&'.join(split[1:])
            parsedUrl = split[0] + '?__siteDate=' + date_s + '&' + extra_params
        return parsedUrl


    # # If search 
    # if '?q=' in url:
    #     split_url = url.split("&lang")
    #     lang = split_url[1].split("&")[0]
    #     split_url[0] += lang

    #     if '&' in split_url[1]:
    #         if 'sz' in split_url[1]:
    #             split_url[1] = split_url[1].replace('sz=', 'sz=9999')
    #             size_param = True
    #         more_param = True
    #     else:
    #         more_param = False
    #         size_param = False
        
    #     if staging and more_param and size_param:
    #         parsedUrl = split_url[0] + '&__siteDate=' + date_s + '&' + split_url[1]
    #     elif staging and more_param:
    #         parsedUrl = split_url[0] + '&__siteDate=' + date_s + '&' + split_url[1] + '&sz=9999'
    #     elif staging:
    #         parsedUrl = split_url[0] + '&__siteDate=' + date_s + '&sz=9999'
    #     else:
    #         parsedUrl = split_url[0] + '&sz=9999'

    #     print(parsedUrl)
    #     return
    
    # # If there's no params
    # if '?' not in url and '&' not in url:
    #     if staging: 
    #         parsedUrl = url + '?__siteDate=' + date_s + '&sz=9999'
    #     else:
    #         parsedUrl = url + '?sz=9999'
        
    #     print(parsedUrl)
    #     return

    

    # # If there's one param
    # if '?' in url:
    #     # split param
    #     split_url = url.split('?')
    #     # replace sz if sz in param
    #     if 'sz' in split_url[1]:
    #         split_url[1] = split_url[1].replace('sz=', 'sz=9999')
    #     else:
    #         split_url[1] += '&sz=9999'

    #     if staging: 
    #         parsedUrl = split_url[0] + '?__siteDate=' + date_s + '&' + split_url[1]
    #     else:
    #         parsedUrl = split_url[0] + '?' + split_url[1]

    #     print(parsedUrl)
    #     return
    

    
# u0 = "https://www.lululemon.com.au/en-au/c/women/collections/whats-new"
# u1 = "https://www.lululemon.com.au/en-au/c/women/collections/whats-new?sz=12"
# u2 = "https://www.lululemon.com.au/en-au/c/women/collections/whats-new?prefn1=styleNumber&prefv1=Full+Length+Tights"
# u3 = "https://www.lululemon.com.au/en-au/c/women/collections/whats-new?prefn1=styleNumber&prefv1=Full+Length+Tights&sz=12"
# u0 = "https://staging-eu01-lululemon.demandware.net/s/HK/en-hk/c/features/lululemon"
# u1 = "https://staging-eu01-lululemon.demandware.net/s/HK/en-hk/c/features/lululemon?prefn1=styleNumber&prefv1=Bags&sz=12"

# u0 = "https://www.lululemon.com.au/en-au/search?q=tshirt&lang=en_AU"
# u1 = "https://www.lululemon.com.au/en-au/search?q=tshirt&lang=en_AU&sz=24"
# u2 = "https://www.lululemon.com.au/en-au/search?q=tshirt&prefn1=styleNumber&prefv1=Short+Sleeve+Tops"
# u3 = "https://www.lululemon.com.au/en-au/search?q=tshirt&prefn1=styleNumber&prefv1=Short+Sleeve+Tops&sz=12"

u0 = "https://staging-eu01-lululemon.demandware.net/s/HK/en-hk/search?q=align"
u1 = "https://staging-eu01-lululemon.demandware.net/s/HK/en-hk/search?q=align&lang=en_HK"
u2 = "https://staging-eu01-lululemon.demandware.net/s/HK/en-hk/search?q=align&prefn1=size&prefv1=2&sz=12"



# https://staging-eu01-lululemon.demandware.net/s/HK/en-hk/search?q=wunder&lang=en_HK&__siteDate=202011100102&__sourceCode=&__customerGroup=&__abTest=&__abTestSegment=&__previewID=&sz=24