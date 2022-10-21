from control.app import appFactory
from control.webdavapp import app as webdavapp
from control.dispatcher import DispatchWebdav


app = appFactory()
app.wsgi_app = DispatchWebdav(appFactory(), "/webdav/", webdavapp)
