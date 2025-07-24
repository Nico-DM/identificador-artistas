import praw
from datetime import datetime

import praw.exceptions

reddit = praw.Reddit("identificador_artistas")
reddit.read_only = True

def obtener_fecha_post(url):
    try:
        submission = reddit.submission(url=url)
        timestamp = submission.created_utc
        return datetime.fromtimestamp(timestamp)
    except praw.exceptions.InvalidURL:
        return datetime.now()

# Ejemplo
if __name__ == "__main__":
    url = "https://www.reddit.com/r/goodmythicalmorning/comments/m2x33f/im_going_to_tell_my_kids_that_this_was_link_from/"
    fecha = obtener_fecha_post(url)
    print("Fecha exacta:", fecha)