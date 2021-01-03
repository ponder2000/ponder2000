import tweepy as tw
import key


BLUE_COLOR = '\033[95m'
RED_COLOR = '\033[91m'
GREEN_COLOR = '\033[92m'
COLOR_END = '\033[0m'


class TweeterBot:
    def __init__(self):
        api_key = key.API_KEY
        api_secret = key.API_KEY_SECRET
        access_token = key.ACCESS_TOKEN
        access_token_secret = key.ACCESS_TOKEN_SECRET

        auth = tw.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tw.API(auth, wait_on_rate_limit=True,
                          wait_on_rate_limit_notify=True)
        self.me = self.api.me()

    def _parseUserData(self, user) -> dict:
        "Parse tweepy user data with atributes and returns a dict with required info"
        _id = user.id
        _username = user.screen_name
        _displayName = user.name
        _description = user.description
        _profileImage = user.profile_image_url
        return {
            'id': _id,
            'username': _username,
            'displayName': _displayName,
            'description': _description,
            'profileImage': _profileImage,
        }

    def getMyself(self) -> dict:
        "Returns my info"
        return self._parseUserData(self.me)

    def getRecentFollowers(self, num: int = 3) -> list:
        "Returns my recent followers"
        followersObj = self.me.followers()
        followers = [f for f in followersObj]
        result = []
        for i in range(min(num, len(followers))):
            try:
                result.append(self._parseUserData(followers[i]))
            except:
                pass
        return result

    def getMyRecentTweet(self) -> str:
        "Returns my most recent tweet content"
        myTweets = self.me.status
        recentTweet = self.api.get_status(myTweets.id)
        return recentTweet.text


def getMarkdownUser(username, img_url):
    return f"![]({img_url}) [@{username}](https://twitter.com/{username})<br>"


def writeDynamicMd(result, me):
    tmp = ""
    for r in result:
        tmp += r
    content = f"\n {tmp} \n\n![](https://visitor-badge.laobi.icu/badge?page_id=ponder2000)\n"
    fp = open('dynamic.md', 'w')
    fp.write(content)
    fp.close()


if __name__ == "__main__":
    bot = TweeterBot()
    me = bot.getMyself()
    recentFollowers = bot.getRecentFollowers(num=5)
    # recentTweetText = bot.getMyRecentTweet()
    result = []
    for user in recentFollowers:
        result.append(getMarkdownUser(user['username'], user['profileImage']))

    writeDynamicMd(result, getMarkdownUser(me['username'], me['profileImage']))
    print(f"{GREEN_COLOR}Code executed successfully {COLOR_END}")
