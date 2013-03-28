import sys
from PyQt4 import QtGui
from threading import Thread
import time
from subprocess import call
import subprocess

def ping( hostname ):
	hostname;
	response = call("ping -n 1 " + hostname, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell = False)
	
	if response == 0:
		#up
		return True
	else:
		return False

class SystemTrayIcon(QtGui.QSystemTrayIcon):
	def pollthing(self):
		lastResult = True;
		while self.kill == False :
			result = ping( "www.google.com" )
			if result != lastResult :
				if result :
					self.setIcon(QtGui.QIcon("checkmark.png"))
				else:
					self.setIcon(QtGui.QIcon("x_button.png"))
					
				lastResult = result
			time.sleep(1.0)
	
	def killapp(self):
		self.kill = True
		self.pollthread._stop()
		QtGui.qApp.quit()
		sys.exit()
		
	def __init__(self, icon, parent=None):
		QtGui.QSystemTrayIcon.__init__(self, icon, parent)
		menu = QtGui.QMenu(parent)
		
		exitAction = QtGui.QAction(QtGui.QIcon("exit.png"), '&Exit', self)		
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(self.killapp)
		
		menu.addAction( exitAction )
		self.setContextMenu(menu)
		
		#timer for polling
		self.kill = False
		self.pollthread = Thread( None, self.pollthing )
		self.pollthread.start()
		#self.pollthing()

def main():
	app = QtGui.QApplication(sys.argv)

	w = QtGui.QWidget()
	trayIcon = SystemTrayIcon(QtGui.QIcon("checkmark.png"), w)

	trayIcon.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()