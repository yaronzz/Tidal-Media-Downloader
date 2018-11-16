def downloadFile(url, fileName):
    import sys
    if sys.version_info > (2, 7):
        # Python 3
        from urllib.request import urlopen
    else:
        # Python 2
        from urllib2 import urlopen

    try:
        response = urlopen(url)
        chunk = 16 * 1024
        with open(fileName, 'wb') as f:
            while True:
                chunk = response.read(chunk)
                if not chunk:
                    break
                f.write(chunk)
            return True
    except:
        return False
