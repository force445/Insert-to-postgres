import psycopg2

import json
import datetime

class InsertData():
    def __init__(self,host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        
        try:
            self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        except:
            raise Exception('500 Internal Server Error')
        
        self.validate_data_structure(input(""))

    def validate_file_name(self, file_name):
        if 'section' in file_name:
            return 'section'
        elif 'widget' in file_name:
            return 'widget'

    def validate_data_structure(self,file_name):
        with open(file_name) as json_file:
            data = json.load(json_file)
            if isinstance(data, list):
                for item in data:
                    if self.validate_file_name(file_name) == 'section':
                        self.insert_section(item)
                    elif self.validate_file_name(file_name) == 'widget':
                        self.insert_widget(item)
            elif isinstance(data, dict):
                if self.validate_file_name(file_name) == 'section':
                    self.insert_section(data)
                elif self.validate_file_name(file_name) == 'widget':
                    self.insert_widget(data)
            

    def insert_section(self, data):
        data['section_option'] = json.dumps(data['section_option'])
        data['section_style'] = json.dumps(data['section_style'])

        
        cur = self.conn.cursor()
        sql = f"""

        INSERT INTO public.customize_dashboard_dashboardsection(
	        id, deleted_by_cascade, created_at, updated_at, index, section_name, section_type, section_option, section_style, created_by_id, project_id, updated_by_id)
	    VALUES('{data['id']}', False, '{datetime.datetime.now()}',
            '{datetime.datetime.now()}', {data['index']}, '{data['section_name']}', 
            '{data['section_type']}', '{data['section_option']}', '{data['section_style']}', '1', {data['project_id']}, '1')
        
        """
        cur.execute(sql)
        self.conn.commit()
        cur.close()
        self.conn.close()

    def insert_widget(self, data):
        data['widget_items'] = json.dumps(data['widget_items'])
        data['chart_style'] = json.dumps(data['chart_style'])

        cur = self.conn.cursor()
        sql = f"""

        INSERT INTO public.customize_dashboard_sectionwidget(
	        id, deleted_by_cascade, created_at, updated_at, index, widget_name, widget_type, widget_items, chart_type, chart_style, created_by_id, section_id, updated_by_id)
        VALUES ('{data['id']}', False, '{datetime.datetime.now()}', '{datetime.datetime.now()}', 
            {data['index']}, '{data['widget_name']}', '{data['widget_type']}', '{data['widget_items']}', 
            '{data['chart_type']}','{data['chart_style']}', '1', '{data['section_id']}', 
            '1')

        """
        cur.execute(sql)
        self.conn.commit()
        cur.close()
        self.conn.close()

insert = InsertData('host', 'db_name', 'user', 'password')

