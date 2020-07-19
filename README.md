# Final

Web Programming with Python and JavaScript

# Scraper for QA websites and get Image status 

## Use cases 
> As a digital operation specialist, I would like to check instantly if products have images, or else they cannot be merchandised to ecommerce website. 

> As a merchandiser, I would like to know the same information to know whether arrived products should be transferred to retail stores instead. 

> As a digital operation specialist and buyer, I would like to know if the prices are correct in the ecommerce site. 

> As a visual merchandiser, I would like to know the assortment and order currently on a Category Display Page (CDP). 

> As a content operation specialist and a quality assurer, I would like to know the information on the site without opening hundreds of tabs. 

> As a localization team member, I would like to find out what products and attributes are translated.

## Stack
The website utilizes Flask with Celery and Redis to handle long time processing tasks to free up users' time. 

Scraping functions use requests and BeautifulSoup. 

I also use Websockets to check pending tasks in Celery and update user when their new task is ready. 

Styling is done with Boostrap. 

## Features
### Image Function
This page takes users' input of company's style colors, modify to image url structure, and send the request to get a status code. If image status returns 200, it means image exists. If image status returns 403, it means image does not exist for the style.

### PDP Function (Product Display Page)
This page takes users' input of website IDs (Masters and SKUs), modify to product url structure, and send request to scrape the page. Using BS4, the function checks specific CSS class fields and get their `text`. 

### CDP Function (Category Display Page)
This page takes users' input of a CDP page, modify to inspect larger amount of products, and get products' URL and name. 

### Celery
Using celery, longer tasks or higher amount of queries can be queued on Redis. User can continue to use other functions or wait for their tasks' status to turn `SUCCESS`. 

### Scale
I am using Flask Session to store users' tasks. They're able to share tasks' results but will not see other people's tasks. 

Sessions are cleared when current UTC day is larger than previous user's access day. 