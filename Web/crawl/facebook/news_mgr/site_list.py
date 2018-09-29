def get():
    """
    新聞網站分類的資料
    :return: list of dict, topics底下再包著list of dict
    """
    SITE_LIST = [
        {
            'img': 'media/web-apple-daily.jpg',
            'name': '蘋果日報',
            'topics': [
                {'topicname': 'Iphone',
                 'url': '#'},
                {'topicname': '就業',
                 'url': '#'},
                {'topicname': '直播',
                 'url': '#'},
                {'topicname': '貿易',
                 'url': '#'}
            ]
        },
        {
            'img': 'media/web-ltn.jpg',
            'name': '自由時報',
            'topics': [
                {'topicname': '財經',
                 'url': '#'},
                {'topicname': '3C',
                 'url': '#'},
                {'topicname': '健康',
                 'url': '#'}
            ]
        },
        {
            'img': 'media/web-ct.png',
            'name': '中國時報',
            'topics': [
                {'topicname': '',
                 'url': ''}
            ]
        }
    ]

    return SITE_LIST