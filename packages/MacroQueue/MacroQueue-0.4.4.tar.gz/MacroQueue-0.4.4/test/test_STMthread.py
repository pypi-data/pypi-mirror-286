import wx
import multiprocessing as mp
import unittest
import sys
import os
application_path = os.path.dirname(__file__)
sys.path.append(os.path.realpath(application_path+'\\..\\MacroQueue\\'))
from MacroQueue import MacroQueue


class STMThread_test(unittest.TestCase):
    def test_thread(self):
        mp.freeze_support()
        self.app = wx.App() 
        self.MyMainFrame = MacroQueue(test=True)
        TestMacro = [ [{'Name':"Print","Parameters":{"Number":5}},True] ]
        self.MyMainFrame.IncomingQueue.put(("StartFunction",TestMacro))
        Message = self.MyMainFrame.OutgoingQueue.get()
        self.assertEqual(f"{Message}","('SetStatus', ('Function: Print', 1))")
        Message = self.MyMainFrame.OutgoingQueue.get()
        self.assertEqual(f"{Message}","('FunctionFinished', None)")
        self.MyMainFrame.OnClose()

        pass

if __name__ == '__main__':
    unittest.main()