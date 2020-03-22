import requests
import json
import bs4
import urllib
import progress.bar



def checkRecall(UPC):
    '''
    Parses CFIA recalls for UPC. Returns recall link if found, else none.
    '''

    cfia_url = 'https://www.inspection.gc.ca/food-recall-warnings-and-allergy-alerts/eng/1351519587174/1351519588221'

    soup = bs4.BeautifulSoup(urllib.request.urlopen(cfia_url), 'html.parser')
    table = soup.find('tbody')

    recall_urls = []
    rows = table.findChildren('tr')
    for row in rows:
        recall_url = row.find('a')['href']
        recall_url = 'https://www.inspection.gc.ca/'+recall_url
        recall_urls.append(recall_url)
    
    bar = progress.bar.Bar('Searching CFIA', max=len(recall_urls))
    for recall_url in recall_urls:
        soup = bs4.BeautifulSoup(urllib.request.urlopen(recall_url), 'html.parser')

        table = soup.find('table', attrs={'class':'table table-bordered table-condensed'}).find('tbody')

        rows = table.findChildren('tr')

        for row in rows:
            if row.findChildren('th'):      # check if bolded first row header is found
                col = 2
            else:
                col = 3

            UPC_recall = row.findChildren('td')[col].text.strip().replace(u'\xa0', '').replace(' ', '')

            if UPC == UPC_recall:
                bar.finish()
                return recall_url

            elif 'Startswith' in UPC_recall:
                UPC_recall_trim = UPC_recall[10:]

                if UPC_recall_trim in UPC:
                    bar.finish()
                    return recall_url
            
            elif 'Noneor' in UPC_recall:
                UPC_recall = UPC_recall[6:]
                if UPC == UPC_recall:
                    bar.finish()
                    return recall_url
            
        
        bar.next()
    bar.finish()

    return None


def UPCLookup(UPC):
    '''
    Gets product data from online database. Use for autocomplete purposes.
    Returns none if no match is found.
    '''

    params = {
        'barcode':UPC,
        'key':'sznnc8pmbtfg2dcpcvdpn8uiibogrg'    
    }

    response = requests.get('https://api.barcodelookup.com/v2/products', params)

    if response.status_code != 404:
        product = response.json()['products'][0]
        return product
    else:
        return None


if __name__ == '__main__':
    UPC = input('Enter UPC: ')

    print('Retrieving data for {}...'.format(UPC))
    product = UPCLookup(UPC)

    if product:
        print('--Product Data--')
        print('Name:', product['product_name'])
        print('Brand:', product['brand'])
        print('Manufacturer:', product['manufacturer'])
        print('Category:', product['category'])
        print('Weight:', product['description'])
        print('Image:', product['images'][0])
    else:
        print('No data found.')


    url = checkRecall(UPC)
    print('Status: No recall found') if url == None else print('Status: WARNING! POTENTIAL RECALL: {}'.format(url))




    
    


