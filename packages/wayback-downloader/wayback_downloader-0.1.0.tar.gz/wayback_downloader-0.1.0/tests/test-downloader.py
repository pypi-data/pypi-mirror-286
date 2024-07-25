import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from wayback_downloader.downloader import (
    check_internet_connection,
    create_session_with_retries,
    download_archive,
    save_archive,
    extract_links,
    get_content_hash,
    crawl_and_archive,
)

def test_check_internet_connection():
    with patch('socket.gethostbyname') as mock_gethostbyname:
        mock_gethostbyname.return_value = '123.45.67.89'
        assert check_internet_connection() == True
        
        mock_gethostbyname.side_effect = Exception('Unable to resolve')
        assert check_internet_connection() == False

def test_create_session_with_retries():
    session = create_session_with_retries()
    assert session.mount.call_count == 2  # Called for both http and https

def test_download_archive():
    with patch('requests.Session.get') as mock_get:
        mock_response = MagicMock()
        mock_response.text = '<html>Test content</html>'
        mock_get.return_value = mock_response
        
        content = download_archive('http://example.com', datetime.now())
        assert content == '<html>Test content</html>'

def test_save_archive(tmp_path):
    content = '<html>Test content</html>'
    filename = tmp_path / 'test.html'
    saved_filename = save_archive(content, str(filename))
    
    assert saved_filename.endswith('.html')
    with open(saved_filename, 'r') as f:
        assert f.read() == content

def test_extract_links():
    content = '''
    <html>
        <body>
            <a href="http://example.com/page1">Page 1</a>
            <a href="http://example.com/page2">Page 2</a>
            <a href="http://external.com">External</a>
        </body>
    </html>
    '''
    base_url = 'http://example.com'
    links = extract_links(content, base_url)
    assert links == {'http://example.com/page1', 'http://example.com/page2'}

def test_get_content_hash():
    content = 'Test content'
    hash1 = get_content_hash(content)
    hash2 = get_content_hash(content)
    assert hash1 == hash2
    assert isinstance(hash1, str)

@patch('wayback_downloader.downloader.download_archive')
@patch('wayback_downloader.downloader.save_archive')
@patch('wayback_downloader.downloader.extract_links')
def test_crawl_and_archive(mock_extract_links, mock_save_archive, mock_download_archive):
    mock_download_archive.return_value = '<html>Test content</html>'
    mock_save_archive.return_value = 'saved_file.html'
    mock_extract_links.return_value = set()
    
    wayback_client = MagicMock()
    wayback_client.search.return_value = [MagicMock(timestamp=datetime.now())]
    
    with patch('wayback.WaybackClient', return_value=wayback_client):
        crawl_and_archive('http://example.com', datetime.now(), datetime.now())
    
    assert mock_download_archive.called
    assert mock_save_archive.called
    assert mock_extract_links.called

if __name__ == '__main__':
    pytest.main()
