#!/usr/bin/python3

import asyncio, time, logging, argparse, sys, os, importlib
from emmi import app

from emmi.api.exports import ExportObjectFromDict

logger = logging.getLogger(__name__)

class Application(app.IocApplication):
    '''
    Main application model for EPICS-SCPI gateway. Consits of:
      - an IOC
      - a SCPI device
      - handling of a configuration YAML (for a device and application)
      - updating/overwriting of configuration options by command line
        and environment variables
    '''
    
    def __init__(self, name="escpi", desc='EPICS-IOC for SPCI devices',
                 access_class="emmi.scpi:MagicScpi", access_obj=None,
                 **kwargs):
        '''
        If `device` is not None, it is used as an SCPI device (object),
        Otherwise a new device is created, with I/O on SCPI-port `port`
        is used.
        '''
        super().__init__(**kwargs)

        parser = argparse.ArgumentParser(
            prog=name,
            description=desc,
            epilog='If you break it, you get to keep both pieces'
        )

        parser.add_argument('-d', '--access-device', action='store',
                            help='VISA device to use')
        parser.add_argument('-r', '--access-rman', action='store', default="@py",
                            help='VISA resource manager to use (default: @py)')
        parser.add_argument('-e', '--epics-prefix', action='store',
                            help='EPICS prefix to export to')
        parser.add_argument('-y', '--from-yaml', action='store',
                            help='Load device properties from YAML definiton')
        parser.add_argument('-l', '--logging', action='store', default="INFO",
                            help='Logging level (DEBUG, INFO, WARNING, ERROR)')

        self.args_parser = parser

        if access_obj is not None:
            self.access_obj = access_obj
        else:
            self.conf['access_class'] = access_class

        
    def _make_access(self, access_class, access_args=None):
        # Generates an access object of type `access_class`.
        # This involves loading the module and instantiating
        # a class. To make the external class a "1st-class citizen",
        # we pass it `access_args` as kwargs, if it is not `None`.
        mod, cls = access_class.split(':')
        try:
            acc_module = importlib.import_module(mod)
            acc_class = getattr(acc_module, cls)
        except Exception as e:
            logger.error(f'module={mod} class={cls} desc="{e}"')
            raise

        if access_args is None:
            access_args = {}
        return acc_class(**access_args)

        
    def _init_access(self, access_obj=None, **config_args):
        '''
        Initializes the access device.

        This would typically be called during, or close after, `.__init__()`.
        But when subclassing this application class, the higher layer might
        want to add specific command line arguments or transformations.
        So we leave it as the higher layer's responsibility to
        do this.

        This will load the application's `.conf['access]` section for
        named initialization parameters to be passed to the access class's
        `__init__()` routine.
        '''
        
        self.configure(self.args_parser, **config_args)

        if access_obj is not None:
            self.access_obj = access_obj

        if not hasattr(self, "access_obj"):
            try:
                acls = self.conf["access_class"]
            except KeyError:
                raise RuntimeError(f'Somehow we ended up without an access class')
            
            acc_args = self.conf.get('access', {})
            logger.info(f'access="{acls}" args="{acc_args}"')
            self.access_obj = self._make_access(acls, acc_args)


    def setupIoc(self, **config_args):
        
        self._init_access(**config_args)
        
        super().setupIoc()
        
        for f in self.conf['fields']:
            self.addField(**f)

            
    def addField(self, **spec):
        '''
        Exposes a property/field/signal/... from its YAML configuration keys.
        '''        
        ExportObjectFromDict(self.iocDispatch, self.access_obj, spec)



