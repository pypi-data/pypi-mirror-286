from .. import trace, const
from ...wrappers import sysmonw
from ...basics import dicts


PROVIDER_NAME: str = const.ETW_SYSMON['provider_name']
PROVIDER_GUID: str = const.ETW_SYSMON['provider_guid']
PROCESS_CREATION_EVENT_ID: int = const.ETW_SYSMON['event_ids']['process_create']


class SysmonProcessCreationTrace:
    def __init__(
            self,
            attrs: list = None,
            session_name: str = None,
            close_existing_session_name: bool = True,
            sysmon_directory: str = None
    ):
        """
        DnsTrace class use to trace DNS events from Windows Event Tracing for EventId 3008.

        :param attrs: List of attributes to return. If None, all attributes will be returned.
        :param session_name: The name of the session to create. If not provided, a UUID will be generated.
        :param close_existing_session_name: Boolean to close existing session names.
            True: if ETW session with 'session_name' exists, you will be notified and the session will be closed.
                Then the new session with this name will be created.
            False: if ETW session with 'session_name' exists, you will be notified and the new session will not be
                created. Instead, the existing session will be used. If there is a buffer from the previous session,
                you will get the events from the buffer.
        :param sysmon_directory: The directory where Sysmon is located. If not provided, "C:\\Windows\\Sysmon" will be
            used. If 'Sysmon.exe' is not found in the directory, it will be downloaded from the internet.

        -------------------------------------------------

        Usage Example:
            from atomicshop.etw import dns_trace


            dns_trace_w = dns_trace.DnsTrace(
                attrs=['pid', 'name', 'cmdline', 'domain', 'query_type'],
                session_name='MyDnsTrace',
                close_existing_session_name=True,
                enable_process_poller=True,
                process_poller_etw_session_name='MyProcessTrace'
            )
            dns_trace_w.start()
            while True:
                dns_dict = dns_trace_w.emit()
                print(dns_dict)
            dns_trace_w.stop()
        """

        self.attrs = attrs
        self.sysmon_directory: str = sysmon_directory

        self.event_trace = trace.EventTrace(
            providers=[(PROVIDER_NAME, PROVIDER_GUID)],
            # lambda x: self.event_queue.put(x),
            event_id_filters=[PROCESS_CREATION_EVENT_ID],
            session_name=session_name,
            close_existing_session_name=close_existing_session_name
        )

    def start(self):
        sysmonw.start_as_service(
            installation_path=self.sysmon_directory, download_sysmon_if_not_found=True, skip_if_running=True)
        self.event_trace.start()

    def stop(self):
        self.event_trace.stop()

    def emit(self):
        """
        Function that will return the next event from the queue.
        The queue is blocking, so if there is no event in the queue, the function will wait until there is one.

        Usage Example:
            while True:
                dns_dict = dns_trace.emit()
                print(dns_dict)

        :return: Dictionary with the event data.
        """

        event = self.event_trace.emit()

        event_dict: dict = {
            'event_id': event['event_id'],
            'pid': event['event']['ProcessId'],
            'process_guid': event['event']['ProcessGuid'],
            'image': event['event']['Image'],
            'file_version': event['event']['FileVersion'],
            'product': event['event']['Product'],
            'company': event['event']['Company'],
            'original_file_name': event['event']['OriginalFileName'],
            'command_line': event['event']['CommandLine'],
            'current_directory': event['event']['CurrentDirectory'],
            'user': event['event']['User'],
            'logon_id': event['event']['LogonId'],
            'logon_guid': event['event']['LogonGuid'],
            'terminal_session_id': event['event']['TerminalSessionId'],
            'integrity_level': event['event']['IntegrityLevel'],
            'hashes': event['event']['Hashes'],
            'parent_process_guid': event['event']['ParentProcessGuid'],
            'parent_process_id': event['event']['ParentProcessId'],
            'parent_image': event['event']['ParentImage'],
            'parent_command_line': event['event']['ParentCommandLine']
        }

        if self.attrs:
            event_dict = dicts.reorder_keys(
                event_dict, self.attrs, skip_keys_not_in_list=True)

        return event_dict
