
class Publication(object):

    def __init__(self, info):
        self.info = info
        self.info['cites'] = int(self.info['cites'])

    def __str__(self):
        return "{}, {}, {}\nCitations: {}\nURL: {}".format(self.info['author'], self.info['year'],
                                                           self.info['title'], self.info['cites'],
                                                           self.info["url"] if 'url' in self.info.keys() else 'Not found')

