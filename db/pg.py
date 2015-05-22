#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'fernandinand'


class DB:
    def __init__(self, path):
        """ Get connection from config
        """
        import json

        try:
            with open(path) as config:
                conf = json.load(config)
            self.cur = self.getConn(
                conf['dbname'],
                conf['hostname'],
                conf['username'],
                conf['password'])
        except ValueError, e:
            print "Error loading JSON config. Detail: " + e

    def getConn(self, dbname, hostname, username, password):
        """ Get a PG connection
            @param dbname: The database name
            @type distrito: string
            @param hostname: The PG cluster url
            @type hostname: string
            @param username: User to connect PG
            @type username: string
            @param password: User PG password
            @type password: string
        """
        import psycopg2

        try:
            conn = psycopg2.connect(
                "dbname=" + dbname + " user=" + username + " host=" + hostname + " password=" + password)
            cur = conn.cursor()
            return cur
        except:
            print "I am unable to connect to the database"

    def closeConn(self):
        ''' Closes a connection cursor
        '''
        self.cur.close()

    def getDistritos(self):
        ''' Get district names from PG
        '''
        # TODO: Get query datamodel from config
        self.cur.execute("""SELECT distrito FROM mv_d_continente""")
        d = self.cur.fetchall()
        return d

    def getConcelhos(self, target, distrito):
        """ Get municipalities names by district
            @param target: The target view to query
            @type target: string
            @param distrito: The district name to query
            @type distrito: string
        """
        # TODO: Get query datamodel from config
        if target == 'ACORES':
            self.cur.execute('SELECT municipio FROM mv_acores')
        elif target == 'MADEIRA':
            self.cur.execute('SELECT municipio FROM mv_madeira')
        elif target == 'CONTINENTE':
            self.cur.execute('SELECT municipio FROM mv_continente WHERE distrito like %s;', (distrito,))
        c = self.cur.fetchall()
        return c
