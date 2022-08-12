import speedtest


def check_internet_speed():
    """Checks internet speed

    :return: 2 values: download speed and upload speed
    """
    return speedtest.Speedtest(), speedtest.Speedtest()


def get_internet_speed():
    d, up = check_internet_speed()

    download = f'{d.download() / 8000000:.2f}'
    upload = f'{d.upload() / 8000000:.2f}'

    return download, upload


if __name__ == '__main__':
    get_internet_speed()
