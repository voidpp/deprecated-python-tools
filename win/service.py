
import win32serviceutil
import win32service
import win32event
import win32api

class Service(win32serviceutil.ServiceFramework):
    _svc_name_ = '_unNamed'
    _svc_display_name_ = '_Service Template'

    class Logger():
        def error(self, msg):
            import servicemanager
            servicemanager.LogErrorMsg(str(msg))

        def info(self, msg):
            import servicemanager
            servicemanager.LogInfoMsg(str(msg))

        def debug(self, msg):
            import servicemanager
            servicemanager.LogInfoMsg(str(msg))

        def warning(self, msg):
            import servicemanager
            servicemanager.LogWarningMsg(str(msg))

    def __init__(self, *args):
        win32serviceutil.ServiceFramework.__init__(self, *args)
        self.log('init')
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.logger = Service.Logger()

    def log(self, msg):
        import servicemanager
        servicemanager.LogInfoMsg(str(msg))

    def sleep(self, sec):
        win32api.Sleep(sec*1000, True)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.log('start')
            self.start()
            self.log('wait')
            win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
            self.log('done')
        except Exception, x:
            self.log('Exception : %s' % x)
            self.SvcStop()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.log('stopping')
        self.stop()
        self.log('stopped')
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    # to be overridden
    def start(self):
        pass

    # to be overridden
    def stop(self):
        pass
