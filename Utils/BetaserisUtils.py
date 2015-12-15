import urllib.request
import json
import datetime
class BetaserieUtils:
    key = 'a71be26370dc'
    id = 122640
    version = '2.4'


    def getMemberPlanning(self, memberId, key):
        params = urllib.parse.urlencode({'id': memberId, 'unseen': 'true', 'key': key, 'version': self.version})
        f = urllib.request.urlopen("https://api.betaseries.com/planning/member?%s" % params)
        return (json.loads(f.read().decode('utf-8')))

    def convertStringToDate(self, theString):
        return datetime.datetime.strptime(theString, "%Y-%m-%d")

    def getTodayEpisode(self):
        result = []
        today = datetime.datetime.now()
        planning = self.getMemberPlanning(self.id,self.key)
        if planning is not None:
            for episode in planning['episodes']:
                theDate = self.convertStringToDate(episode['date'])
                if theDate.date() == (today + datetime.timedelta(days=-1)).date():
                    anEpisode = episode['show']['title']+' '+episode['code']
                    print(anEpisode)
                    result.append(anEpisode)
        return result

if __name__ == '__main__':
    aBetaserieUtil = BetaserieUtils()
    aBetaserieUtil.getTodayEpisode()