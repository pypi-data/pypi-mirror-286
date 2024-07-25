"""
Parameter initialization is a global variable by default. When calling the relevant API,
you need to inherit the setting class and set the corresponding parameters.

"""


class Settings:
    """
    Settings class
    """

    report_path = "report"
    db_path = "proxy"
    url = None
    all_events = []
    interface_url = []
    mock = {"api": "", "content": ""}
    events_properties = {}
    result = None
    result_dict = None
    expect = None
    actual = None
    exclude_paths = None
    global_url = None
    api_collection = {}
    web_host: str = "0.0.0.0"
    web_port: int = 8088
    server_port: int = 8888
    # options command: map_remotes, map_locals, modify_bodys, modify_headers, mock_events
    options = "mock_events"
