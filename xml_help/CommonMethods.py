import re
import eaxs.eaxs_helpers.Restrictors as restrict
import hashlib
from eaxs.HashType import Hash
from lxml.ElementInclude import etree
from collections import OrderedDict

global __LOCALID__
global __ROOTPATH__
global __RELPATH__

__LOCALID__= 0  # type: int


class CommonMethods:

    @staticmethod
    def init_hash_dict():
        globals()["__HASH_LIST__"] = {}

    @staticmethod
    def set_chunk_size(size=None):
        globals()["__CHUNKS__"] = size

    @staticmethod
    def get_chunksize():
        return globals()["__CHUNKS__"]

    @staticmethod
    def get_messagetype_map():
        return OrderedDict([
            ("relative_path", "RelPath"),
            ("local_id", "LocalId"),
            ("message_id", "MessageId"),
            ("mime_version", "MimeVersion"),
            ("headers", "Header"),
            ("status_flag", "StatusFlag"),
            ("single_body", "SingleBody"),
            ("multiple_body", "MultiBody"),
            ("incomplete", "Incomplete"),
            ("hash", "Hash")])

    @staticmethod
    def get_singlebody_map():
        return OrderedDict([
            ("content_type", "ContentType"),
            ("charset", "Charset"),
            ("content_name", "ContentName"),
            ("content_type_comments", "ContentTypeComments"),
            ("content_type_param", "ContentTypeParam"),
            ("transfer_encoding", "TransferEncoding"),
            ("transfer_encoding_comments", "TransferEncodingComments"),
            ("content_id", "ContentId"),
            ("content_id_comments", "ContentIdComments"),
            ("description", "Description"),
            ("description_comments", "DescriptionComments"),
            ("disposition", "Disposition"),
            ("disposition_file_name", "DispositionFileName"),
            ("disposition_comments", "DispositionComments"),
            ("disposition_params", "DispositionParams"),
            ("other_mime_header", "OtherMimeHeader"),
            ("body_content", "BodyContent"),
            ("ext_body_content", "ExtBodyContent"),
            ("child_message", "ChildMessage"),
            ("phantom_body", "Phantom_Body")
        ])

    @staticmethod
    def get_multibody_map():
        return OrderedDict([
            ("content_type", "ContentType"),
            ("charset", "Charset"),
            ("content_name", "ContentName"),
            ("boundary_string", "BoundaryString"),
            ("content_type_comments", "ContentTypeComments"),
            ("content_type_param", "ContentTypeParam"),
            ("transfer_encoding", "TransferEncoding"),
            ("transfer_encoding_comments", "TransferEncodingComments"),
            ("content_id", "ContentId"),
            ("content_id_comments", "ContentIdComments"),
            ("description", "Description"),
            ("description_comments", "DescriptionComments"),
            ("disposition", "Disposition"),
            ("disposition_file_name", "DispositionFileName"),
            ("disposition_comments", "DispositionComments"),
            ("disposition_params", "DispositionParam"),
            ("other_mime_header", "OtherMimeHeader"),
            ("preamble", "Preamble"),
            ("single_bodies", "SingleBody"),
            ("multi_bodies", "MultiBody"),
            ("epilogue", "Epilogue"),
        ])

    @staticmethod
    def cdata_wrap(text):
        try:
            if re.search("[<>\'\"]", text) is not None:
                return etree.CDATA(text)
                pass
            return text
        except (ValueError, TypeError) as e:
            if text is None:
                return "Error: No Recipient Found"
            else:
                t = re.sub("\[\[", "\\[\\[", text)
                t = re.sub("]]", "\]\]", t)
                CommonMethods.cdata_wrap(t)

    @staticmethod
    def get_content_type(content_type):
        '''
        :param content_type:
        :type content_type : str
        :return: tuple:
        '''

        if re.search(';', content_type) is not None:
            # has a secondary component
            mime = content_type.split(";")[0]
            key, value = content_type.split(";")[1].split("=")
            return [mime, key.strip(), value.strip("\"")]
        else:
            # is only a mime type
            return [content_type]

    @staticmethod
    def increment_local_id():
        globals()["__LOCALID__"] += 1
        return globals()["__LOCALID__"]

    @staticmethod
    def get_current_local_id():
        return globals()["__LOCALID__"]

    @staticmethod
    def get_eol(message):
        """
        :param message
        :type message : str
        :return:
        """
        try:
            if message[-2:] == "\r\n": return restrict.CRLF
            if message[-1:] == "\r": return restrict.CR
            if message[-1:] == "\n" and message[-2:] != "\r\n": return restrict.LF
        except KeyError as ke:
            return restrict.LF

    @staticmethod
    def get_hash(message):
        '''
        Defaulting to SHA1 in this version of the tool.  Future versions give options.
        :return:
        '''
        hsh = hashlib.sha1()
        hsh.update(message)
        return Hash(hsh.hexdigest(), restrict.SHA1)

    @staticmethod
    def set_base_path(path):
        globals()["__ROOTPATH__"] = path

    @staticmethod
    def get_base_path():
        return globals()["__ROOTPATH__"]

    @staticmethod
    def set_attachment_dir(folder='attachments'):
        globals()["__ATTACHMENTS__"] = folder

    @staticmethod
    def get_attachment_directory():
        return globals()["__ATTACHMENTS__"]

    @staticmethod
    def set_xml_dir(folder='eaxs_xml'):
        globals()["__EAXS_XML__"] = folder

    @staticmethod
    def get_xml_directory():
        return globals()["__EAXS_XML__"]

    @staticmethod
    def set_store_rtf_body(val=False):
        globals()["__STORE_RTF_BODY__"] = val

    @staticmethod
    def store_rtf_body():
        return globals()["__STORE_RTF_BODY__"]

    @staticmethod
    def set_eaxs_file(file_name):
        globals()["__EAXS_FILE__"] = file_name

    @staticmethod
    def get_eaxs_filename():
        return globals()["__EAXS_FILE__"]

    @staticmethod
    def set_ext_hash(gid, hash):
        hash_list = globals()["__HASH_LIST__"]  # type: dict
        if hash.value not in hash_list:
            hash_list[hash.value] = gid
            return True
        return False

    @staticmethod
    def get_ext_gid(hash):
        hash_list = globals()["__HASH_LIST__"]  # type: dict
        return hash_list[hash]

    @staticmethod
    def set_dedupe(val=True):
        globals()["__DEDUPE__"] = val

    @staticmethod
    def get_dedupe():
        return globals()["__DEDUPE__"]