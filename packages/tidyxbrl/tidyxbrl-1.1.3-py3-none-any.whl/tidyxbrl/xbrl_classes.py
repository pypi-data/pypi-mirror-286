    """
    
    """
    
# %%

class DataRequest:
    def __init__(self, xbrl):
        self.xbrl = xbrl
        self.data = self.get_data(

class XBRL:
    def __init__(self, xbrl_file):
        self.xbrl_file = xbrl_file
        self.xbrl = self.load_xbrl()
        self.xbrl_dict = self.xbrl_to_dict()