def get():
    """
    新聞網站分類的資料
    :return: list of dict, topics底下再包著list of dict
    """
    base = '/recommendation/site='
    SITE_LIST = [
        {
            'img': 'media/web-apple-daily.jpg',
            'name': '蘋果日報',
            'topics': [
                {'topicname': 'Iphone',
                 'url': base + 'apple&theme=iphone'},
                {'topicname': '就業',
                 'url': base + 'apple&theme=career'},
                {'topicname': '直播',
                 'url': base + 'apple&theme=livestream'},
                {'topicname': '貿易',
                 'url': base + 'apple&theme=trading'}
            ]
        },
        {
            'img': 'media/web-ltn.jpg',
            'name': '自由時報',
            'topics': [
                {'topicname': '財經',
                 'url': base + 'free&theme=finance'},
                {'topicname': '3C',
                 'url': base + 'free&theme=3c'},
                {'topicname': '健康',
                 'url': base + 'free&theme=health'}
            ]
        },
        {
            'img': 'media/web-ct.png',
            'name': '中國時報',
            'topics': [
                {'topicname': '體育',
                 'url': base + 'china&theme=sport'},
                {'topicname': '軍事',
                 'url': base + 'china&theme=military'},
                {'topicname': '娛樂',
                 'url': base + 'china&theme=entertainment'},
                {'topicname': '選舉',
                 'url': base + 'china&theme=election'},
                {'topicname': '旅遊',
                 'url': base + 'china&theme=travel'}
            ]
        }
    ]

    return SITE_LIST