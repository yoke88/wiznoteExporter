#!/usr/bin/env python
#coding:utf-8
# Author        : tuxpy
# Email         : q8886888@qq.com.com
# Last modified : 2015-11-05 13:55:24
# Filename      : notebook.py
# Description   : 
from __future__ import print_function, unicode_literals
from wiz.base import BaseManager
from wiz.utils import ObjectDict, get_text_from_html, get_image_from_html
from wiz.note import Note, NoteData, NoteImageData, NoteAttrData

class Notebook(ObjectDict):
    def rename(self, new_title):
        return self._manager.rename(self['id'], new_title)

    def rm(self):
        return self._manager.rm(self['id'])

    def ls(self, count = 200):
        """list all notes in this notebook"""
        return self._manager.ls_notes(self['id'], count)

    def find(self, keyword):
        return self._manager.find_notes(self['id'], keyword)

class NotebookManager(BaseManager):
    def ls(self):
        result, error = self.api_request('/api/category/all')
        notebooks = []

        # 用户可能会修改默认的那个笔记本名
        if '/My Notes/' not in [n['location'] for n in result['list']]:
            result['list'].append({u'type': u'category', u'location': u'/My Notes/', 
                u'category_name': '我的笔记'})

        for raw_notebook in result['list']:
            notebooks.append(Notebook({
                'name'      :       raw_notebook['category_name'],
                'path'      :       raw_notebook['location'],
                'id'        :       raw_notebook['location'],
                '_manager'   :       self,
                }))

        return notebooks


    def rename(self, _id, new_title):
        result, error = self.api_request('/api/category/item', method = 'PUT', data = {
                    'old_category_path'         :       _id,
                    'new_title'                 :       new_title,
                })

    def rm(self, _id):
        result, error = self.api_request('/api/category/item', method = 'DELETE', data = {
            'old_category_path'         :       _id,
            })

    def ls_notes(self, _id, count = 200):
        return self.__get_notes('category', _id, count)

    def __get_notes(self, action_cmd, action_value, count = 200):
        result, error = self.api_request('/api/document/list', method = 'GET', data = {
            'action_cmd'        :       action_cmd,
            'action_value'      :       action_value,
            'count'             :       count,
            'auto'              :       'true',
            })

        notes = []
        for raw_note in result['list']:
            notes.append(Note({
                'title'           :       raw_note['document_title'],
                'tag_guids'       :       raw_note['document_tag_guids'],
                'version'         :       raw_note['version'],  # 被修改了多少次
                'create_time'     :       raw_note['dt_created'],
                'modify_time'     :       raw_note['dt_data_modified'],
                'md5'             :       raw_note['data_md5'],
                'attachment_count':       raw_note['document_attachment_count'],
                'guid'            :       raw_note['document_guid'],
                '_manager'        :       self,
                }))

        return notes

    def find_notes(self, keyword, count = 200):
        return self.__get_notes('keyword', keyword, count)

    def __get_note_attrs(self, guid):
        result, error = self.api_request('/api/attachment/list', method = 'GET', data = {
            'document_guid'     :       guid,
            })

        attrs = [{'name': attr_data['attachment_name'], 'url': attr_data['download_url']}\
                for attr_data in result['list']]

        return attrs

    def get_note_data(self, guid):
        result, error = self.api_request('/api/document/info', method = 'GET', data = {
            'document_guid'     :       guid,
            })

        document_info = result['document_info'];
        if int(document_info['document_attachment_count']):
            attachments = self.__get_note_attrs(guid)
        else:
            attachments = []

        note_data = NoteData({
            'body'         :       document_info['document_body'],
            'md5'          :       document_info['data_md5'],
            'text'         :       get_text_from_html(document_info['document_body']),
            'images'       :       [NoteImageData(img_url) for img_url in get_image_from_html(document_info['document_body'])],
            'attachments'  :       [NoteAttrData(**attr_data) for attr_data in attachments],
            })

        return note_data

