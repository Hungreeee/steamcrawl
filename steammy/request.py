import requests
import json
import pandas as pd
import warnings

from steammy.exceptions import exception

warnings.simplefilter(action = "ignore", category = RuntimeWarning)

class Steammy:

  def __init__(self):
    self.headers = {
      'Cookie': ''
    }
    self.listings_api = 'https://steamcommunity.com/market/search/render/?search_descriptions=0&norender=1'
    self.appid_api = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
    self.pricehistory_api = 'https://steamcommunity.com/market/pricehistory/'
    self.listingshistory_api = 'https://steamcommunity.com/market/myhistory/render/?norender=1'
    self.appdetails_api = 'https://store.steampowered.com/api/appdetails/'


  def set_steam_auth(self, steamLoginSecure: str):
    """
    """
    exception('type', steamLoginSecure, str, "Input steamLoginSecure it not a valid string type.")
    header = 'steamLoginSecure=' + steamLoginSecure + ';'
    testApi = 'https://steamcommunity.com/market/pricehistory/?appid=730&market_hash_name=P90%20%7C%20Blind%20Spot%20(Field-Tested)'
    requestObject = requests.get(testApi, headers={'Cookie': header}, timeout=1.0).content
    exception('network', requestObject, [], "Input header it not an authorized cookie header.")
    self.headers['Cookie'] = header


  def __request_helper(self, api: str, params: dict, headers: dict, index: list):
    """
    """
    dfGather = []
    requestObject = requests.get(api, params=params, headers=headers, timeout=1.0)
    contentObject = json.loads(requestObject.content)

    for i in index:
      if i in contentObject:
        if contentObject[i] != []:
          dfGather.append(contentObject[i])

    if 'success' in contentObject:
      isSuccess = contentObject['success']
      exception('network', isSuccess, False, "Steam cannot make this API call. Please double check your parameters and try again.")
    
    if 'total_count' in contentObject and 'count' in params:
      maxPage = contentObject['total_count']
      exception('exceed', params['count'], maxPage, f"{params['count']} is larger than the maximum number of count {maxPage}.")

    return dfGather

  def get_all_listings(self, sortby: str='default', sortdir: str='desc', appid: str='', count: int=100):
    """
    """
    exception('type', sortby, str, "Input sortby it not a valid string type.")
    exception('type', sortdir, str, "Input sortdir it not a valid string type.")
    exception('type', count, int, "Input count it not a valid integer type.")
    exception('type', appid, str, "Input appid it not a valid string type.")
    exception('contain', sortby, ['default', 'price', 'quantity', 'name'], 
      f"{sortby} is not valid as a sortby type. It should only be 'default', 'price', 'quantity', or 'name'.")
    exception('contain', sortdir, ['desc', 'asc'], 
      f"{sortdir} is not valid as a sortby type. It should only be 'desc' or 'asc'.")
    if appid != '':
      exception('contain', int(appid), list(self.get_all_appid()['appid']), 
        f"{appid} is not a valid appid. Please check the complete list using get_all_appid().")
    
    params = {
      'sortcolumn': sortby,
      'sortdir': sortdir,
      'appid': appid,
      'start': 0, 
      'count': count
    }

    jsonObject = self.__request_helper(self.listings_api, params, self.headers, ['results'])[0]

    if count == 0:
      return pd.DataFrame()
    
    if count <= 100: 
      return pd.json_normalize(jsonObject)
    
    else:
      remainCount = count % 100
      params['count'] = 100
      dfCombined = []

      for i in range(0, count - remainCount, 100):
        params['start'] = i
        jsonObject = self.__request_helper(self.listings_api, params, self.headers, ['results'])[0]
        dfCombined.append(pd.json_normalize(jsonObject))

      if remainCount == 0:
        return pd.concat(dfCombined, ignore_index=True)
      
      else:
        params['count'] = remainCount
        jsonObject = self.__request_helper(self.listings_api, params, self.headers, ['results'])[0]
        dfCombined.append(pd.json_normalize(jsonObject))
        return pd.concat(dfCombined, ignore_index=True)
    

  def get_all_appid(self):
    """
    """
    jsonObject = self.__request_helper(self.appid_api, {}, self.headers, ['applist'])[0]['apps']
    return pd.json_normalize(jsonObject)
  
  
  def get_app_details(self, appid: str):
    """
    """
    exception('type', appid, str, "Input appid it not a valid string type.")
    if appid != '':
      exception('contain', int(appid), list(self.get_all_appid()['appid']), 
        f"{appid} is not a valid appid. Please check the complete list using get_all_appid().")
      
    params = {
      'appids': appid
    }

    jsonObject = self.__request_helper(self.appdetails_api, params, self.headers, [appid])[0]['data']
    return pd.json_normalize(jsonObject)
  

  def get_price_history(self, item_name: str, appid: str):
    """
    """
    exception('type', item_name, str, "Input item_name it not a valid string type.")
    exception('type', appid, str, "Input appid it not a valid string type.")
    exception('network', self.headers['Cookie'], '', 
      "Cookie not authorized. Please set your steamLoginSecure first using set_steam_auth().")
    if appid != '':
      exception('contain', int(appid), list(self.get_all_appid()['appid']), 
        f"{appid} is not a valid appid. Please check the complete list using get_all_appid().")

    params = {
      'appid': appid,
      'market_hash_name': item_name
    }

    jsonObject = self.__request_helper(self.pricehistory_api, params, self.headers, ['prices'])[0]
    df = pd.read_json(json.dumps(jsonObject))
    df[0] = df[0].apply(lambda x: x[0:11])
    pd.to_datetime(df[0], format='%b %d %Y')
    df = df.set_axis(['date', 'median_price', 'volume_sold'], axis=1, copy=False)
    return df

  def __market_history_helper(self, index: list):
    """
    """
    dfCombinedAssets = []
    dfCombinedEvents = []
    dfCombinedListings = []
    dfCombinedPurchases = []

    for key in index[0]:
      gameJsonObject = index[0][key]
      for contextid in gameJsonObject:
        itemJsonObject = gameJsonObject[contextid]
        for listingid in itemJsonObject:
          dfCombinedAssets.append(pd.json_normalize(itemJsonObject[listingid]))
    dfCombinedAssets = pd.concat(dfCombinedAssets)
    dfCombinedAssets.rename({'id': 'asset.id'}, axis=1, inplace=True)
    dfCombinedAssets = dfCombinedAssets.drop(['currency', 'background_color'], axis=1)

    dfCombinedEvents = pd.json_normalize(index[1])
    dfCombinedEvents = dfCombinedEvents.drop(['time_event_fraction', 'date_event'], axis=1)
    dfCombinedEvents = dfCombinedEvents.replace({'event_type': {1: 'List', 2: 'Cancel', 3: 'Sold', 4: 'Buy'}})

    dfCombinedEvents['time_event'] = pd.to_datetime(dfCombinedEvents['time_event'], unit='s')

    for key in index[2]:
      dfCombinedListings.append(pd.json_normalize(index[2][key]))
    dfCombinedListings = pd.concat(dfCombinedListings)
    dfCombinedListings = dfCombinedListings.drop(['currencyid', 'asset.contextid', 'asset.appid', 'asset.currency', 'steam_fee', 'publisher_fee', 'publisher_fee_percent', 'publisher_fee_app', 'price', 'fee', 'asset.amount', 'original_price'], axis=1)

    if len(index) == 4:
      for key in index[3]:
        dfCombinedPurchases.append(pd.json_normalize(index[3][key]))
      dfCombinedPurchases = pd.concat(dfCombinedPurchases)
      dfCombinedPurchases = dfCombinedPurchases.drop(['asset.id', 'asset.appid', 'needs_rollback', 'purchaseid', 'steam_fee', 'publisher_fee', 'publisher_fee_percent', 'publisher_fee_app', 'received_amount', 'received_currencyid', 'asset.appid', 'asset.appid', 'asset.classid', 'asset.new_contextid', 'asset.new_id', 'asset.instanceid', 'asset.amount', 'asset.status'], axis=1)
      dfCombinedPurchases['total_paid'] = dfCombinedPurchases['paid_amount'] + dfCombinedPurchases['paid_fee'] 
      dfCombinedPurchases['time_sold'] = pd.to_datetime(dfCombinedPurchases['time_sold'], unit='s')
      dfCombined = pd.merge(dfCombinedAssets, 
                            pd.merge(dfCombinedEvents, 
                                      pd.merge(dfCombinedListings, dfCombinedPurchases, 
                                                how='outer', on=['listingid']), 
                                      how='outer', on=['listingid']), 
                            how='outer', on=['asset.id'])
      return dfCombined
    
    else:
      dfCombined = pd.merge(dfCombinedAssets, 
                            pd.merge(dfCombinedEvents, dfCombinedListings, 
                                      how='outer', on=['listingid']), 
                            how='outer', on=['asset.id']) 
      return dfCombined


  def get_market_history(self, count: int):
    """
    """
    exception('type', count, int, "Input count it not a valid integer type.")
    exception('network', self.headers['Cookie'], '', 
      "Cookie not authorized. Please set your steamLoginSecure first using set_steam_auth().")
    
    params = {
      'start': 0,
      'count': count
    }

    jsonObjectList = self.__request_helper(self.listingshistory_api, params, self.headers, ['assets', 'events', 'listings', 'purchases'])

    if count == 0:
      return pd.DataFrame()
    
    if count <= 100: 
      return self.__market_history_helper(jsonObjectList).reset_index(drop=True)
    
    else:
      remainCount = count % 100
      params['count'] = 100
      dfCombined = []

      for i in range(0, count - remainCount, 100):
        params['start'] = i
        jsonObjectList = self.__request_helper(self.listingshistory_api, params, self.headers, ['assets', 'events', 'listings', 'purchases'])
        dfCombined.append(self.__market_history_helper(jsonObjectList))
      
      if remainCount == 0:
        return pd.concat(dfCombined).reset_index(drop=True)
      
      else:
        params['count'] = remainCount
        jsonObjectList = self.__request_helper(self.listingshistory_api, params, self.headers, ['assets', 'events', 'listings', 'purchases'])
        dfCombined.append(self.__market_history_helper(jsonObjectList))
        return pd.concat(dfCombined).reset_index(drop=True)
  
