from jjsystem.common import subsystem
from jjlocal.subsystem.sysadmin.ibge_sync \
  import resource, manager

subsystem = subsystem.Subsystem(resource=resource.IbgeSync,
                                manager=manager.Manager)
