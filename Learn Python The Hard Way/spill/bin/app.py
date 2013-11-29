#import web so this app can run on the web
import web
from maps import map

#sets urls
urls = (
  '/game', 'GameEngine',
  '/', 'Index', '/sttc',
)

app = web.application(urls, globals())

# little hack so that debug mode works with sessions
if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')
    session = web.session.Session(app, store,
                                  initializer={'room': None})
    web.config._session = session
else:
    session = web.config._session

render = web.template.render('templates/', base="layout")


class Index(object):
    def GET(self):
        # this is used to "setup" the session with starting values
        session.room = map.START
        web.seeother("/game")

#Class GameEningen, if a room has a session returns show.room html if not die. 
class GameEngine(object):

    def GET(self):
        if session.room:
            return render.show_room(room=session.room)
        else:
            
            return render.you_died()
	#Takes input from user.
    def POST(self):
        form = web.input(action=None)

        # there is a bug here, can you fix it? - no. 
        if session.room and form.action:
            session.room = session.room.go(form.action)

        web.seeother("/game")

if __name__ == "__main__":
    app.run()