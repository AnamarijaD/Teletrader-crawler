import datetime
from config.logger_config import Logger
from helper.file_helper import download_file

BASE_URL = 'https://fondswelt.hansainvest.com'

def extract_record_metadata(span, isin_td):
    """Extract metadata for a record from the webpage.
    
    Args:
        span (BeautifulSoup Tag): The HTML span element containing the document details.
        isin_td (list): A list containing ISIN details.
        
    Returns:
        dict: A dictionary containing the metadata for the record, or None if download fails.
    """

    isin = isin_td[1]
    effective_date = span.span.span.text.strip() if span.span.span else ''
    file_size = span.small.text.strip() if span.small else ''
    document_type = span.a['href'].split('/')[3]
    document_url = BASE_URL + span.a['href']

    if document_url:
        file_path, md5_hash = download_file(document_url, isin)
        if file_path and md5_hash:
            Logger.info(f'Crawling record: {isin}')
            download_date = datetime.datetime.now().strftime('%d.%m.%Y')
            metadata = {
                'ISIN': isin,
                'DocumentType': document_type,
                'EffectiveDate': effective_date,
                'DownloadDate': download_date,
                'DownloadUrl': document_url,
                'FilePath': file_path,
                'MD5Hash': md5_hash,
                'FileSize': file_size
            }
            return metadata
    return None
