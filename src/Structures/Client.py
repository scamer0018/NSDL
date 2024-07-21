import signal
from neonize.client import NewClient
from neonize.utils import *
from neonize.events import event
from Helpers.Utils import Utils

def interrupted(*_):
    event.set()
    
signal.signal(signal.SIGINT, interrupted)

class Client(NewClient):

    def __init__(self, name: str, uuid: str, prefix: str, uri: str): 
          super().__init__(uuid)
          self.name = name
          self.prifix = prefix
          self.uri = uri                         
          self.log = log     
          self.get_message_type = get_message_type 
          self.extract_text = extract_text
          self.FFmpeg = FFmpeg
          self.save_file_to_temp_directory = save_file_to_temp_directory
          self.get_bytes_from_name_or_url = get_bytes_from_name_or_url
          self.AspectRatioMethod = AspectRatioMethod
          self.build_jid = build_jid
          self.Jid2String = Jid2String
          self.JIDToNonAD = JIDToNonAD
          self.MediaType = MediaType
          self.MediaTypeToMMS = MediaTypeToMMS
          self.BlocklistAction = BlocklistAction
          self.ChatPresence = ChatPresence
          self.ChatPresenceMedia = ChatPresenceMedia
          self.ClientName = ClientName
          self.ClientType = ClientType
          self.ParticipantChange = ParticipantChange
          self.ParticipantRequestChange = ParticipantRequestChange
          self.PrivacySetting = PrivacySetting
          self.PrivacySettingType = PrivacySettingType
          self.ReceiptType = ReceiptType
          self.add_exif = add_exif
          self.validate_link = validate_link
          self.gen_vcard = gen_vcard
          self.utils = Utils()