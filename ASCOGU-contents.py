import requests
import json
import pandas as pd
import time
from io import BytesIO
from PIL import Image
from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor
import os
from zipfile import ZipFile
headers = {
    'Accept': '*/*',
    'Authorization': 'eyJraWQiOiJEdUdJYVBFRjZVUWtZRC0xRDBLNF8yRDhGWHJ1N2IwbmNoRThOWE9NM3ZvIiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULmo3d1N2eU5FYlRBeGlpZzhDck83SS1HUjAtUzViMnBMWGxSSHh0UzNFdnMiLCJpc3MiOiJodHRwczovL3NpZ25pbi5hc2NvLm9yZy9vYXV0aDIvYXVzMWdvYXA1blEzM3ZvN0EyOTciLCJhdWQiOiJhcGk6Ly9kZWZhdWx0IiwiaWF0IjoxNzA4NTg1Mjc1LCJleHAiOjE3MDg2NzE2NzUsImNpZCI6IjBvYTZtOG53bnA5dDhTMHd3Mjk3IiwidWlkIjoiMDB1bWd6ZGZ5dDA3R2NOUUIyOTciLCJzY3AiOlsiZW1haWwiLCJwcm9maWxlIiwib3BlbmlkIl0sImF1dGhfdGltZSI6MTcwODU4NTI3NCwic3ViIjoicm9zaGFuLm11cmFsaUB6b29tcnguY29tIiwiRW1haWwiOiJyb3NoYW4ubXVyYWxpQHpvb21yeC5jb20iLCJGdWxsTmFtZSI6IlJvc2hhbiBNdXJhbGkiLCJBc2NvSWQiOiI3MzU4MDcwIiwiQ29udGFjdElkIjoiNzlkY2E1NzItMmU5OC1lZTExLWJlMzctNjA0NWJkZDVhMTQzIiwiaWQiOiI3MzU4MDcwIn0.RnfjJGZu2vNJqKHHZjLrcMjWgM3OCRY7uAQ1e4IXQMP_gVX_SM7wI22wfizD8tZ_qvckdfKqH0vZwUuOK38shZL7_QWs_PhYrlnQ0EtMzIsa5XrFiqbsZZDQTp_rmDd-hhdJQwCxRVoVdKf85Wa1UTw4Ejwugg7LNShi7GWOqAdFIvQwr5AQ67hdcG0ft-32R0FeD6Xdyh6Yu72w8p74a-ENI-OcrxIZ4WFVoQPNUWCbyJGvX0-gw-GbCbXJdjP5VyyNs4yrktBDLekFfReDOjQt1bk7F37dNLORp8rzDFbhOdKMG9QjpCq-L31UuHQql2C5Cp2uSsiG4I19tFTYqw',
    'Content-Type': 'application/json',
    'Referer': 'https://meetings.asco.org/',
    'Sec-Ch-Ua': '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    'X-Datadog-Origin': 'rum',
    'X-Datadog-Parent-Id': '2045220876576884443',
    'X-Datadog-Sampled': '1',
    'X-Datadog-Sampling-Priority': '1',
    'X-Datadog-Trace-Id': '2383813850394105565'
}


def posterid():
    payload = {"operationName":"Search","variables":{"q":"*","sortBy":"Oldest","size":20,"pageNumber":1,"filters":{"sessionType":[{"key":"Poster Session"},{"key":"Trials in Progress Poster Session"},{"key":"Poster Discussion Session"}],"contentTypeGroupLabel":[{"key":"Sessions"}],"meetingId":[{"key":"315"}]},"pages":[1]},"query":"query Search($q: String!, $filters: SearchFilters, $pageNumber: Int, $size: Int, $sortBy: SearchResultsSortBy, $groupBy: SearchGroupBy, $groupSize: Int, $searchFields: [SearchField]) {\n  search(\n    q: $q\n    filters: $filters\n    pageNumber: $pageNumber\n    size: $size\n    sortBy: $sortBy\n    groupBy: $groupBy\n    groupSize: $groupSize\n    searchFields: $searchFields\n  ) {\n    status\n    result {\n      suggestion\n      groups {\n        total\n        hits {\n          ...SearchHitFields\n          innerHits {\n            total\n            hits {\n              ...SearchHitFields\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      aggregations {\n        meetingYear {\n          key\n          doc_count\n          __typename\n        }\n        sessionType {\n          key\n          doc_count\n          __typename\n        }\n        meetingTypeName {\n          key\n          doc_count\n          __typename\n        }\n        topic {\n          key\n          doc_count\n          children {\n            key\n            doc_count\n            children {\n              key\n              doc_count\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        mediaType {\n          key\n          doc_count\n          __typename\n        }\n        contentTypeDisplayLabel {\n          key\n          doc_count\n          __typename\n        }\n        contentTypeGroupLabel {\n          key\n          doc_count\n          __typename\n        }\n        track {\n          key\n          doc_count\n          __typename\n        }\n        sessionStartTime {\n          key\n          doc_count\n          __typename\n        }\n        sessionDeliveryType {\n          key\n          doc_count\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment SearchHitFields on SearchHit {\n  abstractNumber\n  contentId\n  uid\n  elapsedTime\n  contentTypeDisplayLabel\n  contentTypeGroupLabel\n  contentSourceLabel\n  meetingYear\n  meetingName\n  meetingTypeName\n  contentSourceId\n  title\n  summary\n  mediaTypes\n  mediaCtas {\n    icon\n    text\n    url {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    __typename\n  }\n  posterBoardNumber\n  sponsoredCompanyName\n  firstAuthor {\n    fullNameWithDesignation\n    photoUrl {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    role\n    __typename\n  }\n  sessionType\n  totalPresentations\n  abstract {\n    abstractNumber\n    posterBoardNumber\n    __typename\n  }\n  url {\n    path\n    target\n    title\n    fqdn\n    queryParams\n    __typename\n  }\n  dateTimePublished\n  score\n  presentations\n  primaryTrack\n  meetingAttendanceType\n  attendanceType\n  sessionDeliveryType\n  sessionAttendanceType\n  sessionLocation\n  sessionCategory\n  sessionLiveBroadcastFlag\n  sessionDates {\n    start\n    end\n    timeZone\n    __typename\n  }\n  meetingId\n  isBookmarked\n  isOnDemandOnly\n  isInAgenda\n  applicationDates {\n    start\n    end\n    __typename\n  }\n  liveBroadcastUrl {\n    path\n    target\n    title\n    fqdn\n    queryParams\n    __typename\n  }\n  mediaSlides {\n    id\n    pages {\n      pageLowRes {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      pageHiRes {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      pagePpt {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      previewLowRes {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      previewHiRes {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      pageNumber\n      __typename\n    }\n    pageTotal\n    pptDeck {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    previewLowRes {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    previewHiRes {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    submitDate\n    __typename\n  }\n  __typename\n}\n"}
    s=[]
    a=[]
    response = requests.post(url = 'https://api.asco.org/graphql',headers=headers,data=json.dumps(payload))
    time.sleep(1)
    data = response.json()
    time.sleep(1)
    for d in data["data"]["search"]["result"]["groups"]["hits"]:
        a.append(d.get("contentId",''))
    df= pd.DataFrame({"id":a})
    df.to_csv("posterid.csv",index=False)
    return df

def posterlinks():
    poster_links=[]
    df =posterid()
    l = df['absID'].astype(str).unique().tolist()
    print("Unique absID values:", l)

    for i in l:
        payload = {
            "operationName": "getPosters",
            "variables": {"sessionId": i},
            "query": "query getPosters($sessionId: String!) {\n  session(sessionId: $sessionId) {\n    result {\n      contentId\n      presentations {\n        contentId\n        hasVideosAccess\n        presentation {\n          title\n          __typename\n        }\n        abstract {\n          abstractNumber\n          posterBoardNumber\n          __typename\n        }\n        mediaPosters {\n          pages {\n            pageLowRes {\n              path\n              target\n              title\n              fqdn\n              queryParams\n              __typename\n            }\n            pageHiRes {\n              path\n              target\n              title\n              fqdn\n              queryParams\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    status\n    errors {\n      code\n      message\n      __typename\n    }\n    __typename\n  }\n}\n"}
        
        response = requests.post(url='https://api.asco.org/graphql2', headers=headers, data=json.dumps(payload))
        try:
            data = response.json() 
            for presentation in data["data"]["session"]["result"]["presentations"]:
                try:
                    page_hi_res_path = presentation["mediaPosters"][0]["pages"][0]["pageHiRes"]["fqdn"] + presentation["mediaPosters"][0]["pages"][0]["pageHiRes"]["path"]
                    poster_links.append(page_hi_res_path)
                except:
                    continue
                
        except Exception as e:
            print("Error for absID {}: {}".format(i, str(e)))
            continue

    f = pd.DataFrame({'links':poster_links})
    f['link']="https://"+f['links']
    f.drop(columns=['links'],inplace=True)
    f.to_csv("plink.csv",index=False)
    return f
    
def download_poster():
    df = posterlinks()
    def download_images(row, folder_path):
        try:
            response = requests.get(row.link)
            img = Image.open(BytesIO(response.content))
            filename = os.path.join(folder_path, f"{row.link.split('/')[-1]}")
            img.save(filename)
            print(f"Image for poster {row.link} downloaded and saved as {filename}.")
        except Exception as e:
            print(f"Error downloading image for poster {row.link}: {e}")

    def download_images_parallel(row):
        download_images(row, "Downloaded Posters")

    pool = ThreadPool(processes=8)
    pool.map(download_images_parallel, df.itertuples(index=False))
    pool.close()
    pool.join()

#### slides download below

def slidesid():
    payload = {"operationName":"Search","variables":{"q":"*","sortBy":"Oldest","size":1000,"pageNumber":1,"filters":{"isOnDemandOnly":[{"key":"false"}],"contentTypeGroupLabel":[{"key":"Sessions"}],"excludeSessionCategory":[{"key":"Bonus Sessions"}],"meetingId":[{"key":"315"}]},"pages":[1]},"query":"query Search($q: String!, $filters: SearchFilters, $pageNumber: Int, $size: Int, $sortBy: SearchResultsSortBy, $groupBy: SearchGroupBy, $groupSize: Int, $searchFields: [SearchField]) {\n  search(\n    q: $q\n    filters: $filters\n    pageNumber: $pageNumber\n    size: $size\n    sortBy: $sortBy\n    groupBy: $groupBy\n    groupSize: $groupSize\n    searchFields: $searchFields\n  ) {\n    status\n    result {\n      suggestion\n      groups {\n        total\n        hits {\n          ...SearchHitFields\n          innerHits {\n            total\n            hits {\n              ...SearchHitFields\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      aggregations {\n        meetingYear {\n          key\n          doc_count\n          __typename\n        }\n        sessionType {\n          key\n          doc_count\n          __typename\n        }\n        meetingTypeName {\n          key\n          doc_count\n          __typename\n        }\n        topic {\n          key\n          doc_count\n          children {\n            key\n            doc_count\n            children {\n              key\n              doc_count\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        mediaType {\n          key\n          doc_count\n          __typename\n        }\n        contentTypeDisplayLabel {\n          key\n          doc_count\n          __typename\n        }\n        contentTypeGroupLabel {\n          key\n          doc_count\n          __typename\n        }\n        track {\n          key\n          doc_count\n          __typename\n        }\n        sessionStartTime {\n          key\n          doc_count\n          __typename\n        }\n        sessionDeliveryType {\n          key\n          doc_count\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment SearchHitFields on SearchHit {\n  abstractNumber\n  contentId\n  uid\n  elapsedTime\n  contentTypeDisplayLabel\n  contentTypeGroupLabel\n  contentSourceLabel\n  meetingYear\n  meetingName\n  meetingTypeName\n  contentSourceId\n  title\n  summary\n  mediaTypes\n  mediaCtas {\n    icon\n    text\n    url {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    __typename\n  }\n  posterBoardNumber\n  sponsoredCompanyName\n  firstAuthor {\n    fullNameWithDesignation\n    photoUrl {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    role\n    __typename\n  }\n  sessionType\n  totalPresentations\n  abstract {\n    abstractNumber\n    posterBoardNumber\n    __typename\n  }\n  url {\n    path\n    target\n    title\n    fqdn\n    queryParams\n    __typename\n  }\n  dateTimePublished\n  score\n  presentations\n  primaryTrack\n  meetingAttendanceType\n  attendanceType\n  sessionDeliveryType\n  sessionAttendanceType\n  sessionLocation\n  sessionCategory\n  sessionLiveBroadcastFlag\n  sessionDates {\n    start\n    end\n    timeZone\n    __typename\n  }\n  meetingId\n  isBookmarked\n  isOnDemandOnly\n  isInAgenda\n  applicationDates {\n    start\n    end\n    __typename\n  }\n  liveBroadcastUrl {\n    path\n    target\n    title\n    fqdn\n    queryParams\n    __typename\n  }\n  mediaSlides {\n    id\n    pages {\n      pageLowRes {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      pageHiRes {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      pagePpt {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      previewLowRes {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      previewHiRes {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      pageNumber\n      __typename\n    }\n    pageTotal\n    pptDeck {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    previewLowRes {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    previewHiRes {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    submitDate\n    __typename\n  }\n  __typename\n}\n"}
    s=[]
    a=[]
    response = requests.post(url = 'https://api.asco.org/graphql',headers=headers,data=json.dumps(payload))
    time.sleep(1)
    data = response.json()
    time.sleep(1)
    for d in data["data"]["search"]["result"]["groups"]["hits"]:
        a.append(d.get("contentId",''))
    df1= pd.DataFrame({"id":a})
    df2=pd.read_csv("posterid.csv")
    df1['id'] = df1['id'].astype('int64')
    df2['id'] = df2['id'].astype('int64')
    merged_df = pd.merge(df1,df2, on='id', how='outer', indicator=True)
    df = merged_df[merged_df['_merge'] == 'left_only']
    df = df.drop('_merge', axis=1)
    df.to_csv("slidesid.csv",index=False)
    
    return df

def slideslinks():
    slides_links=[]
    df  =slidesid()
    l = df['id'].astype(str).unique().tolist()
    print("Unique absID values:", l)
    for i in l:
        payload = {"operationName":"getSession",
                   "variables":{"sessionId":i},
                   "query":"query getSession($sessionId: String!) {\n  session(sessionId: $sessionId) {\n    result {\n      ...main\n      ...ceRecord\n      ...presentations\n      __typename\n    }\n    status\n    errors {\n      code\n      message\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment main on Session {\n  edBookReference {\n    doi\n    url {\n      fqdn\n      path\n      queryParams\n      target\n      title\n      __typename\n    }\n    __typename\n  }\n  inpersonContent\n  onlineContent\n  sponsoredCompanyName\n  isOnDemandOnly\n  attendanceType\n  sessionLocation\n  cmeCredits\n  fullSummary\n  ceParsActivity {\n    activityId\n    __typename\n  }\n  sessionNotes {\n    notes\n    timeStamp\n    __typename\n  }\n  isInPerson\n  uid\n  contentId\n  title\n  sessionType\n  playerEmbed {\n    fqdn\n    path\n    queryParams\n    target\n    title\n    __typename\n  }\n  sessionLiveBroadcastFlag\n  hasSlidesAccess\n  hasVideosAccess\n  tracks {\n    track\n    __typename\n  }\n  url {\n    path\n    target\n    title\n    fqdn\n    queryParams\n    __typename\n  }\n  claimCEurl {\n    path\n    target\n    title\n    fqdn\n    queryParams\n    __typename\n  }\n  frontMatterInfo {\n    activityType\n    coiLink\n    funders\n    __typename\n  }\n  mediaVideos {\n    m3u8 {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    mp4 {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    mediaDuration\n    previewLowRes {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    previewHiRes {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    chapterMeta {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    chapterMarker {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    slideMarker {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    __typename\n  }\n  sessionDates {\n    start\n    end\n    timeZone\n    __typename\n  }\n  liveBroadcastUrl {\n    path\n    target\n    title\n    fqdn\n    queryParams\n    __typename\n  }\n  meeting {\n    uid\n    contentId\n    title\n    abstractTitleReleaseDate {\n      start\n      __typename\n    }\n    abstractReleaseDate {\n      start\n      __typename\n    }\n    productBundlePurchaseUrl {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    registrationURL {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    meetingDates {\n      end\n      __typename\n    }\n    meetingChatPasscode\n    meetingYear\n    meetingType {\n      meetingType\n      name\n      active\n      displayOrder\n      __typename\n    }\n    ceMeeting {\n      displayClaimEndDate\n      isAbimAvailable\n      isAbpAvailable\n      islicenseAvailable\n      isAbsAvailable\n      feedbackFormId\n      feedbackEndDate\n      frontMatterTemplate\n      __typename\n    }\n    __typename\n  }\n  downloadAllUrl {\n    path\n    target\n    title\n    fqdn\n    queryParams\n    __typename\n  }\n  isBookMarked\n  __typename\n}\n\nfragment ceRecord on Session {\n  contentId\n  hasSlidesAccess\n  hasVideosAccess\n  ceRecord {\n    ascoId\n    ceCreditsClaimed\n    buttonStatus\n    ceStatus\n    buttonProps {\n      cssClass\n      icon\n      text\n      __typename\n    }\n    claimCreditPercent\n    accreditationType\n    feedbackQuestionAnswers {\n      questionNo\n      answer\n      __typename\n    }\n    cePersonalInfo {\n      firstName\n      lastName\n      birthDateTs\n      licenseState\n      abimId\n      abpId\n      showPersonalInfo\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment presentations on Session {\n  presentations {\n    contentId\n    url {\n      path\n      target\n      title\n      fqdn\n      queryParams\n      __typename\n    }\n    tracks {\n      track\n      __typename\n    }\n    presentation {\n      slidesUrl {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      videoUrl {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      doiUrl {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      title\n      abstractNumber\n      posterBoardNumber\n      disclosureUrl {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      recordable\n      orderWithinSession\n      presentationType\n      presentationDates {\n        start\n        end\n        timeZone\n        __typename\n      }\n      discussedAbstracts {\n        contentId\n        abstractId\n        abstractNumber\n        abstractTitle\n        __typename\n      }\n      discussedPosters\n      __typename\n    }\n    abstract {\n      disclosureUrl {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      subTrack {\n        subTrack\n        __typename\n      }\n      doi\n      abstractTitle\n      abstractNumber\n      abstractId\n      fullBody\n      fundingSource\n      tempAbstractId\n      journalCitation\n      posterBoardNumber\n      abstractType\n      originalResearchFlag\n      clinicalTrialRegistryNumber\n      downloadUrl {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      __typename\n    }\n    mediaSlides {\n      pptDeck {\n        path\n        target\n        title\n        fqdn\n        queryParams\n        __typename\n      }\n      __typename\n    }\n    visibleDates {\n      posters\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"}        
        response = requests.post(url='https://api.asco.org/graphql2', headers=headers, data=json.dumps(payload))
        data = response.json() 
        try:
            downloadAllUrl_data = data["data"]["session"]["result"]["downloadAllUrl"]
            queryParams_str = downloadAllUrl_data["queryParams"]
            queryParams_dict = json.loads(queryParams_str)
            policy_value = queryParams_dict["Policy"]
            signature_value = queryParams_dict.get("Signature", "")
            key = queryParams_dict.get("Key-Pair-Id", "")
            path = downloadAllUrl_data["path"]
            slides_links.append("https://d201v5jt9ylckg.cloudfront.net"+path+"?Policy="+policy_value+"&Signature="+signature_value+"&Key-Pair-Id="+key)        
        except Exception as e:
            print("error", e)
    d=pd.DataFrame({"link":slides_links})
    d.to_csv("slideslink.csv",index=False)
    return d

def download_slides():
    df = slideslinks()   
    def download_and_extract(row, folder_path):
        try:
            response = requests.get(row.link)
            zip_content = BytesIO(response.content)
            
            with ZipFile(zip_content, 'r') as zip_file:
                zip_file.extractall(folder_path)
                
            print(f"Slides for {row.link} downloaded and extracted to {folder_path}.")
        except Exception as e:
            print(f"Error downloading slides for {row.link}: {e}")

    def download_and_extract_parallel(row):
        download_and_extract(row, "Downloaded Posters")

    pool = ThreadPool(processes=8)
    pool.map(download_and_extract_parallel, df.itertuples(index=False))
    pool.close()
    pool.join()

# download_poster()
# posterid()
# download_slides()
