import re
def meme(nick,streak):
    icons="øæå"
    current_icon = "æ"
    current_streak = streak+1

    if current_streak > 0:
        s=f'^\d+({"|".join(icons)}) '
        if (match:=re.compile(s).match(nick)):
            nick = ''.join(nick.split(match.group(0))[1:])
        return f'{current_streak}{current_icon} {nick}'
        
